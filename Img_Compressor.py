# Import Modules
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime
import os
import scipy as sc

origTotalSize = 0
compTotalSize = 0
rootLabels = []


#getRoot
def getRoot(): 
    global root
    # create root window
    root = Tk()
    # root window title and dimension
    root.title("Image Compressor - Developed using Python [Badri Naraayanan]")  
    # Set geometry(widthxheight)
    root.geometry('950x450')


def sel():
   global isFolder
   selection = str(option.get())
   print(selection)
   if(selection=="1"):
     isFolder = True
   else:
     isFolder = False
    
def showOptions():
    #root = Tk()
    global option
    option = IntVar()
    R1 = Radiobutton(root, text="Folder", variable=option, value=1, command=sel)
    R1.grid(column = 1, row = 1, sticky='w', padx=5)
    R2 = Radiobutton(root, text="File", variable=option, value=2, command=sel)
    R2.grid(column = 1, row = 0, sticky='w',padx=5)
    #root.mainloop()

#get time stamp
def getCurrentTimeStamp():
    now = datetime.now()
    timestamp = now.strftime("%d_%m_%Y_%H_%M_%S")
    return timestamp

#creates output directory, if it doesn't exist and returns the path
def createOutputDir(user):
    timeStamp = getCurrentTimeStamp()
    #print("date and time:",date_time)
    OUTPUT_PATH = "C:\\Users\\"+user+"\\Downloads\\COMPRESSION\\"+timeStamp+"\\"
    CHECK_FOLDER = os.path.isdir(OUTPUT_PATH)
    if not CHECK_FOLDER:
        os.makedirs(OUTPUT_PATH)
    return OUTPUT_PATH    

#saves image object in the given path with given name and extension and compression percentage
def compressAndSaveFile(img, path, name, extension, compression):
    OUTPUT_STR = path + name+"-compressed.jpeg"
                   
    img.save(OUTPUT_STR,
                 extension,
                 optimize = True,
                 quality = compression)

    

#displays given text as label in given grid position(rowind, colind)
def displayLabel(text, rowInd, colInd):
    lbl = Label(root, text ="\n"+text, anchor="w", justify="left",font=("Arial", 12))
    lbl.grid(column = colInd, row = rowInd, sticky='w')
    root.update()
    global rootLabels
    rootLabels.append(lbl)

#gets size of a given file in a given format [MB - MegaBytes, KB - KiloBytes, anything else - Bytes]
def getFileSize(filePath, sizeFormat):
    file_size = os.path.getsize(filePath)
    if(sizeFormat == "MB"):
        #MegaBytes
        file_size = round(file_size/(1024*1024),2)
    elif(sizeFormat=="KB"):
        #KiloBytes
        file_size = round(file_size/(1024),2)
    else:
        #bytes
        file_size = file_size
    return file_size

def resetLabels():
    global rootLabels
    for label in rootLabels:
        label.after(50, label.destroy())
    rootLabels = []    


def isPNG(fileName):
    split_tup = os.path.splitext(fileName)

    # extract the file name and extension
    file_name = split_tup[0]
    file_extension = split_tup[1]

    if(str(file_extension)=='.PNG' or str(file_extension)=='.png'):
        return True
    else:
        return False
    
#compresses a given file and saves it in disk
def compress(imgPath, OUTPUT_PATH, index, count):
    global origTotalSize
    global compTotalSize
    resetLabels()
    displayLabel("SOURCE: "+imgPath,3,1)
    image = Image.open(imgPath)
    
    x = imgPath.split("/")
    filename = (x[-1])
    #print("before outputstr= stmt"+filename)

    displayLabel("Compressing File ["+str(index+1)+"/"+str(count)+"]: " + filename,12,1)
    orig_file_size = getFileSize(imgPath, "MB")
    displayLabel("Original Size : "+ str(orig_file_size) + " MB",13,1)

    #removing alpha for PNG image
    if(isPNG(filename)):
        image = image.convert('RGB')
    
    compressAndSaveFile(image, OUTPUT_PATH , filename , "JPEG", 50)

    OUTPUT_STR = OUTPUT_PATH + filename +"-compressed.jpeg"
    compressed_file_size = getFileSize(OUTPUT_STR,"MB")
    compTotalSize = compTotalSize + compressed_file_size

    txtFileSize = "Compressed Size: " + str(compressed_file_size)+" MB"
    displayLabel(txtFileSize,14,1)

    origTotalSize = origTotalSize + orig_file_size
    if(orig_file_size != 0):
        percent_reduced = (orig_file_size-compressed_file_size)*100/orig_file_size
    else:
        percent_reduced = 0
    txtPercentReduced = "Compression: "+str(round(percent_reduced,2))+" %"
    displayLabel(txtPercentReduced,16,1)
    txtFileSaved = "File saved: " + OUTPUT_STR
    displayLabel(txtFileSaved,18,1)
    #resetLabels()    
    #open_popup(win)
 
    return

#fetches all the images in a given folder
def getImgFiles(folder):
  # specify the img directory path
    path = folder

    # list files in img directory
    files = os.listdir(path)
    
    imgFiles = []
    for file in files:
        #print(file)
    # make sure file is an image
        if file.endswith(('.jpg', '.png', 'jpeg', '.JPG', '.JPEG','.PNG','.bmp','.BMP')):
            #print("inside if")
            img_path = path + file
            imgFiles.append(path+"/"+file)

    return imgFiles

def handleFolderOption():
    global origTotalSize
    global compTotalSize

    dir = filedialog.askdirectory()
    START_TIME = datetime.now()


    displayLabel("SOURCE FOLDER: "+dir,3,1)
    imgFiles = getImgFiles(dir)
    fileCount = len(imgFiles)
    user = os.getlogin()
    OUTPUT_PATH = createOutputDir(user)
    numFiles = len(imgFiles)
    if(not numFiles == 0):
        for ind in range(numFiles):
            #displayLabel("Source Folder: "+dir, 3, 1)
            compress(imgFiles[ind],OUTPUT_PATH,ind,numFiles)

        origTotalSize = round(origTotalSize,2)
        compTotalSize = round(compTotalSize,2)
        resetLabels()
        displayLabel("Source Folder: "+dir, 3, 1)
        displayLabel("Destination Folder [Compressed Files]: "+OUTPUT_PATH, 20, 1)
        displayLabel(str(len(imgFiles))+" Files compressed from a total of " + str(origTotalSize) + " MB to " + str(compTotalSize) + " MB" ,21,1)
        totalPercentReduced = (origTotalSize-compTotalSize)*100/origTotalSize
        txtTotalPercent = str(round(totalPercentReduced,2))
        displayLabel("Compression Achieved(%): " + txtTotalPercent + " %" ,22,1)
        END_TIME = datetime.now()
        TOTAL_TIME = END_TIME -START_TIME
        #TOTAL_TIME=TOTAL_TIME.replace(microsecond=0)
        displayLabel("Total Time Taken: " + str(TOTAL_TIME), 25, 1)
    else:
        open_popup(root)

def display_image(file_path):
##        image = sc.misc.imread(file_path)
##        #with Image.open(file_path) as image:  
##        photo = ImageTk.PhotoImage(image)
##        image_label = tk.Label(root)
##        image_label.grid(column = 1, row = 3, sticky='w')
##        image_label.config(image=photo)
##        image_label.photo = photo

 
        print(file_path)
##        img = ImageTk.PhotoImage(Image.open(file_path))
##        image_label = Label(root)
##        image_label.grid(column = 1, row = 3, sticky='w')
##        image_label.config(image=img)
##        #image_label.photo = img

        img = ImageTk.PhotoImage(file=file_path)
        image_label = Label(root)
        image_label.grid(column=1, row=3, sticky = 'w')
        image_label.photo = img
##        b2 =Button(root,image=img) # using Button 
##        b2.grid(row=3,column=1)
        root.update()
    
def handleFileOption():
    types = [('images', '*.PNG *.JPG *.JPEG *.BMP *.png *.jpg *.jpeg *.bmp')]
##        ('JPG', '*.JPG'),
##        ('BMP', '*.BMP'),
##        ('JPEG', '*.JPEG'),
##        ('png', '*.png'),
##        ('jpg', '*.jpg'),
##        ('bmp', '*.bmp'),
##        ('jpeg', '*.jpeg')
    
    # show the open file dialog
    f = filedialog.askopenfilename(filetypes=types)
    START_TIME = datetime.now()
    displayLabel("SOURCE: "+f,3,1)
    user = os.getlogin()
    OUTPUT_PATH = createOutputDir(user)
    index=0
    count=1
    compress(f, OUTPUT_PATH, index, count)
    END_TIME = datetime.now()
    TOTAL_TIME = END_TIME -START_TIME
    #TOTAL_TIME=TOTAL_TIME.replace(microsecond=0)
    displayLabel("Total Time Taken: " + str(TOTAL_TIME), 25, 1)
    #display_image(f)

   # filename = filedialog.askopenfilename(filetypes=f_types)
    #img = ImageTk.PhotoImage(file=filename)




#click event handler for "Browse" button
def clicked():

    
    resetLabels()
    if(isFolder):
        handleFolderOption()
    else:
        handleFileOption()
    
    
    
def reset():
    #label.after(1000, label.destroy())
    for item in root.pack_slaves():
        print(item)
        print(type(item))
        #item.do_stuff()

#opens new popup window
def open_popup(win):   
   top= Toplevel(win)
   top.geometry("300x300")
   top.title("Image Compression")
   Label(top, text= "No Files Found!", font=('Mistral 18 bold')).place(x=150,y=80)

#Application Window Logic Begins
getRoot()
#global lineFrame

lineFrame = Frame(root, highlightbackground="blue", highlightthickness=2)
lineFrame.grid(column=1, row=2,sticky='w')
showOptions()

# button widget with red color text inside
btn = Button(root, text = "Browse" ,fg = "red", command=clicked, font=("Arial", 12))
# Set Button Grid
btn.grid(column=1, row=2, sticky='w', padx=5)
 
# Execute Tkinter
root.mainloop()

