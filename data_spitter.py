"""
split data file into sub-files
given: file with data files
read data file and split int multiple lines
(1) get data file name
(2) get size of split
(3) loop on lines in data file
    (a) read file name
    (b) build sublines
    (c) loop on items
        calculate sub boxes
        add sub boxes to sub_lines
    (d) write sub-lines
"""
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
    file.close()
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


class Data_splitter():

    def __init__(self):
        
        self.tile_size = 200
        self.rotation_angle = 90.0

        self.lines = []
        self.line_number = 0

        ## Get data file
        print ('Please browse for data.txt file')
        self.data_file = get_file_name('Select file containing data')

        ## Get directory to hold revised data.txt file
        print ('Please browse for directory to contain revise dat.txt file: ')
        self.save_directory = get_directory_name('Select output directory')
        self.save_file = self.save_directory + '/data.txt'

    def split_data(self):
        with open(self.data_file.name,'r') as odf:
            self.old_name = 'smaller_images'
            self.new_name = 'images_200X200'
            self.line_offset = 0
            for line in odf:
                self.working_string = line
                ## parse line
                self.x = self.working_string.split(' ')
                self.n_boxes = 0
                base_file = self.x[0]
                base_file_directory  = base_file
                base_file_name = base_file.split('/')
                base_file_name = base_file_name[len(base_file_name)-1]
                #print('base_file_name',base_file_name)
                base_file_directory = base_file_directory.strip(base_file_name)
                root_file_name = base_file_name.split('_')
                file_type = root_file_name[len(root_file_name)-1]
                file_type = file_type.split('.')
                self.file_type = '.' + file_type[len(file_type)-1] 
                working_file_name = base_file_name.replace(self.file_type,"")
                #print('first_cut working_file_name',working_file_name)
                start_points = working_file_name.split('_')
                start_point_x = start_points[len(start_points)-2]
                start_point_y = start_points[len(start_points)-1]
                mask_out = '_' + start_point_x + '_' + start_point_y
                #print('mask_out',mask_out)
                working_file_name = working_file_name.replace(mask_out,"")
                #print('working_file_name',working_file_name)
                working_file = base_file_directory.replace(self.old_name,self.new_name)
                working_file = working_file + working_file_name
                #print ('working_file',working_file)
                try:
                    self.start_x = int(start_point_x)
                    self.start_y = int(start_point_y)
                    #print('self.start_x',self.start_x,'self.start_y',self.start_y)
                except:
                    self.start_x = 0
                    self.start_y = 0

                #print ('\n',working_file)
                #print ('self.start_x ',self.start_x,' self.start_y ',self.start_y)
##
##                for k in range (1,len(root_file_name)-2):
##                    working_file = working_file + '_' + str(root_file_name[k])
##                working_file.replace('smaller_images','images_200X200')
                #print ('Working File ',working_file)
                try:
                    ## read base file
                    base_image = PIL.Image.open(base_file)
                    (W,H) = base_image.size
                    base_image.close()
                    #print ('W',W,'H',H)
                    self.n_j = math.ceil(W/self.tile_size)
                    self.n_i = math.ceil(H/self.tile_size)
                    
                    #print('self.n_j ',self.n_j,' self.n_i ',self.n_i)

                    ## loop on j
                    for i in range(0,W,self.tile_size):
                        ## Loop on i
                        for j in range(0,H,self.tile_size):
                            title_i_j = working_file + '_' + str(self.start_x+j) + '_' + str(self.start_y+i) + '.JPG'
                            #print('title_i_j',title_i_j)
                            self.lines.append(title_i_j)

                    self.n_boxes = int((len(self.x)-1)/5)
                    #print ('n_boxes =', self.n_boxes)                                              
                except:
                    pass
                #print (self.lines)
                # Loop on boxes
                for box in range(self.n_boxes):
                    #print ('box',box)
                    try:
                        # These values are in reference frame of the large image
                        x_min = int(self.x[5*box + 1])
                        x_max = int(self.x[5*box + 3])
                        x_center = (x_min + x_max)/2.0
                        #print ('x_min',x_min)

                        y_min = int(self.x[5*box + 2])
                        y_max = int(self.x[5*box + 4])
                        y_center = (y_min + y_max)/2.0

                        classification_1 = int(self.x[5*box + 5])

                        bb_area = (x_max-x_min)*(y_max-y_min) # cs invariant

                        try:
                            j_center = int(int(x_center)/int(self.tile_size))
                        except:
                            j_center = 0

                        try:
                            i_center = int(int(y_center)/int(self.tile_size))
                        except:
                            i_center = 0
                        
                        #print (' j_center ',j_center, ' i_center ',i_center)
                        # thanslate to local cs
                        x_min_local = x_min - j_center*self.tile_size
                        x_max_local = x_max - j_center*self.tile_size
                        y_min_local = y_min - i_center*self.tile_size
                        y_max_local = y_max - i_center*self.tile_size

                        # trim to cell boundray
                        x_min_local = max(0,x_min_local)
                        x_max_local = min(x_max_local,self.tile_size)
                        y_min_local = max(0,y_min_local)
                        y_max_local = min(y_max_local,self.tile_size)

##                        print ('x_min ',x_min,'x_max ',x_max,'\n',
##                               'y_min ',y_min, 'y_max',y_max)
##                        
##                        print ('x_min_local ',x_min_local,'x_max_local ',x_max_local,'\n',
##                              'y_min_local ',y_min_local, 'y_max_local',y_max_local) 

                        bb_area_local = (x_max_local-x_min_local)*(y_max_local-y_min_local)
                        IOU = 0.
                        if bb_area != 0.:
                            IOU = bb_area_local/bb_area
                            #print ('bb_area ',bb_area,' bb_area_local ',bb_area_local,'IOU ',IOU)

                        self.line_number = self.n_j*i_center +j_center + self.line_offset
                        #print('j_center',j_center,' i_center ',i_center,'line number ', self.line_number)
                        # only consider cases where IOU is greater than 75%
                        if IOU > 0.0:#0.75:

                            #print('j_center',j_center,' i_center ',i_center, self.line_number)
                            self.lines[self.line_number] = self.lines[self.line_number] + ' ' + str(x_min_local)
                            self.lines[self.line_number] = self.lines[self.line_number] + ' ' + str(y_min_local)
                            self.lines[self.line_number] = self.lines[self.line_number] + ' ' + str(x_max_local)
                            self.lines[self.line_number] = self.lines[self.line_number] + ' ' + str(y_max_local)
                            self.lines[self.line_number] = self.lines[self.line_number] + ' ' + str(classification_1)
                    except:
                        pass #print('IOU', IOU) ##pass
                #print ('self.line_offset',self.line_offset)
                self.line_offset += self.n_i*self.n_j


        ## write lines to data file
        with open(self.save_file,'a+') as dsf:
            for line_s in self.lines:
                line_s = line_s + '\n'
                #print (line_s)
                #dsf = open(self.save_file,'a+')
                dsf.write(line_s)
        dsf.close()

        print('n_lines',len(self.lines))
        
def main():
     root = Tk()
     root.title('data splitter')
     splitter = Data_splitter()
     splitter.split_data()
     
main()
    
