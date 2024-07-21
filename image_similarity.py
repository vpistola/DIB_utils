import os
import time
from PIL import Image
import imagehash
import re
import cv2
from skimage import metrics

folder1 = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8'
folder2 = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\distinct\images'
folder3 = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\clusters\images'
similar_imgs = {}

def perceptual_hash(image_path, resize=False):
    image = Image.open(image_path)
    if resize == True:
        newsize = (2592,1944)
        image = image.resize(newsize)
    return imagehash.phash(image)


def rename_images(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            pos1 = file.index("_")
            pre = os.path.join(root, file)
            post = os.path.join(root, file[:pos1] + '.png')
            os.rename(pre, post)
            #m = re.match(r"_[0-9.a-z]+?\.(\w+)\.[0-9a-z]+", file)


def find_matching_images(folder1, folder2):
    folder1_hashes = {}
    folder2_hashes = {}
    matches = []

    for root, _, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            folder1_hashes[file_path] = perceptual_hash(file_path)

    for root, _, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            folder2_hashes[file_path] = perceptual_hash(file_path)

    for path1, hash1 in folder1_hashes.items():
        for path2, hash2 in folder2_hashes.items():
            if hash1 == hash2:
                matches.append((path1, path2))

    return matches
    

def ssim(image1, image2):
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]), interpolation = cv2.INTER_AREA)
    #print(image1.shape, image2.shape)
    
    # Convert images to grayscale
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Calculate SSIM
    ssim_score = metrics.structural_similarity(image1_gray, image2_gray, full=True)
    #print(f"SSIM Score: ", round(ssim_score[0], 2))
    return round(ssim_score[0], 2)


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

    matches = [(image1, image2) for image1 in folder1_images for image2 in folder2_images if ssim(image1, image2) > 0.95]
    return matches


## USING THE PHASH METHOD
## 1. distinct images
matches = find_matching_images(folder1, folder2)
# for match in matches:
#     print(f'Match found: {match[0]} and {match[1]}')
print(f'{len(matches)} matches in distinct folder have been found.')

## 2. clusters images
matches = find_matching_images(folder1, folder3)
# for match in matches:
#     print(f'Match found: {match[0]} and {match[1]}')
print(f'{len(matches)} matches in clusters folder have been found.')



## Rename files in folder
# rename_images(folder1)
# print('All files renamed.')


# img1 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\zn-1ppm-40x-8_jpg.rf.78c4b54ce612e3174122369d9a97375f.png' 
# img2 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\clusters\\images\\625.png'
# print(ssim(img1, img2))


## USING THE SSIM METHOD
# print("Find similarity in distinct images")
# s1=time.time()
# matches = find_matching_images_2(folder1, folder2)
# s2=time.time()
# print(f'{len(matches)} matches in distinct folder have been found in {s2-s1} ms.')