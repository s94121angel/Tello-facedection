

import cv2
import numpy as np
import threading
import face_recognition
from djitellopy import Tello
import time


starCounter = 1

myDrone =Tello()
myDrone.connect()
myDrone.for_back = 0
myDrone.left_right_velocity = 0
myDrone.up_down_velocity = 0
myDrone.yaw_velocity = 0
myDrone.speed = 0
print(myDrone.get_battery())
myDrone.streamoff()
myDrone.streamon()


frameWidth = 640
frameHeight = 480
scale = 0.8

'''影像偵測'''
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a third sample picture and learn how to recognize it.
trump_image = face_recognition.load_image_file("trump.jpg")
trump_face_encoding = face_recognition.face_encodings(trump_image)[0]

# Load a thourth sample picture and learn how to recognize it.
michelle_image = face_recognition.load_image_file("michelle.jpg")
michelle_face_encoding = face_recognition.face_encodings(michelle_image)[0]

# Load a fifth sample picture and learn how to recognize it.
lala_image = face_recognition.load_image_file("lala.jpg") 
lala_face_encoding = face_recognition.face_encodings(lala_image)[0]

pig_image = face_recognition.load_image_file("pig.jpg") 
pig_face_encoding = face_recognition.face_encodings(pig_image)[0]

Jian_image = face_recognition.load_image_file("Jian.jpg") 
Jian_face_encoding = face_recognition.face_encodings(Jian_image)[0]
#
hong_image = face_recognition.load_image_file("hong.jpg")
hong_face_encoding = face_recognition.face_encodings(hong_image)[0]



# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    trump_face_encoding,
    michelle_face_encoding,
    lala_face_encoding,
    hong_face_encoding,
]
known_face_names = [
   "Barack Obama",
    "Joe Biden",
    "Donald Trump",
    "Michelle Obama",
    "tung",
    "PIG",
    "Jian",
    "Hong"
    
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def display(img):
    #cv2.line(影像, 開始座標, 結束座標, 顏色, 線條寬度)
    cv2.line(img,(int(frameWidth*2/3),0),(int(frameWidth*2/3),frameHeight),(0,255,255),3)
    cv2.line(img,(int(frameWidth/3),0),(int(frameWidth/3),frameHeight),(0,255,255),3)
    cv2.line(img,(0,int(frameHeight/3)),(frameWidth,int(frameHeight/3)),(0,255,255),3)
    cv2.line(img,(0,int(frameHeight*2/3)),(frameWidth,int(frameHeight*2/3)),(0,255,255),3)
'''
myDrone.takeoff()
time.sleep(5)
myDrone.rotate_clockwise(90)
time.sleep(5)
myDrone.land()



''' 
cap = cv2.VideoCapture(0)
direction = 0
wid = 0
frame_read = myDrone. get_frame_read()
myDrone.takeoff()
def imageshow():
    global direction
    global wid
    while True:
      
            #success, image = cap.read()
            frame_read = myDrone. get_frame_read()
            image = frame_read.frame
               
            imgResize = cv2.resize(image,(frameWidth,frameHeight))
            
            display(imgResize)
            #facedetection(imgResize)
               
              
            
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(imgResize, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
            
                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]
            
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
            
                    face_names.append(name)
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
            
                # Draw a box around the face
                cv2.rectangle(imgResize, (left, top), (right, bottom), (0, 0, 255), 2)
                cx = (right-left)/2+left
                cy = bottom-top/2+top
                str_cx = str(cx)
                str_cy = str(cy)
                #location control
                if (cx<int(frameWidth/3)):
                    cv2.putText(imgResize, "Go Right", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),3)
                    direction = 1
                    
                elif(cx>int(frameWidth*2/3)):
                    cv2.putText(imgResize, "Go left", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),3)
                    direction = 2
                    
                elif(cy<int(245)):
                    cv2.putText(imgResize, "Go up", (20,80), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),3)
                    direction = 3
                    
                elif(cy>int(520)):
                    cv2.putText(imgResize, "Go down", (20,80), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),3)
                    direction =4
                else:
                    direction = 0
                    
                # Draw a label with a name below the face
                cv2.rectangle(imgResize, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(imgResize, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                #cv2.putText(imgResize,"("+str_cx+","+str_cy+")",(right, bottom),font, 0.5, (255, 255, 255), 1)
                wid = int(right-left)
                
                
                
            cv2.imshow("StackedImages",imgResize)  
            if cv2.waitKey(1) & 0xFF == ord('q'):
                myDrone.land()
                break

def tellocontrol():
    
    while True:
        if direction == 1:
            
           if wid <=144:
               myDrone.move_left(20) 
               myDrone.move_forward(20)
               myDrone.rotate_clockwise(1)
           elif wid >230:
               myDrone.move_left(20) 
               myDrone.move_back(20)
               myDrone.rotate_clockwise(1)
           else:
              
                myDrone.move_left(20)                
                myDrone.rotate_clockwise(1)
         
           #print("相機往右飛")  
        elif direction == 2:
            
            if wid <=144:
                myDrone.move_right(20) 
                myDrone.move_forward(20)
                myDrone.rotate_counter_clockwise(1)
            elif wid >230:
                 myDrone.move_right(20) 
                 myDrone.move_back(20)  
                 myDrone.rotate_counter_clockwise(1)
            else:
                
                myDrone.move_right(20)          
                myDrone.rotate_counter_clockwise(1)
            #print("相機往左飛")  
        elif direction == 3:
            myDrone.move_up(20) 
            #print("相機往上飛")  
            
        elif direction == 4:
            myDrone.move_down(20) 
            #print("相機往下飛")
        #else:
             #print("STAY")

def handcontrol():
    function=''    
    while True:
        function=input("請輸入欲執行之功能：")
        #battery=drone.Battery()
       
        if function=='1':
            myDrone.move_up(20)
            
        elif function=='2':
            myDrone.move_down(20)
              
        elif function=='3':
            myDrone.move_right(20) 
        elif function=='4':
            myDrone.move_left(20) 
        elif function=='5':
            myDrone.move_forward(20) 
        elif function =='6':
            myDrone.move_back(20)
        elif function =='7':
            myDrone.land()
            break
      
     
if __name__ == '__main__':
    t1 = threading.Thread(target=imageshow)
    t1.start()
    t2 = threading.Thread(target=tellocontrol)
    t2.start()
    t3 = threading.Thread(target=handcontrol)
    t3.start()
    t1.join()
    if t1.join:
        t2.stop()
        t3.stop()
        print("程式結束=====================")
   
