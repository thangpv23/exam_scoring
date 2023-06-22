import cv2

import numpy as np 
import os
import imutils
from imutils import contours
from PIL import Image, ImageTransform


def exam50_scoring(image, answer_key):
    center_points = []
    
    im2 = image
    im2 = cv2.resize(im2,(3030, 3400))

    #  y,x coordinates of top-left, bottom-left, bottom-right and top-right corners
    shape_y = im2.shape[0]
    shape_x = im2.shape[1]
    image2detect = [im2[400:900, 300:800], 
                    im2 [im2.shape[0]-300:, 0:800], 
                    im2 [im2.shape[0]-500:im2.shape[0]-100, im2.shape[1]-700:im2.shape[1]-200] ,
                    im2 [400:800,  im2.shape[1]-800:im2.shape[1]-200]]
                    
    # image2detect = [image2detect[2]]
    offset = [[400, 300],  [shape_y-300, 0],[shape_y-500, shape_x-700], [400, shape_x-800]]

    for roi in image2detect:

        roi_gray = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = np.ones((5, 5), np.uint8)
        roi_gray = cv2.erode(roi_gray, kernel, iterations=2)
        edges= cv2.Canny(roi_gray, 200,255)

        contours, hierarchy= cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # print(contours[0][0][0])
        # contours = np.array(contours[0])
        # print(contours[0][0])
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center_points.append([cX, cY])



    for n, point in enumerate (center_points):
        # if n > 0:
        #     break
        point[0] += offset[n][1]
        point[1] += offset[n][0]

        cv2.circle(im2, point, 20, (0, 0, 255), -1)


    PIL_align_coor = []

    # Define 8-tuple with y,x coordinates of top-left, bottom-left, bottom-right and top-right corners and apply
    for point in center_points:
        PIL_align_coor.append(point[0])
        PIL_align_coor.append(point[1])


    color_coverted = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_coverted)
    result = pil_image.transform((1654 ,2339), ImageTransform.QuadTransform(PIL_align_coor))

    res_cv = np.array(result) 
    full_form = res_cv



    correct_list= []
    false_list=[]

    offset_visualize = []
    coor_false_visualize = []


    align_coor1 = full_form[ 757:2277,5:425 ]

    align_coor2 = full_form[757:1777, 410:825] 

    offset_fullform_x = [5, 410]

    align_coor_list= [align_coor1, align_coor2]
    # align_coor_list= [align_coor1]


    answer_list=[]

    for block, align_coor in enumerate (align_coor_list):

        new_img = align_coor

        # block=0
        region_list_1=[new_img[:260 ,:], new_img[260:510, :],new_img[510:770 ,:], new_img[760:1020 ,:] , new_img[1020: 1270 ,:], new_img[1270:  ,:] ]
        region_list_2 = [ new_img[:260 ,:], new_img[260:510, :],new_img[510:770 ,:], new_img[760:1020 ,:]]
        # region_list=[region_list_or[0]]
        # region_list_1 = [ new_img[:260 ,:]]
        offset_region_list = [0, 260, 510, 760, 1010, 1270]


        x_range = 70
        y_range = 50
        if block < 1 :
            region_list = region_list_1
        else:
            region_list = region_list_2
        for n, region in enumerate (region_list):
            
            offset_y = offset_region_list[n]

            new_img_gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            tmp  = cv2.threshold(new_img_gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
            tmp = cv2.bitwise_not(tmp)
            kernel = np.ones((5, 5), np.uint8)
            # tmp = cv2.bitwise_not(tmp)
            tmp = cv2.erode(tmp,  kernel, iterations=2)
            # tmp = cv2.morphologyEx(tmp, cv2.MORPH_OPEN, kernel)
            # tmp = cv2.bitwise_not(tmp)

            for i in range(5):
    
                answer = 0
                max_num = 0
                ques_num = (i+5*n + 1 + block*30-1)
                for j in range(4):
                    
                    
                    scoring_region = tmp[   i*50 : i*50 + 50 , 120 + j*60:  120+ j*65 + 65]
                    cv2.rectangle(tmp,(120 + j*65  ,   i*50 ),   ( 120+ j*65 + 65  ,  i*50 + 50),    (0, 0, 0), 1)
                    # cv2.rectangle(region,(120 + j*65  ,  i*50 ),   ( 120+ j*65 + 65  , i*50 + 50),   (0, 0, 0), 1)
    
                    number_of_black_pix = np.sum(scoring_region ==  0) 
                    max_black = 60*50

                    if number_of_black_pix > max_num and number_of_black_pix > 0.5 * max_black and answer != 0:
                        # max_num = number_of_black_pix
                        answer = 0
                        break


                    if number_of_black_pix > max_num and number_of_black_pix > 0.5 * max_black and answer == 0:
                        max_num = number_of_black_pix
                        answer = j+1
                        break

                answer_list.append(answer)

                if answer != answer_key[i+5*n + 1 + block*30-1]:
                    
                    coor_draw = answer_key[ques_num] -1
                    false_list.append(ques_num)
                    offset_visualize.append(offset_y)
                    coor_false_visualize.append(coor_draw)
                    
        
                else: 
                
                    correct_list.append(ques_num)
            
            
    for n, false in enumerate (false_list):
        
        false +=1 
        offset_draw_x = offset_fullform_x[(false-1)//30]
        offset_draw_y = offset_region_list[((false-1) - (false-1)//30 * 30)//5]
        coor = coor_false_visualize[n]
        i = ((false-1) - 30* block ) %5
        j = coor
        # cv2.rectangle(full_form,(offset_draw_x + 120 + j*65  , offset_draw_y + 757 + i*50 ),   ( offset_draw_x + 120+ j*65 + 65  , offset_draw_y + 757 + i*50 + 50),   (0, 0, 0), 1)
        cv2.circle(full_form,( offset_draw_x +  120 + j*65 + 32, offset_draw_y + 757 +    i*50 + 25),  20, (255, 0, 0),3)         

    for n in range (len(correct_list)):
        # print(correct)
        # ques_num = correct_list [n]
        ques_num = correct_list [n] + 1
        offset_draw_x = offset_fullform_x[(ques_num-1)//30]
        offset_draw_y = offset_region_list[((ques_num-1) - (ques_num-1)//30 * 30)//5]
        answer = answer_key[ques_num-1] 
        i = ((ques_num-1) - 30* block ) %5
        j = answer -1 
        # cv2.rectangle(full_form,(offset_draw_x + 120 + j*65  , offset_draw_y + 757 + i*50 ),   ( offset_draw_x + 120+ j*65 + 65  , offset_draw_y + 757 + i*50 + 50),   (0, 0, 0), 1)
        cv2.circle(full_form,( offset_draw_x +  120 + j*65 + 32, offset_draw_y + 757 +    i*50 + 25),  20, (0, 255, 0),3) 

    score = len(correct_list) / 50
    return score, full_form
