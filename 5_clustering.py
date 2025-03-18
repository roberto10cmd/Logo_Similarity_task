import os
import torch
import numpy as np
import cv2
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from torchvision import models, transforms
from PIL import Image
from torchvision.models import resnet50, ResNet50_Weights


# folosim ResNet50 pentru extragerea caracteristicilor
model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # eliminam ultimul strat de clasificare
model.eval()

# preprocesarea imaginilor
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def is_black_and_white(image_path, threshold=0.05):
    # Verifica daca imaginea este predominant alb-negru
    image = cv2.imread(image_path)
    if image is None:
        return True

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    color_diff = cv2.absdiff(image, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))


    percent_color = np.count_nonzero(color_diff) / color_diff.size

    return percent_color < threshold  # Returnează true dacă imaginea este alb-negru


def extract_deep_features(image_path):
    # extragem caracteristici
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # adaugam batch dimension

    with torch.no_grad():
        features = model(image).squeeze().numpy()  # scoatem din tensor

    return features.flatten()


def get_website_from_logo(logo_path):
    filename = os.path.basename(logo_path).lower()
    website = filename.replace("_logo.png", "")
    return website


def cluster_logos(image_folder, eps=10, min_samples=2, max_pca_components=50):
    # aplicam clustering pe logo-uri si returneaza website-urile grupate + date pentru vizualizare
    logo_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(".png")]

    #   dictionar pentru a asocia logo-urile cu website-urile
    logo_to_website = {path: get_website_from_logo(path) for path in logo_paths}

    # filtrare cu alb-negru inainte de clustering
    filtered_paths = [path for path in logo_paths if not is_black_and_white(path)]

    feature_vectors = []
    valid_paths = []

    for path in filtered_paths:
        features = extract_deep_features(path)
        feature_vectors.append(features)
        valid_paths.append(path)

    if not feature_vectors:
        print(" nu s-au gasit logo-uri .")
        return None, None, None, None

    feature_vectors = np.array(feature_vectors)

    num_samples, num_features = feature_vectors.shape
    n_components = min(max_pca_components, num_samples, num_features)

    if n_components > 1:
        pca = PCA(n_components=n_components)
        reduced_features = pca.fit_transform(feature_vectors)
    else:
        reduced_features = feature_vectors

    #  DBSCAN pentru clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    labels = dbscan.fit_predict(reduced_features)

    #  grupam website-urile în funcție de cluster
    website_clusters = {}
    for logo_path, label in zip(valid_paths, labels):
        website = logo_to_website[logo_path]
        if label not in website_clusters:
            website_clusters[label] = set()  # Folosim set() pentru a evita duplicate
        website_clusters[label].add(website)

    return website_clusters, labels, reduced_features, valid_paths


def display_clusters(website_clusters):
    # afisam website urile in functie de clustere
    for cluster_id, websites in website_clusters.items():
        print(f"\n Cluster {cluster_id + 1}:")
        for website in websites:
            print(f"   - {website}")



image_folder = "output_logos_svd"
website_clusters, labels, reduced_features, valid_paths = cluster_logos(image_folder)

if website_clusters:
    display_clusters(website_clusters)
