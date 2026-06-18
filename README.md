# سهم | Sahm - محرك البحث الفائق للأقراص

سهم هو أداة خفيفة الوزن وسريعة جداً، برمجت خصيصاً لمسح وفهرسة الهاردات والأقراص الممتلئة، والعثور على الملفات والمجلدات في أجزاء من الثانية دون استهلاك موارد الجهاز. يمتلك التطبيق واجهة رسومية عصرية تدعم تغيير اللغات لحظياً.

## الميزات الرئيسية

1. بحث فوري ذكي: يبدأ البحث فور توقفك عن الكتابة بـ 300 جزء من الثانية لضمان سلاسة الواجهة تماماً ومنع التجميد.
2. تحميل تدريجي: يعرض البرنامج النتائج على دفعات مرتبة تلقائياً حسب الحجم من الأكبر للأصغر لتوفير استهلاك الذاكرة العشوائية.
3. فلاتر نوعية متقدمة: تصفية فورية لعرض كل الملفات، المجلدات، الصور، المستندات، الفيديوهات، والصوتيات.
4. نظام المفضلة: إمكانية حفظ مسارات ملفاتك المهمة للوصول السريع إليها لاحقاً.
5. حذف آمن ومباشر: القدرة على حذف الملفات والمجلدات مباشرة من داخل التطبيق بأمان بفضل مكتبة النظام.

## كيفية التشغيل

المشروع يعتمد بالكامل على مكتبات بايثون القياسية المدمجة، فلن تحتاج لتثبيت أي مكتبات خارجية.

1. تأكد من تثبيت لغة Python على جهازك.
2. افتح مجلد المشروع في VS Code.
3. افتح الـ Terminal وشغّل الأمر التالي:
   python search_app.py

ملاحظة: قد يطلب التطبيق صلاحيات المسؤول عند التشغيل، وذلك لتتمكن الأداة من قراءة أحجام الملفات العميقة داخل النظام وتنظيف كاش الأقراص بنجاح.

## الترخيص القانوني

هذا المشروع مرخص بموجب ترخيص GNU GPLv3.
- مسموح: بالاستخدام الشخصي، الاطلاع على الكود، وتعديله بغرض التعلم والتطوير.
- يشترط: إذا قمت بإعادة نشر الكود أو تعديله، يجب أن يكون مشروعك الجديد مجانياً ومفتوح المصدر بالكامل وتحت نفس الترخيص.
- غير قابل للبيع: يمنع منعاً باتاً أخذ هذا الكود أو أجزاء منه بغرض البيع أو الاستخدام في برمجيات مغلقة المصدر.

---

# Sahm - Ultra Fast File Finder

Sahm is a lightweight and ultra-fast file search engine designed specifically to scan and index large or cluttered drives, finding files and folders in milliseconds without draining system resources. The application features a modern Dark Mode interface with instant multi-language support.

## Key Features

1. Instant Search: The search triggers 300ms after you stop typing, ensuring absolute GUI stability and preventing freezing.
2. Lazy Loading: Displays results in managed batches sorted by size from largest to smallest to optimize RAM consumption.
3. Advanced Quick Filters: Instant filtering by type including All Files, Folders, Images, Documents, Videos, and Audios.
4. Favorites System: Save important file or folder paths to your personal favorites list for quick access anytime.
5. Smart and Safe Deletion: Delete files and folders directly from the application safely via system library.

## How to Run

Since the project relies solely on Python's built-in standard libraries, you do not need to install any external dependencies.

1. Make sure Python is installed on your system.
2. Open the project folder in VS Code.
3. Open the Terminal and run the following command:
   python search_app.py

Note: The application may request Administrator privileges upon launch to enable the scanner to read deep system file sizes and successfully purge drive caches.

## License

This project is licensed under the GNU GPLv3 License.
- Permitted: Personal use, viewing, and modifying the code for educational or development purposes.
- Condition: If you modify or redistribute this code, your project MUST also be free, open-source, and under the exact same license.
- Strictly Non-Commercial: It is forbidden to take this code or any part of it to sell or include in closed-source commercial software.
