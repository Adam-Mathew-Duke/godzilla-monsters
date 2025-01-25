# Name: Image Processng
# Description: Crop images to a uniform size
# Author: Adam

'''
Usage: 

1. Place the images you wish to copy inside
   the folder in the root directory and name in input_images

2. The result will be saved to a folder called output_images

3. Works best for small dimension changes and if the monsters
   face is in the center of the image
'''

# PIP install PIL if not already installed
from PIL import Image
import os

# find the center of the image and crop to the desired size
def crop_and_save_images(input_dir, output_dir, target_size=(200, 200)):
 
    # create an output folder if it does not
    # already exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # look in the input directory
    for filename in os.listdir(input_dir):

        # look for image files
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
           
            # open the images in the input directory
            try:
                img_path = os.path.join(input_dir, filename)
                img = Image.open(img_path)

                # find the center of the image
                # and calculate the cropping
                original_width, original_height = img.size
                left = (original_width - target_size[0]) // 2
                top = (original_height - target_size[1]) // 2
                right = left + target_size[0]
                bottom = top + target_size[1]

                # crop the image
                cropped_img = img.crop((left, top, right, bottom))

                # save the cropped image
                output_path = os.path.join(output_dir, filename)
                cropped_img.save(output_path)

            # if the image cannot be opened
            except Exception as e:
                print(f"Error processing image {filename}: {e}")
                exit()

# directories
input_dir = "input_images/"
output_dir = "output_images/"

# image crop size
target_size = (200, 200)

# crop the iamge from the input directory
# save a copy of the cropped image to the output directory
crop_and_save_images(input_dir, output_dir, target_size)

# end of code
