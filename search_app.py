import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import shutil  
import search_engine
import sahm_languages   

class FastSearchApp:
    def __init__(self, root):
        self.root = root
        self.lang = 'ar'
        self.all_files = []      
        self.filtered_files = [] 
        self.displayed_count = 0 
        self.chunk_size = 500     
        self.fav_file = "favorites.json"
        self.showing_fav = False
        self.search_timer = None  
        
        try:
            if os.path.exists("logo.ico"):
                self.root.iconbitmap("logo.ico")
        except Exception:
            pass
            
        self.load_favorites()
        self.setup_ui()
        self.update_ui_text()

    def setup_ui(self):
        self.root.geometry("1150x650") 
        self.root.configure(bg="#1e1e2e")
                
        lang_frame = tk.Frame(self.root, bg="#1e1e2e")
        lang_frame.pack(fill=tk.X, padx=10, pady=2)
        self.lang_select = ttk.Combobox(lang_frame, values=['ar', 'en', 'fr'], width=5, state="readonly")
        self.lang_select.set(self.lang)
        self.lang_select.pack(side=tk.LEFT, padx=5)
        self.lang_select.bind("<<ComboboxSelected>>", self.change_language)
        
        self.top_frame = tk.Frame(self.root, bg="#1e1e2e")
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_drive = tk.Label(self.top_frame, bg="#1e1e2e", fg="white", font=("Cairo", 11, "bold"))
        self.lbl_drive.pack(side=tk.RIGHT, padx=5)
        
        drives = [f"{chr(x)}:\\" for x in range(65, 91) if os.path.exists(f"{chr(x)}:\\")]
        self.drive_select = ttk.Combobox(self.top_frame, values=drives, width=10, font=("Cairo", 10))
        self.drive_select.pack(side=tk.RIGHT, padx=5)
        if drives: self.drive_select.current(0)
        
        self.btn_index = tk.Button(self.top_frame, bg="#a6e3a1", fg="#11111b", font=("Cairo", 10, "bold"), command=self.start_indexing)
        self.btn_index.pack(side=tk.RIGHT, padx=10)
        
        self.lbl_status = tk.Label(self.top_frame, bg="#1e1e2e", font=("Cairo", 10))
        self.lbl_status.pack(side=tk.LEFT, padx=10)
        
        search_frame = tk.Frame(self.root, bg="#1e1e2e")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_search = tk.Label(search_frame, bg="#1e1e2e", fg="white", font=("Cairo", 11, "bold"))
        self.lbl_search.pack(side=tk.RIGHT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.debounce_search())
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg="#313244", fg="white", font=("Cairo", 11))
        self.search_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        self.lbl_results_count = tk.Label(search_frame, bg="#1e1e2e", fg="#b4befe", font=("Cairo", 10, "bold"))
        self.lbl_results_count.pack(side=tk.LEFT, padx=10)
        
        center_frame = tk.Frame(self.root, bg="#1e1e2e")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.filter_frame = tk.Frame(center_frame, bg="#181825", width=150)
        self.filter_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.filter_frame.pack_propagate(False)
        
        self.lbl_filter = tk.Label(self.filter_frame, bg="#181825", fg="#cdd6f4", font=("Cairo", 10, "bold"))
        self.lbl_filter.pack(pady=10)
        
        self.filter_type = tk.StringVar(value="all")
        self.radio_all = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="all", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_all.pack(anchor=tk.W, padx=10, pady=5)
        self.radio_folders = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="folders", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_folders.pack(anchor=tk.W, padx=10, pady=5)
        self.radio_images = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="images", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_images.pack(anchor=tk.W, padx=10, pady=5)
        self.radio_docs = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="docs", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_docs.pack(anchor=tk.W, padx=10, pady=5)
                
        self.radio_videos = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="videos", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_videos.pack(anchor=tk.W, padx=10, pady=5)
        self.radio_audios = tk.Radiobutton(self.filter_frame, variable=self.filter_type, value="audios", bg="#181825", fg="white", selectcolor="#313244", font=("Cairo", 9), command=self.instant_search)
        self.radio_audios.pack(anchor=tk.W, padx=10, pady=5)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#252538", foreground="white", fieldbackground="#252538", rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background="#313244", foreground="white", font=("Cairo", 10, "bold"))
        style.map("Treeview", background=[('selected', '#585b70')])
        
        grid_frame = tk.Frame(center_frame, bg="#1e1e2e")
        grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(grid_frame, columns=('name', 'size', 'path'), show='headings')
        scrollbar = ttk.Scrollbar(grid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.bind("<Double-1>", self.open_file)
        
        bottom_bar = tk.Frame(self.root, bg="#1e1e2e")
        bottom_bar.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_open_folder = tk.Button(bottom_bar, bg="#89b4fa", fg="#11111b", font=("Cairo", 10, "bold"), command=self.open_file_folder)
        self.btn_open_folder.pack(side=tk.RIGHT, padx=5)
        self.btn_delete_file = tk.Button(bottom_bar, bg="#f38ba8", fg="#11111b", font=("Cairo", 10, "bold"), command=self.delete_selected_file)
        self.btn_delete_file.pack(side=tk.RIGHT, padx=5)
        self.btn_fav = tk.Button(bottom_bar, bg="#f9e2af", fg="#11111b", font=("Cairo", 10, "bold"), command=self.add_to_favorites)
        self.btn_fav.pack(side=tk.RIGHT, padx=5)
        self.btn_show_fav = tk.Button(bottom_bar, bg="#fab387", fg="#11111b", font=("Cairo", 10, "bold"), command=self.toggle_favorites_view)
        self.btn_show_fav.pack(side=tk.RIGHT, padx=5)
        self.btn_load_more = tk.Button(bottom_bar, bg="#b4befe", fg="#11111b", font=("Cairo", 10, "bold"), command=self.load_more_results)
        self.btn_load_more.pack(side=tk.LEFT, padx=5)

    def change_language(self, event):
        self.lang = self.lang_select.get()
        self.update_ui_text()
        self.instant_search()

    def update_ui_text(self):
        tx = sahm_languages.LOCALES[self.lang]
        self.root.title(tx['title'])
        self.lbl_drive.config(text=tx['drive'])
        self.btn_index.config(text=tx['btn_index'])
        self.lbl_status.config(text=tx['status_ready'] if not self.all_files else f"{tx['status_ready']} ({len(self.all_files)})", fg="#a6e3a1")
        self.lbl_search.config(text=tx['search'])
        self.lbl_filter.config(text=tx['filter_title'])
        self.radio_all.config(text=tx['all'])
        self.radio_folders.config(text=tx['folders'])
        self.radio_images.config(text=tx['images'])
        self.radio_docs.config(text=tx['docs'])
        self.radio_videos.config(text=tx['videos']) 
        self.radio_audios.config(text=tx['audios']) 
        self.btn_open_folder.config(text=tx['btn_open'])
        self.btn_delete_file.config(text=tx['btn_delete'])
        self.btn_fav.config(text=tx['btn_fav'])
        self.btn_load_more.config(text=tx['btn_load'])
        self.tree.heading('name', text=tx['col_name'])
        self.tree.heading('size', text=tx['col_size'])
        self.tree.heading('path', text=tx['col_path'])
        
        if self.showing_fav:
            back_text = {'ar': "↩️ رجوع للبحث", 'en': "↩️ Back to Search", 'fr': "↩️ Retour"}
            self.btn_show_fav.config(text=back_text.get(self.lang, "Back"), bg="#f38ba8")
        else:
            self.btn_show_fav.config(text=tx['btn_show_fav'], bg="#fab387")

    def load_favorites(self):
        if os.path.exists(self.fav_file):
            with open(self.fav_file, 'r', encoding='utf-8') as f:
                self.favorites = json.load(f)
        else: self.favorites = []

    def save_favorites(self):
        with open(self.fav_file, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=4)

    def add_to_favorites(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']
        if item and len(item) > 2:
            f_data = {'name': str(item[0]), 'size_str': str(item[1]), 'path': str(item[2]), 'is_dir': "📁" in str(item[0]), 'size': 0}
            if f_data['path'] not in [x['path'] for x in self.favorites]:
                self.favorites.append(f_data)
                self.save_favorites()
                messagebox.showinfo("Sahm", sahm_languages.LOCALES[self.lang]['fav_added'])

    def toggle_favorites_view(self):
        self.showing_fav = not self.showing_fav
        self.update_ui_text()
        
        if self.showing_fav:
            self.filtered_files = self.favorites
            self.tree.delete(*self.tree.get_children())
            self.displayed_count = 0
            self.load_more_results()
        else:
            self.instant_search()

    def start_indexing(self):
        drv = self.drive_select.get()
        if not drv:
            messagebox.showwarning("!", sahm_languages.LOCALES[self.lang]['alert_drive'])
            return
        self.lbl_status.config(text=sahm_languages.LOCALES[self.lang]['status_scanning'], fg="#f9e2af")
        self.btn_index.config(state=tk.DISABLED)
        threading.Thread(target=self.run_scan, args=(drv,), daemon=True).start()

    def run_scan(self, drive):
        self.all_files = search_engine.scan_drive(drive)
        self.root.after(0, self.indexing_complete)

    def indexing_complete(self):
        self.showing_fav = False
        self.btn_index.config(state=tk.NORMAL)
        self.update_ui_text()
        self.instant_search()

    def debounce_search(self):
        if self.search_timer:
            self.root.after_cancel(self.search_timer)
        self.search_timer = self.root.after(300, self.instant_search)

    def instant_search(self):
        if self.showing_fav: return
        query = self.search_var.get().lower().strip()
        f_type = self.filter_type.get()
        self.filtered_files = []
        
        for file in self.all_files:
            if query not in file['name'].lower(): continue
            if f_type == "folders" and not file['is_dir']: continue
            if f_type == "images" and not any(file['name'].lower().endswith(e) for e in ['.jpg', '.jpeg', '.png', '.webp', '.gif']): continue
            if f_type == "docs" and not any(file['name'].lower().endswith(e) for e in ['.pdf', '.txt', '.docx', '.xlsx', '.pptx']): continue
                        
            if f_type == "videos" and not any(file['name'].lower().endswith(e) for e in ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv']): continue
            if f_type == "audios" and not any(file['name'].lower().endswith(e) for e in ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg']): continue
                        
            if file['is_dir']:
                icon = "📁"
            elif f_type == "videos" or any(file['name'].lower().endswith(e) for e in ['.mp4', '.mkv', '.avi']):
                icon = "🎬"
            elif f_type == "audios" or any(file['name'].lower().endswith(e) for e in ['.mp3', '.wav', '.m4a']):
                icon = "🎵"
            else:
                icon = "📄"
                
            self.filtered_files.append({
                'name': f"{icon} {file['name']}", 'path': file['path'], 'size': file['size'],
                'size_str': search_engine.get_readable_size(file['size'], self.lang) if not file['is_dir'] else "--"
            })
            
        self.filtered_files.sort(key=lambda x: x['size'], reverse=True)
        self.tree.delete(*self.tree.get_children())
        self.displayed_count = 0
        self.load_more_results()

    def load_more_results(self):
        start = self.displayed_count
        end = min(start + self.chunk_size, len(self.filtered_files))
        for i in range(start, end):
            f = self.filtered_files[i]
            self.tree.insert('', tk.END, values=(f['name'], f['size_str'], f['path']))
        self.displayed_count = end
        self.lbl_results_count.config(text=sahm_languages.LOCALES[self.lang]['results'].format(self.displayed_count, len(self.filtered_files)))
        if self.displayed_count < len(self.filtered_files):
            self.btn_load_more.pack(side=tk.LEFT, padx=5)
        else:
            self.btn_load_more.pack_forget()

    def open_file(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel)['values']
            if item and len(item) > 2:
                try: os.startfile(str(item[2]))
                except Exception as e: messagebox.showerror("Error", str(e))

    def open_file_folder(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']
        if item and len(item) > 2:
            p = str(item[2])
            fld = p if os.path.isdir(p) else os.path.dirname(p)
            try: os.startfile(fld)
            except Exception as e: messagebox.showerror("Error", str(e))

    def delete_selected_file(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']
        if item and len(item) > 2:
            name, path = str(item[0]), str(item[2])
            if messagebox.askyesno("?", sahm_languages.LOCALES[self.lang]['confirm_del'].format(name)):
                try:
                    if os.path.isdir(path): 
                        shutil.rmtree(path)  
                    else: 
                        os.remove(path)
                        
                    self.all_files = [x for x in self.all_files if x['path'] != path]
                    self.favorites = [x for x in self.favorites if x['path'] != path]
                    self.save_favorites()
                    self.instant_search()
                except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FastSearchApp(root)
    root.mainloop()