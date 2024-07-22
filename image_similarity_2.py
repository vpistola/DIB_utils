import os
import time
from PIL import Image
import imagehash
import re
import cv2
from skimage import metrics

orig_dir = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8'
distinct_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\distinct\images'
clusters_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\clusters\images'
similar_imgs = {}


def find_matching_images(folder1, folder2):
    folder1_hashes = {}
    folder2_hashes = {}
    matches = []
    non_matches = []

    for root, _, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            folder1_hashes[file_path] = str(imagehash.phash(Image.open(file_path)))

    for root, _, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            folder2_hashes[file_path] = str(imagehash.phash(Image.open(file_path)))

    for path1, hash1 in folder1_hashes.items():
        for path2, hash2 in folder2_hashes.items():
            if hash1 == hash2:    
                matches.append((path1, path2))
            elif hash1 != hash2:
                non_matches.append((path1, path2))

    return non_matches


## USING THE PHASH METHOD
## 1. distinct images
matches = find_matching_images(orig_dir, distinct_dir)
print(matches)
print(len(matches))


# img1 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\zn-1ppm-40x-8_jpg.rf.78c4b54ce612e3174122369d9a97375f.png' 
# img2 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\clusters\\images\\625.png'
# img3 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\cd-1ppm-40x-3_jpg.rf.7107a0b8c3d2a77b3ba94e08df56474a.png'
# img4 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\distinct\\images\\95.png'

# hash0 = imagehash.phash(Image.open(img1)) 
# hash1 = imagehash.phash(Image.open(img2))
# print(hash0)
# print(hash1)
# print(hash0 == hash1)

# folder1_hashes = {}
# for root, _, files in os.walk(orig_dir):
#         for file in files:
#             file_path = os.path.join(root, file)
#             hash1 = imagehash.phash(Image.open(file_path))
#             folder1_hashes[file_path] = hash1

# print(folder1_hashes.items())