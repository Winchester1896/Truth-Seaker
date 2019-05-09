import PIL
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import math

root = None
maxSamples = 250

def get_directory_name(caption):
    dirname = filedialog.askdirectory(parent=root,initialdir="/",title=caption)
    if len(dirname ) > 0:
        print (' You chose %s' % dirname)
    return dirname

def get_file_name(caption):
    file = filedialog.askopenfile(parent=root,mode='rb',title=caption)
    if file != None:
        data = file.read()
    #file.close()
    print (' I got %d bytes from this file.' % len(data))
    return file

def save_file_name(caption):
    myFormats = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]
    fileName = filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title=caption)
    if len(fileName ) > 0:
        print ('Now saving under %s"' % nomFichier)
    return fileName

def createImage(imgFile):
    img = Image.open(imgFile)
    x,y = [random.randint(1333,2566), random.randint(1000,1900)]
    img = img.crop((x,y,x+100,y+100))
    return img

class Image_splitter():

    def __init__(self):

        self.tile_size = 1000
        self.rotation_angle = 90.0
        
##    def get_in_directory(self):
##        # Get directory containing images to split
        print ('Please select directory containing image files: ')
        self.input_files_directory = get_directory_name('Select directory containing image files:')
        
        # Ges directory to hold split images
##    def get_out_directory(self):
        print ('Please select dirctory to contain processed image files: ')
        self.out_file_directory = get_directory_name('Select processed file directory: ')

    def split(self):
        #loop on input files
        for file_name in os.listdir(self.input_files_directory):
            base_image_name = self.input_files_directory + '/' + file_name
            base_image = PIL.Image.open(base_image_name)
            (W,H) = base_image.size
            size = W,H
            if self.rotation_angle != 0:
                size = H,W
                base_image = base_image.rotate(self.rotation_angle,expand=1).resize(size)
                print ('size',size,W,H)

            exif_data = base_image.info['exif']   
            #loop on tiles
##            I_tiles = math.ceil(H/self.tile_size)
##            J_tiles = math.ceil(W/self.tile_size)
            for i in range (0,W,self.tile_size):
                i_start = i
                i_stop = (i_start + self.tile_size)
                if i_stop > W:
                    i_stop = W
                for j in range(0,H,self.tile_size):
                    j_start = j
                    j_stop = (j_start + self.tile_size)
                    if j_stop > H:
                        j_stop = H
                    cropped_image = base_image.crop((j_start,i_start,j_stop,i_stop))
                    cropped_image_name = self.out_file_directory + '/' + file_name[0:len(file_name)-4]
                    cropped_image_name = cropped_image_name + '_' + str(j) + '_' + str(i) + '.JPG'
                    print('cropped_image_name',cropped_image_name)
                    cropped_image.save(cropped_image_name,exif=exif_data)
                    #cropped_image.save(cropped_image_name,exif=exif_data)

def main():
     root = Tk()
     root.title('splitter')
     splitter = Image_splitter()
     splitter.split()
     
main()

