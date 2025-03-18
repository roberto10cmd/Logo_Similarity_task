import pandas as pd

def save_urls_to_file(file_path, output_file):
    # Citirea datelor din fișierul .parquet dat ca intrare
    data = pd.read_parquet(file_path)
    urls = data['domain'].tolist()

    # salvarea pdf-urilor într-un fișier text
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')

file_path = r'C:\Users\robert\Desktop\New folder\logos.snappy (1).parquet'
output_file = 'urls.txt'
save_urls_to_file(file_path, output_file)
