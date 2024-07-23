import os
import time
from PIL import Image
from numpy import asarray
import scipy
import json
import shutil
from collections import defaultdict
import sys

with open("config.json") as f:
    conf = json.load(f)
    orig_dir = conf['orig_dir']    
    orig_dir_dest1 = conf['orig_dir_dest1']   
    orig_dir_dest2 = conf['orig_dir_dest2']   
    distinct_dir = conf['distinct_dir']   
    clusters_dir = conf['clusters_dir']    
    distinct_p = conf['distinct_p']    
    load_p = conf['load_p']
    run_hamming = conf['run_hamming']     
    test_p = conf['test_p']         
    process_data1 = conf['process_data1']
    move_data1 = conf['move_data1']      
    process_data2 = conf['process_data2']
    move_data2 = conf['move_data2']   


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
    matches = defaultdict(list)
    dir1_img_array = []
    dir2_img_array = []

    folder1_images = walk_directory(folder1)
    folder2_images = walk_directory(folder2)

    ## Build image np array
    for im1 in folder1_images:
        img1 = Image.open(im1)
        img1 = img1.resize((640,640))
        np1 = asarray(img1)
        dir1_img_array.append((im1, np1))
    
    for im2 in folder2_images:
        np2 = asarray(Image.open(im2))
        dir2_img_array.append((im2, np2))

    for (im1, np1) in dir1_img_array:
        for (im2, np2) in dir2_img_array:    
            #np1 = asarray(img1)
            #np2 = asarray(Image.open(im2))
            score = scipy.spatial.distance.hamming(np1.ravel(), np2.ravel())
            if score > 0.6: continue
            matches[im1].append((im2, score))
    
    return matches


def write_list(a_list, dt, fname):
    print("Started writing list data into a json file")
    with open(fname, "w") as fp:
        json.dump(a_list, fp)
        json.dump(f'"timing": {len(a_list)} matches in distinct folder have been found in {round(dt, 2)} seconds ({round(dt/60, 2)} minutes)!.', fp)
        print("Done writing JSON data into .json file")


def fix_score(data):
    "Fix the data dict to keep the lowest score if multiple exists."
    fixed_data = []
    for im1, values in data.items():
        if len(values) > 1:
            min_score = min(x[1] for x in values)
            new_val = [x[0] for x in values if x[1] == min_score]
            #print(im1, min_score, new_val[0])
            fixed_data.append((im1, new_val[0], min_score))
        else:
            fixed_data.append((im1, values[0][0], values[0][1]))
    return fixed_data

if test_p == "True":
    test = 'D:/MICRO_ALGAE_DATASET/algebra.v23i.yolov8/cd-1ppm-40x-8_jpg.rf.befa1add74c6d71731f97c0974fca8e5.png'
    orig_images = walk_directory(orig_dir, is_set=True)
    print(orig_images)
    print(len(orig_images))
    print(test in orig_images)

if load_p == "True":
    cl_set = set()
    dis_set = set()
    matches_orig = set()
    cnt1, cnt2 = 0, 0
    fixed_data1 = []
    fixed_data2 = []    
        #pb-10ppm-40x-16_jpg.rf.dd9514dffd07336271ed298dba070f19.png
    orig_images = walk_directory(orig_dir, is_set=True)
    distinct_images = walk_directory(distinct_dir, is_set=True)
    clusters_images = walk_directory(clusters_dir, is_set=True)

    if process_data1 == "True":
        f1 = open('matches_cl.json')
        data1 = json.load(f1)   ## clusters
        f1.close()
    if process_data2 == "True":
        f2 = open('matches.json')
        data2 = json.load(f2)   ## distinct
        f2.close()
    
    fixed_data1 = fix_score(data1)  ## Fix scores in clusters data
    fixed_data2 = fix_score(data2)  ## Fix scores in distinct data

    if process_data1 == "True":  
        for orig, new, score in fixed_data1:
            cnt1 += 1    
            fname1 = os.path.basename(orig)
            fname2 = os.path.basename(new)
            from_path = orig_dir + fname1
            to_path = orig_dir_dest1 + fname2 
            #print(from_path + ' ==> ' + to_path)
            if move_data1 == "True": shutil.move(from_path, to_path)
            cl_set.add(new)
            matches_orig.add(orig)    
    print(f'The operation moved {cnt1} files in clusters directory.')
    
    # print(len(orig_images - matches_orig))    ## 628 - 159 => 469
    # sys.exit()

    if process_data2 == "True":
        for orig, new, score in fixed_data2:
            cnt2 += 1
            fname1 = os.path.basename(orig)
            fname2 = os.path.basename(new)
            from_path = orig_dir + fname1
            to_path = orig_dir_dest2 + fname2
            if move_data2 == "True": shutil.move(from_path, to_path) 
            dis_set.add(new)
            matches_orig.add(orig)
    print(f'The operation moved {cnt2} files in distinct directory.')

    # print(len(orig_images - matches_orig))    ## 628 - 159 - 446 = 23
    # sys.exit()
    
    with open("non_matches.txt", "w") as f:
        f.write(f'Non matches from the clusters images : {clusters_images - cl_set} (LENGTH = {len(clusters_images - cl_set)})' + '\n')
        f.write('\n')
        f.write(f'Non matches from the distinct images : {distinct_images - dis_set} (LENGTH = {len(distinct_images - dis_set)})' + '\n')
        f.write('\n')
        f.write(f'Non matches from the original images : {orig_images - matches_orig} (LENGTH = {len(orig_images - matches_orig)})' + '\n')

if run_hamming == "True": 
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