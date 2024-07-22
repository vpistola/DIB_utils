import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os
import time

orig_dir = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8'
distinct_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\distinct\images'
clusters_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\clusters\images'
similar_imgs = {}

def resize_image(image, size):
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

def mse(imageA, imageB):
    # Mean Squared Error
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def compare_images(image_path1, image_path2, size=(256, 256)):
    image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    image1_resized = resize_image(image1, size)
    image2_resized = resize_image(image2, size)

    m = mse(image1_resized, image2_resized)
    #s = ssim(image1_resized, image2_resized)

    return m

# img1 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\zn-1ppm-40x-8_jpg.rf.78c4b54ce612e3174122369d9a97375f.png' 
# img2 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\clusters\\images\\625.png'
# img3 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\cd-1ppm-40x-3_jpg.rf.7107a0b8c3d2a77b3ba94e08df56474a.png'
# img4 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\distinct\\images\\95.png'
# m, s = compare_images(img1, img2)       # different images
# m2, s2 = compare_images(img3, img3)     # similar images

# print(f'Mean Squared Error: {m}')
# print(f'Structural Similarity Index: {s}')
# print(f'Mean Squared Error: {m2}')
# print(f'Structural Similarity Index: {s2}')


def find_matching_images_2(folder1, folder2):
    folder1_images = []
    folder2_images = []

    for root, _, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            folder1_images.append(file_path)

    for root, _, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            folder2_images.append(file_path)

    matches = [(image1, image2) for image1 in folder1_images for image2 in folder2_images if compare_images(image1, image2) > 0]
    return matches


print("Find similarity in distinct images")
s1=time.time()
matches = find_matching_images_2(orig_dir, distinct_dir)
s2=time.time()
print(f'{len(matches)} matches in distinct folder have been found in {s2-s1} seconds!.')