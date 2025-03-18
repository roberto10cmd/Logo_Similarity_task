# Logo_Similarity_Match

"Logo Similarity" realizeaza clusteringul logo-urilor pentru a grupa website-urile care au logo-uri similare.

  Workflow & Scripturi

1_extract_urls.py  :  Extragerea url-urilor din fisierul dat ca input.  
2_extract_pdfs.js  :  Crearea de capturi de ecran in format PDF.  
3_extract_images.py : Extragerea imaginilor din PDF-uri.  
4_extract_logos.py : Detectia si decuparea logo-urilor din imagini. 

5_clustering.py    : Aplicarea clusteringului pe logo-uri si gruparea website-urilor.


Instalare & Configurare

1. git clone https://github.com/roberto10cmd/Logo_Similarity_task.git
2. rularea scripturilor in ordinea de mai sus


Tehnologii Utilizate : 

  1. OpenCV  : procesarea imaginilor si detectia contururilor
  2. Scikit-learn : pt clustering DBSCAN
  3. Puppeteer pt capturarea paginilor web
  4. pdf2image pt conversia PDF -> PNG
  5. Torch si Resnet50 : extragerea caracteristicilor din logo-uri
 
