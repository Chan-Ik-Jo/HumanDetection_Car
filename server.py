import socket
import struct
import pickle
import cv2
from ultralytics import YOLO
from collections import deque
from threading import Thread
from deep_sort_realtime.deepsort_tracker import DeepSort
import os
import time
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class Server:
    def __init__(self):
        self.ip = '192.168.100.91'
        self.port = 4999
        self.model = YOLO("yolov8n.pt")
        self.decode_frame=None
        self.tracker = DeepSort(max_age=10)
        self.threadFrame=None
        self.frame=None
        
        self.serverbind()
        
    def serverbind(self):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((self.ip,self.port))
        self.server_socket.listen(1)
        print('Client Listening..' )
        self.client_socket, address = self.server_socket.accept()
        print("Connect Success",address)

        if self.threadFrame is None:
            self.threadFrame = Thread(target=self.recvFrame)
            self.threadFrame.daemon=True
            self.threadFrame.start()
        self.recvImage()
    
    def recvImage(self):
        while True:
            if self.frame is not None:
                self.decode_frame = cv2.imdecode(self.frame,cv2.IMREAD_COLOR)
                detection = self.model.predict(source=[self.decode_frame],save=False)[0]
                results = []
                
                for data in detection.boxes.data.tolist():
                    confidence = float(data[4])
                    classid = int(data[5])
                    if confidence<0.6 and classid!=0:
                        continue
                    xmin,ymin,xmax,ymax=int(data[0]), int(data[1]), int(data[2]), int(data[3])
                    label =int(data[5])
                    if label==0:
                        results.append([[xmin,ymin,xmax-xmin,ymax-ymin],confidence,label])
                tracks = self.tracker.update_tracks(results,frame=self.decode_frame)
                
                if len(tracks) != 0:
                    track_id = tracks[0].track_id
                    ltrb = tracks[0].to_ltrb()
                    xmin, ymin, xmax, ymax = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
                    center_x = (xmin+xmax)/2
                    self.direction(center_x)

                    cv2.rectangle(self.decode_frame,(xmin,ymin),(xmax,ymax),(0,255,0),2)
                    cv2.circle(self.decode_frame,(320,240),10,(255, 0, 0),1,cv2.LINE_4)
                    cv2.putText(self.decode_frame, str(track_id), (xmin+5, ymin-8), cv2.FONT_ITALIC, 1, (255,255,255), 2)
                else:
                    self.direction(320)
                cv2.imshow('Frame',self.decode_frame)
                key=cv2.waitKey(1)&0xFF
                if key == ord("q"):
                    break
    
    def serverClose(self):            
        self.client_socket.close()
        self.server_socket.close()
        cv2.destroyAllWindows()
        print('exit')
        
    def recvFrame(self):
        data_size = struct.calcsize("L")
        data_buffer = b""
        while True:
            try:   
                if self.client_socket is not None:
                    while len(data_buffer) < data_size:
                        # DATA RESOPONSE
                        data_buffer += self.client_socket.recv(4096)
                    packed_data_size = data_buffer[:data_size]
                    data_buffer = data_buffer[data_size:]
                    frame_size = struct.unpack(">L", packed_data_size)[0]
                    while len(data_buffer) < frame_size:
                        # DATA REPONSE
                        data_buffer += self.client_socket.recv(4096)
                    frame_data = data_buffer[:frame_size]
                    data_buffer = data_buffer[frame_size:]
                    print("수신 프레임 크기 : {} bytes".format(frame_size))
                    self.frame = pickle.loads(frame_data)     
                    pass
                
            except Exception as error:
                print(error)
                
    def direction(self,x):
        x = struct.pack(">f",x)
        self.client_socket.sendall(x)
        pass      
def main():
    server = Server()
     
main()
