import os
from PIL import Image
from itertools import chain
import filecmp

paths = (r'D:\MICRO_ALGAE_DATASET\final_dataset\clusters\\', r'D:\MICRO_ALGAE_DATASET\final_dataset\distinct\\')
clusters_path = paths[0]
distinct_path = paths[1]

bbs_ext = '.txt'
masks_ext = '.png'

# Find the image names from the clusters folder and move the
# respective bbs and masks from the distinct folder to clusters
for (root, dirs, files) in os.walk(clusters_path + 'images'):
    for file in files:
        bname = os.path.splitext(file)[0]
        #print('BBS => ', bname, distinct_path + 'bbs\\' + bname + bbs_ext, clusters_path  + 'bbs\\' + bname + bbs_ext)
        #print('MASKS => ', bname, distinct_path + 'masks\\' + bname + masks_ext, clusters_path  + 'masks\\' + bname + masks_ext)
        os.rename(distinct_path + 'bbs\\' + bname + bbs_ext, clusters_path  + 'bbs\\' + bname + bbs_ext)
        os.rename(distinct_path + 'masks\\' + bname + masks_ext, clusters_path  + 'masks\\' + bname + masks_ext)


print('---- IMAGE MOVING TO CLUSTERS FOLDER COMPLETED ----')