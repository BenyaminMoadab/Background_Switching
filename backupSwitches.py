import numpy as np
import cv2
import os
from PIL import Image
from matplotlib import cm
import numpy as np
# from PIL import Image
# import pixellib
# from pixellib.tune_bg import alter_bg
# import mediapipe as mp


def flipImageH(img): 
    # Do a flip of left and right Horizontally flipped Image

    hori_flippedImage = img.transpose(Image.FLIP_LEFT_RIGHT)
    return hori_flippedImage

def flipImageV(img): 
    # Show vertically flipped image
    Vert_flippedImage = img.transpose(Image.FLIP_TOP_BOTTOM)
    return Vert_flippedImage

def flipImageU(img): 
    # Show vertically flipped image
    Up_flippedImage = img.transpose(Image.FLIP_TOP_BOTTOM)
    return Up_flippedImage

#def rotateImage90(img): 
    #show 90 degree flipped image
 #   height , width, channel = np.array(img).shape
    
 #   degree_flippedImage = img.transpose(Image.ROTATE_90)
   
 #   return degree_flippedImage

def BackGroundReplacing( OriginalImage,ImageMask,bg_image):
# initialize mediapipe

    OriginalImage = np.array(OriginalImage)
    ImageMask = np.array(ImageMask)
    bg_image = np.array(bg_image)

    # resize the background image to the same size of the original frame
    height , width, channel = ImageMask.shape

    bg_image = cv2.resize(bg_image, (width, height))
    # combine frame and background image using the condition
    condition =  (ImageMask>200)
    output_image = np.where(condition, ImageMask, bg_image)
    condition =  (ImageMask<=200)
    
    #OriginalImage = cv2.cvtColor(OriginalImage, cv2.COLOR_GRAY2BGR)  # grayscale --> BGR

    print('condition.shape' , condition.shape)
    print('output_image.shape' , output_image.shape)
    print('OriginalImage.shape' , OriginalImage.shape)

    output_image = np.where(condition, output_image, OriginalImage)
 

    #cv2.imshow("Output", output_image)
    #cv2.imshow("Frame", ImageMask)
    output_image = Image.fromarray(output_image)


    return output_image
    key = cv2.waitKey(0)
    if key == ord('q'):
        return 
    

def load_images_from_folder(folder):
    images = []
    filenames =[]
    Cnt=0
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            filenames.append(os.path.splitext(filename)[0])
            Cnt=Cnt+1
            #if(Cnt>10):
            #    break
        
    return images,filenames

def resize2bg(img):
    new_image = img.resize((500, 500),refcheck=False)
    cv2.imwrite('/out/out.jpg', new_image)
    

def extractFileName(path):
    
    name = path.split('.')
    filename = name[1].split('/')
    print("my file name isss:",name[1])
    return filename[-1]

# imgs = load_images_from_folder('./img')
# bgs = load_images_from_folder('./bg')

# print(imgs[0].shape)
# print(bgs[0].shape)

# sample_bg = cv2.imread("./bg/wood.jpg")
# print(sample_bg.shape)

# sample_img = cv2.imread("./img/0.jpg")
# print(sample_img.shape)
# h, w, c = sample_img.shape
# new_bg = sample_bg.resize((w, h),refcheck=False)
# cv2.imwrite('./bg/bg.jpg', new_bg)

#switchBackgrounds('./img/0.png','./bg/wood.jpg',0)
#print("resized Done!")

path_color = './Dataset/color' #'./Dataset/color'
path_gt = './Dataset/GT' #'./Dataset/GT'
path_bg = './bg' #'./bg'

ImgOrgs,namesOrg = load_images_from_folder(path_color)   #path_color
ImgMasks,namesGT = load_images_from_folder(path_gt)      #path_gt
BackGrounds,namesBg = load_images_from_folder(path_bg)           #path_bg
#ImgOrgs,namesOrg = load_images_from_folder('F:\MRL\DataSet\All DataSet\ImageDataset_makan_100\Dac')

track = 0
print("length is :", len(ImgOrgs))
for pic in range(0,len(ImgOrgs)):
    ImgOrg = ImgOrgs[pic]
    ImgMask = ImgMasks[pic]
    cnt = 0
     
    
    for bg in range(0,len(BackGrounds)):
        if bg != 0:
            ImgOrg = BackGroundReplacing(ImgOrgs[pic],ImgMasks[pic],BackGrounds[bg])

        # cv2.imwrite('out_new/'+namesOrg[pic]+'_'+ str(bg) +'_'+ str(cnt) +'.jpg', ImgOrg)
        
        print('out_new/'+namesOrg[pic]+'_0_'+ str(bg) +'.jpg')
        ImgOrg.save('out_new/'+namesOrg[pic]+'_0_'+ str(bg) +'.jpg')
        ImgMask.save('gt_new/'+namesGT[pic]+'_0_'+ str(bg) +'.jpg')
        track += 1


        img = flipImageH(ImgOrg)
        ImgMaskH = flipImageH(ImgMask)
        print('out_new/'+namesOrg[pic]+'_1_'+ str(bg) +'.jpg')
        img.save('out_new/'+namesOrg[pic]+'_1_'+ str(bg) +'.jpg')
        ImgMaskH.save('gt_new/'+namesGT[pic]+'_1_'+ str(bg) +'.jpg')
        track += 1

        img = flipImageV(ImgOrg)
        ImgMaskV = flipImageV(ImgMask)
        print('out_new/'+namesOrg[pic]+'_2_'+ str(bg) +'.jpg')
        img.save('out_new/'+namesOrg[pic]+'_2_'+ str(bg) +'.jpg')
        ImgMaskV.save('gt_new/'+namesGT[pic]+'_2_'+ str(bg) +'.jpg')
        track += 1

        #img = rotateImage90(ImgOrg)
        #print('out_new/'+namesOrg[pic]+'_'+ str(bg) +'_'+ str(cnt+2) +'.jpg')
        #img.save('out_new/'+namesOrg[pic]+'_'+ str(bg) +'_'+ str(cnt+3) +'.jpg')
        #ImgMask.save('gt_new/'+namesGT[pic]+'_'+ str(bg) +'_'+ str(cnt+3) +'.jpg')

print("out image No." + str(track))  
# # J=4
# for J in range(0,3):
#     for method in range(0,2): #flipH, flipV, rotate
#         key = cv2.waitKey(0)

#         if(method == 0):
#             flipImageH(ImgOrgs[J])


#         img = BackGroundReplacing(ImgOrgs[J],ImgMasks[J],BackGrounds[2])
