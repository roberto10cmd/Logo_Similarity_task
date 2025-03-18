import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def extract_logo_svd(image_path, output_folder, top_height=350, left_width=1500):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # citim imaginea
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # selectam doar partea de sus stanga
    gray_top_left = gray[:top_height, :left_width]

    # facem o binarizare adaptiva
    _, thresh = cv2.threshold(gray_top_left, 180, 255, cv2.THRESH_BINARY_INV)

    # gasim contururile
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f" Nu s-au gasit contururi în {image_path}")
        return

    # grupam componente conexe  (Convex Hull)
    hull = cv2.convexHull(np.vstack([contour for contour in contours]))
    x, y, w, h = cv2.boundingRect(hull)

    #
    aspect_ratio = w / float(h)
    if aspect_ratio < 0.3 or aspect_ratio > 5:
        print(f" Ignorat, nu pare logo corect {image_path}")
        return

    # salvam logo-ul
    logo = image[y:y+h, x:x+w]

    website_name = os.path.basename(image_path).replace('.png', '').lower()

    output_path = os.path.join(output_folder, os.path.basename(image_path))

    cv2.imwrite(output_path, logo)
    print(f" Logo extras: {output_path}")


image_folder = "output_images"
logo_folder = "output_logos_svd"

for image_file in os.listdir(image_folder):
    if image_file.endswith(".png"):
        extract_logo_svd(os.path.join(image_folder, image_file), logo_folder)
