import os
import cv2

def extract_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return descriptors

def find_matching_images(folder1, folder2):
    folder1_features = {}
    folder2_features = {}

    for root, _, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            folder1_features[file_path] = extract_features(file_path)

    for root, _, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            folder2_features[file_path] = extract_features(file_path)

    bf = cv2.BFMatcher()
    matches = []
    for path1, desc1 in folder1_features.items():
        for path2, desc2 in folder2_features.items():
            if desc1 is not None and desc2 is not None:
                match = bf.knnMatch(desc1, desc2, k=2)
                good_matches = [m for m, n in match if m.distance < 0.75 * n.distance]
                if len(good_matches) > 10:  # threshold for a good match
                    matches.append((path1, path2))

    return matches

folder1 = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8'
folder2 = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\clusters\images'
folder3 = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\distinct\images'
matches = find_matching_images(folder1, folder2)
for match in matches:
    print(f'Match found: {match[0]} and {match[1]}')

print(f'Found {len(matches)} matches')
