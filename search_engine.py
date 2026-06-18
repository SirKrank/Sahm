import os
import shutil

def get_readable_size(size_in_bytes, lang='ar'):
    if size_in_bytes == 0:
        return "--"
    units = {
        'ar': ['بايت', 'كيلوبايت', 'ميجابايت', 'جيجابايت', 'تيرابايت'],
        'en': ['B', 'KB', 'MB', 'GB', 'TB'],
        'fr': ['B', 'KB', 'MB', 'GB', 'TB']
    }
    current_units = units.get(lang, units['en'])
    for unit in current_units:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} {current_units[-1]}"

def scan_drive(drive):
    results = []
    try:
        for root_path, dirs, files in os.walk(drive, topdown=True):
            
            dirs[:] = [d for d in dirs if d not in ['$Recycle.Bin', 'System Volume Information', 'Recovery', 'AppData', 'Program Files', 'Windows']]
            
            for sub_dir in dirs:
                try:
                    full_path = os.path.join(root_path, sub_dir)
                    
                    results.append({'name': sub_dir, 'path': full_path, 'size': 0, 'is_dir': True})
                except Exception: continue

            for file in files:
                try:
                    full_path = os.path.join(root_path, file)
                    f_size = os.path.getsize(full_path)
                    results.append({'name': file, 'path': full_path, 'size': f_size, 'is_dir': False})
                except Exception: continue
    except Exception: pass
    return results