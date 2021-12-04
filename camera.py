import face_recognition
import cv2
import numpy as np
import pandas as pd
from datetime import date

import datetime

# import serial
# ser = serial.Serial('/dev/cu.usbmodem143101', 9600) # Establish the connection on a specific port


csv = pd.read_csv('CSV/criminals.csv')
df = pd.DataFrame(csv)

csv = pd.read_csv('CSV/citizen.csv')
df_citizen = pd.DataFrame(csv)

id_column = df.loc[:,'ID']
id_list = id_column.values

criminal_name = df.loc[:,'Name']
criminal_name_list = criminal_name.values

citizen_name = df.loc[:,'Name']
citizen_name_list = citizen_name.values


# ser = serial.Serial('COM3', 9600, timeout=0)

# img_counter = 0

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        

    def __del__(self):
        self.video.release()
    
    def get_frame(self,known_face_encodings,known_face_names):
        




        # ser.write(str.encode('b'))
        # Grab a single frame of video
        ret, frame = self.video.read()
        #frame = cv2.resize(frame,(0,0),None,0.25,0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video



        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                
                name = known_face_names[best_match_index]
             
                img_name = "image_log/opencv_frame_{}.png".format(name)
                cv2.imwrite(img_name, frame)
                # print("{} written!".format(name))
                # img_counter += 1
                
                # x = datetime.datetime.now()


            # print(name)
            # print(name)

            f = open("text_log/file.txt", "a")
            if (name in citizen_name_list) and (name in criminal_name_list):
                # ser.write(str.encode('a'))
                   
                  
                
                
                if name in criminal_name.values:
                    
                    f.write(name + " Criminal")
                    f.write(' ')
                    f.write(str(df.loc[df.Name == name, 'Reason'].values))
                    f.write(' ')
                    today = datetime.datetime.now()
                    today = str(today)
                    # print("Today date is: ", today)

                    f.write(today)

                    f.writelines('\n')

                    # ser.write(str.encode('c')) 

                    print(name, " Criminal + " , df.loc[df.Name == name, 'Reason'].values)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    pos = (10,70)
                    x,y = pos
                    cv2.rectangle(frame, pos,(x+1000,y-300),(0,0,0),-1)

                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 255, 255), 1)
                    cv2.putText(frame, str(df.loc[df.Name == name, 'Reason'].values), (10, 50), font, 2.0, (0, 0, 255), 2)
                
                
            if (name not in criminal_name_list) and (name != "Unknown"):
                # ser.write(str.encode('b'))
                print("Citizen ", name)
                # ser.write(str.encode('b'))
                # f = open("text_log/file.txt", "a")
                f.write(name + " Citizen")
                f.write(' ')
            
                today = datetime.datetime.now()
                today = str(today)
                # print("Today date is: ", today)
            
                f.write(today)
            
                f.writelines('\n')
                # f.close()
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)
                # ser.write(str.encode('c')) 


            elif(name == 'Unknown'):
                # f = open("text_log/file.txt", "a")
                f.write(name + " No Record")
                f.write(' ')
            
                today = datetime.datetime.now()
                today = str(today)
                # print("Today date is: ", today)
            
                f.write(today)
            
                f.writelines('\n')
                

 
                # ser.write(str.encode('d'))  
                print("unknown") 
                cv2.rectangle(frame, (left, top), (right, bottom), (200, 0, 0), 2)

            # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (200, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # ser.write(str.encode('c'))  
            
            f.close()



        
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
