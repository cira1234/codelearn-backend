import os
import fitz  # PyMuPDF

pdf_path = os.path.join("uploads", "slides", "chapter1.pdf")
out_dir = os.path.join("uploads", "slide_images")
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print("จำนวนหน้า:", len(doc))
for i, page in enumerate(doc, start=1):
    pix = page.get_pixmap(dpi=110)
    pix.save(os.path.join(out_dir, f"chapter1_p{i}.png"))
    print("บันทึกหน้า", i)