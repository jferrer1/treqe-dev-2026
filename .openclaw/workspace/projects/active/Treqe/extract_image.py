import fitz  # PyMuPDF
import sys
import os

pdf_path = r"Downloads_assets\Treqe_low_1.pdf"
output_path = r"treqe-girl-skate-real.png"

# Open PDF
doc = fitz.open(pdf_path)
print(f"PDF has {doc.page_count} pages")

# Pages 42-43 (1-indexed) -> zero-indexed 41,42
pages = [41, 42] if doc.page_count > 42 else [doc.page_count - 1]
image_count = 0
for page_num in pages:
    page = doc.load_page(page_num)
    images = page.get_images()
    print(f"Page {page_num+1} has {len(images)} images")
    for img_index, img_info in enumerate(images):
        xref = img_info[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha < 4:  # Convert to RGB if needed
            pix = fitz.Pixmap(fitz.csRGB, pix)
        # Save first image found
        pix.save(output_path)
        print(f"Saved image {img_index+1} from page {page_num+1} to {output_path} ({pix.width}x{pix.height})")
        pix = None
        image_count += 1
        break  # only first image
    if image_count > 0:
        break

doc.close()
if image_count == 0:
    print("No images found in pages 42-43")
    sys.exit(1)