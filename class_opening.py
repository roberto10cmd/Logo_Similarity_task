import pandas as pd
import pdfkit
import os
import time
from concurrent.futures import ThreadPoolExecutor
def convert_to_pdf(url):
    output_filename = 'output_pdfs/' + url.split('//')[-1].replace('.', '_').replace('/', '_') + '.pdf'

    options = {
        'javascript-delay': '5000',  # Mărește timpul de așteptare pentru JavaScript la 5000 ms
        'no-background': '',
        'no-stop-slow-scripts': '',  # Nu opri scripturile lente
        'enable-javascript': '',
        'debug-javascript': '',  # Activează debug-ul pentru JavaScript
    }

    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    try:
        if not os.path.exists('output_pdfs'):
            os.makedirs('output_pdfs')
        pdfkit.from_url(url, output_filename,options=options,configuration= config)
        print(f"PDF creat pentru {url}: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Eroare la crearea PDF-ului pentru {url}: {str(e)}")
        return None


def open_pdf(pdf):
    if pdf:
        # Verifică dacă fișierul există și este complet scris
        while not os.path.isfile(pdf):
            time.sleep(1)  # Așteaptă 1 secundă până când fișierul este disponibil
        print("Deschiderea PDF-ului:", pdf)
        os.startfile(pdf)

def main():
    file_path = r'C:\Users\robert\Desktop\New folder\logos.snappy (1).parquet'
    data = pd.read_parquet(file_path)
    urls = data['domain'].tolist()

    # Limitează numărul de URL-uri procesate la primele 4 pentru testare
    limited_urls = urls[:50]

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(convert_to_pdf, limited_urls))



if __name__ == "__main__":
    main()