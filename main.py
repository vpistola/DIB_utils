import os
from PIL import Image
from itertools import chain
import filecmp

paths = (r'D:\temp\dataset_for_segmentation_masks\images2', r'D:\temp\dataset_for_segmentation_masks\bbs', r'D:\temp\dataset_for_segmentation_masks\backup\images2')
basename0 = paths[0] + '\\'
basename1 = paths[1] + '\\'
basename2 = paths[2] + '\\'
cnt = 1
rename = False
convert = False
check = False

# Rename both the image and the bounding box
if rename:
    for (root1, dirs1, files1), (root2, dirs2, files2) in zip(os.walk(paths[0]), os.walk(paths[1])):
        for file1, file2 in zip(files1, files2):
            os.rename(basename0 + file1, basename0 + str(cnt)+'.jpg')
            os.rename(basename1 + file2, basename1 + str(cnt)+'.txt')
            cnt += 1

# Convert to png
if convert:
    for (root, dirs, files) in os.walk(paths[0]):
        for file in files:
            im = Image.open(basename0 + file)
            im.save(basename0 + file[:-4] + '.png')

# Compare files if are the same after renaming
if check:
    for (root1, dirs1, files1), (root2, dirs2, files2) in zip(os.walk(paths[0]), os.walk(paths[2])):
        assert all(filecmp.cmp(basename0 + file1, basename2 + file2) for file1, file2 in zip(files1, files2)) == True
            
# file1 = r'D:\\temp\\dataset_for_segmentation_masks\\' + '1.jpg'
# file2 = r'D:\\temp\\dataset_for_segmentation_masks\\' + 'cd-10-ppm-40x-1_jpg.rf.239d9729f05d767a110f5f5c41c4bed6.jpg'
# print(filecmp.cmp(file1, file2))
print('---- DONE ----')