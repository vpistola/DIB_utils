import os
import time
from PIL import Image
from numpy import asarray
import scipy
import json
import shutil

orig_dir = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8'
orig_dir_dest1 = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\clusters'
orig_dir_dest2 = 'D:\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\distinct'
distinct_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\distinct\images'
clusters_dir = 'D:\MICRO_ALGAE_DATASET\\final_dataset\dataset\clusters\images'
distinct_p = False
load_p = True


def walk_directory(folder, is_set=False):
    if is_set == False:
        ret = []
    else:
        ret = set()
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if is_set == False: ret.append(file_path)
            if is_set == True: ret.add(file_path)
    return ret


def move_file(from_p, to_p):
    os.rename(from_p, to_p)


def find_matching_images(folder1, folder2):
    folder1_images = []
    folder2_images = []
    matches = []

    folder1_images = walk_directory(folder1)
    folder2_images = walk_directory(folder2)

    for im1 in folder1_images:
        img1 = Image.open(im1)
        img1 = img1.resize((640,640))
        for im2 in folder2_images:    
            np1 = asarray(img1)
            np2 = asarray(Image.open(im2))
            score = scipy.spatial.distance.hamming(np1.ravel(), np2.ravel())
            if score > 0.6: continue
            matches.append((im1, im2, score))
    
    return matches


def write_list(a_list, dt, fname):
    print("Started writing list data into a json file")
    with open(fname, "w") as fp:
        json.dump(a_list, fp)
        json.dump(f'{len(a_list)} matches in distinct folder have been found in {round(dt, 2)} seconds ({round(dt/60, 2)} minutes)!.', fp)
        print("Done writing JSON data into .json file")


if load_p:
    cl_set = set()
    dis_set = set()
    matches_orig = set()
    cnt1, cnt2 = 0, 0
        #pb-10ppm-40x-16_jpg.rf.dd9514dffd07336271ed298dba070f19.png
    orig_images = walk_directory(orig_dir, is_set=True)
    distinct_images = walk_directory(distinct_dir, is_set=True)
    clusters_images = walk_directory(clusters_dir, is_set=True)
    f1 = open('matches_cl.json')
    f2 = open('matches.json')
    data1 = json.load(f1)   ## clusters
    data2 = json.load(f2)   ## distinct
    f1.close()
    f2.close()

    for orig, new, score in sorted(data1):
        print(orig)
        cnt1 += 1
        fname1 = os.path.basename(orig)
        fname2 = os.path.basename(new)
        from_path = 'D:/MICRO_ALGAE_DATASET/algebra.v23i.yolov8' + '/' + fname1
        to_path = 'D:/MICRO_ALGAE_DATASET/algebra.v23i.yolov8/clusters' + '/' + fname2 
        shutil.move(from_path, to_path)
        #print(orig_dir + '\\' + fname1, orig_dir_dest1 + '\\' + fname1)
        #move_file(orig_dir + '\\' + fname1, orig_dir_dest1 + '\\' + fname1)     ## move to clusters folder
        #cl_set.add(new)
        #matches_orig.add(orig)    
    print(f'The operation moved {cnt1} files in clusters directory.')
    # for orig, new, score in data2:
    #     fname2 = os.path.basename(orig)
    #     move_file(orig_dir + '\\' + fname2, orig_dir_dest2 + '\\' + fname2)     ## move to distinct folder
    #     # dis_set.add(new)
    #     # matches_orig.add(orig)
    # print(f'Non matches from the clusters images : {clusters_images - cl_set}')
    # print(f'Non matches from the distinct images : {distinct_images - cl_set}')
    # print(f'Non matches from the original images : {orig_images - matches_orig}')
    # with open("non_matches.txt", "w") as f:
    #     f.write(f'Non matches from the clusters images : {clusters_images - cl_set}' + '\n')
    #     f.write('\n')
    #     f.write(f'Non matches from the distinct images : {distinct_images - dis_set}' + '\n')
    #     f.write('\n')
    #     f.write(f'Non matches from the original images : {orig_images - matches_orig}' + '\n')
else: 
    if distinct_p:
        print("Find similarity in distinct images")
        s1=time.time()
        matches = find_matching_images(orig_dir, distinct_dir)
        s2=time.time()
        dt = s2-s1
        write_list(matches, dt, 'matches.json')
        print("DONE!!!")
    else:
        print("Find similarity in clusters images")
        s1=time.time()
        matches_cl = find_matching_images(orig_dir, clusters_dir)
        s2=time.time()
        dt = s2-s1
        write_list(matches_cl, dt, 'matches_cl.json')
        print("DONE!!!")



'''
## FOR TESTING
# IDENTICAL
img1 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\zn-1ppm-40x-8_jpg.rf.78c4b54ce612e3174122369d9a97375f.png' 
img2 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\clusters\\images\\625.png'
# # IDENTICAL
img3 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\cd-1ppm-40x-3_jpg.rf.7107a0b8c3d2a77b3ba94e08df56474a.png'
img4 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\distinct\\images\\94.png'
# # DIFFERENT
img5 = 'D:\\MICRO_ALGAE_DATASET\\algebra.v23i.yolov8\\cd-1ppm-40x-3_jpg.rf.7107a0b8c3d2a77b3ba94e08df56474a.png'
img6 = 'D:\\MICRO_ALGAE_DATASET\\final_dataset\\dataset\\distinct\\images\\95.png'
image1 = Image.open(img1)
image1 = image1.resize((640,640))
np1 = asarray(image1)
np2 = asarray(Image.open(img4))
score = scipy.spatial.distance.hamming(np1.ravel(), np2.ravel())
print(f'Score: {score}')
'''