import os
from pdf2image import convert_from_path

def extract_images_from_pdfs(pdf_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            images = convert_from_path(pdf_path, poppler_path=r"C:\Release-24.08.0-0\poppler-24.08.0\Library\bin",
                                       dpi=300)
            image_path = os.path.join(output_folder, pdf_file.replace('.pdf', '.png'))
            images[0].save(image_path, 'PNG')
            print(f"✅ Imagine extrasă: {image_path}")

# Rulează funcția
extract_images_from_pdfs("output_pdfs", "output_images")
