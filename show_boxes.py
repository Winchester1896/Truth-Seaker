"""
Show bounding boxes (with class names)

Given:
    (1) A directory containing image files that have been processed
        to identify classes (ground truths)
    (2) A file with the classification names
    (3) A file with the groun tryth infomation
         "file name" x_min y_min x_max y_max classification_number
Dislay: Imge files with labled boundiung boxes 

"""
import PIL
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import math
import numpy as np

root = Tk()
root.title("Image shower")
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

##   Get data file
def get_data_file():
        ## Get data file
        print ('Please browse for data.txt file')
        data_file = get_file_name('Select file containing data')
        return data_file.name

## Get classifications
def get_classifications():    
    print ('Please browse for file with classifications: ')
    classifications = []
    classifications_file = get_file_name('Select file containing classifications')
    with open(classifications_file.name) as f:
        for line_1 in f:
            classifications.append(line_1)
    return classifications

## get Image files
def get_image_files():
    data_file_name = get_data_file()
    base_files = []
    all_boxes = []
    all_classification_numbers = []
    working_strings = []

    with open(data_file_name,'r') as odf:
        for line in odf:
            working_string = line
            working_strings.append(line)
            ## parse line
            x = working_string.split(' ')
            n_boxes = 0
            base_file = x[0]
            base_files.append(base_file)
        return [base_files, working_strings]

def get_boxes(line_1):
    x = line_1.split(' ')
    n_boxes = 0
    n_boxes = int((len(x)-1)/5)
    #print ('n_boxes',n_boxes
    #all_boxes = []
    boxes = []
    classification_numbers = []
    
    if n_boxes  > 0:       
        for box in range(n_boxes):
            #print ('box',box)
            try:

                x_min = int(x[5*box + 1])
                x_max = int(x[5*box + 3])

                y_min = int(x[5*box + 2])
                y_max = int(x[5*box + 4])

                this_box = (x_min,y_min,x_max,y_max)
                boxes.append(this_box)
                #print('this_box',this_box)
                this_classification_number = int(x[5*box + 5])
                classification_numbers.append(this_classification_number)
                #classification_name = classifications[classification_number]               
            except:
                pass
        #all_boxes.append(boxes)
        #all_classification_numbers.append(classification_numbers)
    #print('all_boxes',all_boxes)
    return boxes,classification_numbers
class Image_show(Frame):
    
    def __init__(self,master):
        Frame.__init__(self,master=None)

        frame = ttk.Frame(self, borderwidth=5, relief="sunken", width=500, height=500)
        self.namelbl = ttk.Label(self, text="Classification:")
        self.class_name = ttk.Entry(self)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=1)
        
        ##
        ## Define variables
        self.onevar = BooleanVar()
        self.twovar = BooleanVar()
        ##
        self.classificationvar = StringVar()
        ##
        self.onevar.set(False)
        self.twovar.set(False)
        
        ## Define Widgits
        #self.options checkboxes (not used at this tome)
        self.one = ttk.Checkbutton(self, text="Option One", variable=self.onevar, onvalue=True)
        self.two = ttk.Checkbutton(self, text="Option Two", variable=self.twovar, onvalue=True)
        ##
        ## Classification combobox
        self.classification = ttk.Combobox(self, textvariable=self.classificationvar)
        
        ## Get classification names
        self.valid_classes = get_classifications()

        self.classification['value'] = self.valid_classes
        self.classification.bind('<<ComboboxSelected>>', self.on_clasification)
        self.classificationvar.set(self.valid_classes[0])
        self.classification.set(self.classificationvar.get())
     
        self.cancel = ttk.Button(self, text="Cancel",command = self.on_cancel) #retunss without saving line
        self.apply = ttk.Button(self, text="Apply",command = self.on_apply) #adds  a bb,value to line
        self.next = ttk.Button(self, text="Next",command = self.on_next) # returns line after processing this image
        self.bind('a', self.on_apply)
        self.bind('c', self.on_cancel)
        self.bind('f', self.on_next)

        self.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), pady = 15,padx=5)
        
        self.x = self.y = 0
        self.canvas = Canvas(self, cursor="cross",width = 500,height =500)

        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(column=0, row=0, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
        self.sbarv.grid(row=0,column=2,stick=N+S)
        self.sbarh.grid(row=2,column=0,columnspan = 2, sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        ### add kestroke reply
        self.canvas.bind('a', self.on_apply)
        self.canvas.bind('c', self.on_cancel)
        self.canvas.bind('f', self.on_next)

        ### Define grid and format and place place widgets
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), pady = 15,padx=5)

        ##
        self.one.grid(column=0, row=3)
        self.two.grid(column=1, row=3)
        self.cancel.grid(column=2, row=3)
        self.apply.grid(column=3, row=3)
        self.next.grid(column=4, row=3)
        ##


        self.rect = None

        self.start_x = None
        self.start_y = None

        self.clasificationvar = StringVar()
        self.curX = 0
        self.curY = 0

        self.line = ""

        self.image_index = 0
        self.out_file_name = ""
        self.image_files_directory = ""
        self.image_files = ""

        self.classification.grid(column=3, row=0, columnspan=2, sticky=(N, E, W), pady=35, padx=5)

        ## Get list of image files to process
        (self.image_files, self.working_strings) = get_image_files()
        #print (self.image_files)

        self.image_index = 0
        #self.line = self.image_files_directory + '/' + self.image_files[0]

        self.im = PIL.Image.open(self.image_files[self.image_index])
        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.imgpane = self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
        #draw rectangles
        self.all_boxes,classification_numbers = get_boxes(self.working_strings[self.image_index])
        
        n_boxes = len(self.all_boxes)
        print('n_boxes', n_boxes)
        for i in range(n_boxes):
            print('self.all_boxes',self.all_boxes[i])
        if n_boxes > 0:
            for i in range(n_boxes):
                try:
                    (x_min,y_min,x_max,y_max) = self.all_boxes[i]
                    print('x_min',x_min,'y_min',y_min,'x_max',x_max,'y_max',y_max)
                    self.canvas.create_rectangle(x_min,y_min,x_max,y_max,
                                 outline='green',width = 2.0, tags = 'class 1')
                except:
                    pass

        ### (2) Get output file directory name
        print ('Please select dirctory for output file: ')
        self.out_file_directory = get_directory_name('Select output file directory: ')
        self.out_file_name = self.out_file_directory + '/dataset.text'



    def on_cancel(self, _event = None):
        self.canvas.delete("all")
        self.line = self.image_files_directory + '/' + self.image_files[self.image_index]
        tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.image = tk_im  # line added to fix bug in canvas widget
        self.canvas.create_image(0,0,anchor="nw",image=tk_im,tag = 'current_image')
        print(self.line)

    def on_apply(self, _event=None):
        self.canvas.create_rectangle(self.start_x, self.start_y, self.curX, self.curY,
                                     outline='green',width = 2.0, tags = 'class 1')
        self.line = self.line + ' ' + str(int(self.start_x)) + ' ' + str(int(self.start_y))
        self.line = self.line + ' ' + str(int(self.curX)) + ' ' + str(int(self.curY))
        self.line = self.line + ' ' + str(self.classification.current())
        print (self.line)


    def on_next(self,_event=None):
        self.image_index += 1
        if  self.image_index < len(self.image_files):
            self.line = self.image_files[self.image_index]
            self.line = self.line.replace("\n","")
            print(self.line)
            #create new canvas
            self.canvas.delete("all")
            self.im = PIL.Image.open(self.line)
            tk_im = ImageTk.PhotoImage(self.im)
            self.canvas.image = tk_im  # line added to fix bug in canvas widget
            self.canvas.create_image(0,0,anchor="nw",image=tk_im,tag = 'current_image')
            #draw rectangles
            self.all_boxes,classification_numbers = get_boxes(self.working_strings[self.image_index])
            
            n_boxes = len(self.all_boxes)
            print('n_boxes', n_boxes)
##            for i in range(n_boxes):
##                print('self.all_boxes',self.all_boxes[i])
            if n_boxes > 0:
                for i in range(n_boxes):
                    try:
                        (x_min,y_min,x_max,y_max) = self.all_boxes[i]
                        #print('x_min',x_min,'y_min',y_min,'x_max',x_max,'y_max',y_max)
                        self.canvas.create_rectangle(x_min,y_min,x_max,y_max,
                                     outline='green',width = 2.0, tags = 'class 1')
                        c_number = classification_numbers[i]
                        label_1 = self.valid_classes[c_number]
                        self.canvas.create_text((x_min+x_max)/2,(y_min+y_max)/2,
                                                text=label_1,fill='red',width = int(.8*(x_max-x_min)))
        
                        print ('label_1',label_1)
                    except:
                        pass
            print('current image position',self.canvas.coords('current_image'))
            
    def on_clasification(self,event):
        print (self.clasificationvar.get())

    def on_button_press( self,event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # deletge old test rectangle and creat new one 
        self.canvas.delete('test_rec')
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red',tag = 'test_rec')

    def on_move_press(self,event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units') 
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units') 
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)    

    def on_button_release(self,event):
        pass        
        
def main():
     root = Tk()
     root.title('data splitter')
     show_images = Image_show(root)
     show_images.pack()
     root.mainloop()
main()
    
