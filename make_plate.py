
import cv2
import os
import numpy as np
import random
import string
import argparse
import shutil


def gen_images(mode,image_scale,image_dir,image_list,num_images,image_format):

    # make destination directory
    if (os.path.isdir(image_dir)):
        try:
            shutil.rmtree(image_dir)
        except OSError as e:
            print("Error: %s : %s" % (image_dir, e.strerror))
        
    os.makedirs(image_dir)
    
    # create file for list of images & labels
    f = open(os.path.join(image_dir, image_list), 'w')
    
    # source directories
    letters = 'letters_300'
    numbers = 'numbers_300'
    borders = 'borders_500'
    years = 'year_cropped'
    provs = 'prov_cropped'
    
    # Italian plates don't use these letters
    unused = ['i','o','u','q']


    for i in range(num_images):

        # first whitespace
        plate=np.empty(shape=(300,34,3),dtype=np.uint8)
        plate.fill(255)

        label=""

        # first 2 letters
        for i in range(2):

            # avoid unused letters
            for j in range(0,9999):
                letter = random.choice(string.ascii_lowercase)
                if not(letter in unused):
                    break

            label = ''.join((label,letter))

            image = cv2.imread(os.path.join(letters,letter+'.jpg'))
            plate = np.concatenate((plate,image),axis=1)
            plate = cv2.copyMakeBorder(plate,0,0,0,34,cv2.BORDER_CONSTANT,value=[255,255,255])

        # blank space
        plate = cv2.copyMakeBorder(plate,0,0,0,120,cv2.BORDER_CONSTANT,value=[255,255,255])

        # 3 numbers
        for i in range(3):
            irand = random.randrange(0, 10)
            image = cv2.imread(os.path.join(numbers,str(irand)+'.jpg'))
            plate = np.concatenate((plate,image),axis=1)
            plate = cv2.copyMakeBorder(plate,0,0,0,34,cv2.BORDER_CONSTANT,value=[255,255,255])
            label = ''.join((label,str(irand)))

        # last 2 letters
        for i in range(2):

            # avoid unused letters
            for j in range(0,9999):
                letter = random.choice(string.ascii_lowercase)
                if not(letter in unused):
                    break

            image = cv2.imread(os.path.join(letters,letter+'.jpg'))
            plate = np.concatenate((plate,image),axis=1)

            plate = cv2.copyMakeBorder(plate,0,0,0,34,cv2.BORDER_CONSTANT,value=[255,255,255])
            label = ''.join((label,letter))

        # white padding - top & bottom of numbers/letters
        plate = cv2.copyMakeBorder(plate,100,100,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])

        # blue left border
        left = cv2.imread(os.path.join(borders,'left.jpg'))
        plate = np.concatenate((left,plate),axis=1)

        # blue right border (year & Province)
        year = random.randrange(15, 21)
        image_yr = cv2.imread(os.path.join(years,str(year)+'.jpg'))

        prov_list = os.listdir(provs)
        prov = random.randrange(0, len(prov_list))
        image_prov = cv2.imread(os.path.join(provs,prov_list[prov]))

        right = np.concatenate((image_yr,image_prov),axis=0)
        plate = np.concatenate((plate,right),axis=1)

        # resize
        plate = cv2.resize(plate,( int(1860*(image_scale/100)), int(500*(image_scale/100)) ), interpolation = cv2.INTER_LINEAR)

        height,width = plate.shape[:2]

        # estimate a size for black border
        border = height//25

        plate = cv2.copyMakeBorder(plate,border,border,border,border,cv2.BORDER_CONSTANT,value=[0,0,0])

        if mode=='mono':
            plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(os.path.join(image_dir,label.upper()+'.'+image_format),plate)

        f.write(label.upper()+'.'+image_format+'\n')

    f.close()


    return







# only used if script is run as 'main' from command line
def main():
  # construct the argument parser and parse the arguments
  ap = argparse.ArgumentParser()
  ap.add_argument('-m', '--mode',
                  type=str,
                  default='color',
                  choices=['mono','color'],
                  help='Save in color or monochrome. Default is color')  
  ap.add_argument('-s', '--image_scale',
                  type=int,
                  default=100,
                  help='Image scaling percent. Default is 100.')  
  ap.add_argument('-dir', '--image_dir',
                  type=str,
                  default='image_dir',
                  help='Path to folder for saving images and images list file. Default is image_dir')  
  ap.add_argument('-li', '--image_list',
                  type=str,
                  default='image_list.txt',
                  help='Name of images list file. Default is image_list.txt')  
  ap.add_argument('-f', '--image_format',
                  type=str,
                  default='png',
                  choices=['png','jpg','bmp'],
                  help='Image file format - valid choices are png, jpg, bmp. Default is png')  
  ap.add_argument('-n', '--num_images',
                  type=int,
                  default=1,
                  help='Number of images to generate. Default is 1')
  
  args = ap.parse_args()  
  
  print ('Command line options:')
  print (' --mode         : ', args.mode)
  print (' --image_scale  : ', args.image_scale)
  print (' --image_dir    : ', args.image_dir)
  print (' --image_list   : ', args.image_list)
  print (' --image_format : ', args.image_format)
  print (' --num_images   : ', args.num_images)


  gen_images(args.mode, args.image_scale, args.image_dir, args.image_list, args.num_images, args.image_format)


if __name__ == '__main__':
  main()


