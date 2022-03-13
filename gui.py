from pickle import TRUE
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
import cv2
from cv2 import CAP_DSHOW
import face_recognition
import os
from datetime import datetime
import argparse
import csv
import numpy


class Application:
    def __init__(self, output_path = "./"):
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0,CAP_DSHOW) # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera

        self.root = tk.Tk()  # initialize root window
        self.root.title("Facial Recognition Entry System")  # set window title
        self.root.geometry('1250x750')
        self.root.resizable(False,False)

        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        self.panel = tk.Label(self.root, height= 350, width= 450)  # initialize image panel
        self.panel.place(x=100, y = 170)

        message = tk.Label(self.root, text="INDIAN INSTITUTE OF TECHNOLOGY ROORKEE", fg="black", width=50, height=2,
                   font=('Times New Roman', 28, 'bold underline'))
        message.place(x=80, y=15)  

        message = tk.Label(self.root, text="STUDENT ENTRY/EXIT PORTAL", fg="blue", width=40, height=1,
                   font=('Times New Roman', 20, 'bold underline'))
        message.place(x=280, y=95)

        lbl = tk.Label(self.root, text="Enter Enrollment Number:", fg="black", width=20, height=1,
                   font=('Times New Roman', 18, 'bold'))
        lbl.place(x=600, y=180)

        self.txt = tk.Entry(self.root, width=13, bg="white", fg="blue", font=('Times New Roman', 18, 'bold'))
        self.txt.place(x=900, y=180)

        myFont = font.Font(size=20)
        myFont2 = font.Font(size=16)

        # create a button, that when pressed, will take the current frame and save it to file
        btn = tk.Button(self.root , width = 28, bg= 'blue', fg='white', text="Snapshot", command=self.facerecog)
        btn.place(x= 100, y = 545)

        btn1 = tk.Button(self.root, width = 12, bg= 'green', fg='white', text = 'IN', command=self.hello)
        btn2 = tk.Button(self.root, width = 12, bg= 'red', fg='white', text = 'OUT', command=self.goodbye)

        btn1.place(x = 100, y = 620)
        btn2.place(x = 355, y = 620)

        btn3 = tk.Button(self.root, width = 8, bg= 'yellow', fg='black', text = 'ENTER', command=self.inp)
        btn3.place(x = 1080, y = 170)

        btn['font'] = myFont
        btn1['font'] = myFont
        btn2['font'] = myFont
        btn3['font'] = myFont2

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        self.video_loop()


    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds
    

    def facerecog(self):
        cam = cv2.VideoCapture(0,CAP_DSHOW)
        img_counter=0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if True:
       
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
                break
        cam.release()
        imgElon = face_recognition.load_image_file('opencv_frame_0.png')
        imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
        imgTest = face_recognition.load_image_file("ImagesBasic/"+str(self.txt.get()) + '.jpg')
        imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
 
        faceLoc = face_recognition.face_locations(imgElon)[0]
        encodeElon = face_recognition.face_encodings(imgElon)[0]
        cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
 
        faceLocTest = face_recognition.face_locations(imgTest)[0]
        encodeTest = face_recognition.face_encodings(imgTest)[0]
        cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
 
        results = face_recognition.compare_faces([encodeElon],encodeTest)
        faceDis = face_recognition.face_distance([encodeElon],encodeTest)
        print(results,faceDis)
        cv2.putText(imgTest,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

        if (results==[True]):
            lbl8 = tk.Label(self.root, text="Photo Matches", fg="red", font=('Times New Roman', 16))
            lbl8.place(x=620, y=500)
        else:
            lbl8 = tk.Label(self.root, text="Photo Does Not Match", fg="red", font=('Times New Roman', 16))
            lbl8.place(x=620, y=500)
        
        cv2.destroyAllWindows()

    def take_snapshot(self):
        """ Take snapshot and save it to the file """
        ts = datetime.now() # grab the current timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        self.current_image.save(p, "JPEG")  # save image as jpeg file
        im = Image.open(argparse.file_path)
        im = im.convert("RGBA")
        im.save(argparse.hidpi_path, argparse.FileType, quality=95)
        print("[INFO] saved {}".format(filename))

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

    def inp(self):
        inp = self.txt.get()
        print(inp)

        result = numpy.array(list(csv.reader(open("details.csv", "rt"), delimiter=","))).astype("str")
        i=1
        for i in range(len(result)):
            if result[i][0] == str(self.txt.get()):
                name = result[i][1]
                dept = result[i][2]
                year = result[i][3]
                dob = result[i][4]
                phone = result[i][5]
            
        lbl1 = tk.Label(self.root, text=name, fg="black", font=('Times New Roman', 22))
        lbl1.place(x=870, y=250)

        lbl2 = tk.Label(self.root, text=dept, fg="black", font=('Times New Roman', 18))
        lbl2.place(x=870, y=300)

        lbl7 = tk.Label(self.root, text=year, fg="black", font=('Times New Roman', 16))
        lbl7.place(x=870, y=350)

        lbl3 = tk.Label(self.root, text="D.O.B", fg="black", font=('Times New Roman', 16))
        lbl3.place(x=870, y=400)

        lbl4 = tk.Label(self.root, text="Mobile no", fg="black", font=('Times New Roman', 16))
        lbl4.place(x=870, y=450)

        lbl5 = tk.Label(self.root, text=dob, fg="black", font=('Times New Roman', 16))
        lbl5.place(x=980, y=400)

        lbl6 = tk.Label(self.root, text=phone, fg="black", font=('Times New Roman', 16))
        lbl6.place(x=980, y=450)

        image = Image.open("ImagesBasic\\"+str(self.txt.get())+".jpg")
        image = image.resize((210, 240), Image.ANTIALIAS)
        global photo
        photo = ImageTk.PhotoImage(image)        
        photopanel = tk.Label(self.root, height= 240, width= 210, borderwidth=1, relief="solid", image=photo)  # initialize image panel
        photopanel.place(x=620, y = 250)
        
    def hello(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lbl9 = tk.Label(self.root, text=f"Your last IN time is: {current_time}", fg="brown", font=('Times New Roman', 14))
        lbl9.place(x=620, y=560)
        lbl10 = tk.Label(self.root, text="Your last OUT time was:", fg="brown", font=('Times New Roman', 14))
        lbl10.place(x=620, y=600)
        #lbl11 = tk.Label(self.root, text="Returned to campus after: ", fg="brown", font=('Times New Roman', 14))
        #lbl11.place(x=620, y=640)

    def goodbye(self):
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        lbl9 = tk.Label(self.root, text="                                                   ", fg="brown", font=('Times New Roman', 14))
        lbl9.place(x=620, y=560)
        lbl10 = tk.Label(self.root, text=f"Your last OUT time is:   {current_time}", fg="brown", font=('Times New Roman', 14))
        lbl10.place(x=620, y=600)
        lbl11 = tk.Label(self.root, text="                                                  ", fg="brown", font=('Times New Roman', 14))
        lbl11.place(x=620, y=640)
             

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
print("[INFO] starting...")
pba = Application(args["output"])
pba.root.mainloop()
