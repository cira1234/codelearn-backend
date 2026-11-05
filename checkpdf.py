import sys
import fitz  # PyMuPDF

doc = fitz.open(sys.argv[1])

print("--- ข้อความหน้าแรก (เช็กภาษาไทย) ---")
print(doc[0].get_text()[:300])

print("--- สรุปรายหน้า ---")
print("หน้า | ตัวอักษร | รูป | เส้น/รูปวาด")
for i, page in enumerate(doc, start=1):
    print(i, len(page.get_text().strip()), len(page.get_images()), len(page.get_drawings()))