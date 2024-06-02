import cv2
import socket
import pickle
import struct
import time
from Moter import motor_left,motor_right,motor_stop,motor_go,motor_back
from threading import Thread
import RPi.GPIO as GPIO
import asyncio

X_KP = 0.5
X_KI = 0.3
X_KD = 0.16
cumError=0
rateError =0
lastError=0.0
previousTime =0

# SEN_KP = 0.1
# SEN_KI = 0.06
# SEN_KD = 0.032
SEN_KP = 0.5
SEN_KI = 0.3
SEN_KD = 0.16
sen_cumError=0
sen_rateError =0
sen_lastError=0.0
sen_previousTime =0

class Client:
    def __init__(self,client_socket):
        self.IP = '192.168.100.91'
        self.PORT = 4999
        self.distance=0
        self.cen_x=0
        self.sensor_list=[]
        self.client_socket=client_socket
        self.size=struct.calcsize("f")
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.TRIG=14
        self.ECHO=15
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.TRIG,GPIO.OUT)
        GPIO.setup(self.ECHO,GPIO.IN)
        self.sensor_Thread = Thread(target=self.sensor)
        self.sensor_Thread.daemon=True
        self.sensor_Thread.start()
        self.connection(self.client_socket,self.IP,self.PORT)
        
        #sensor

        
    def connection(self,client_socket,ip,port):
        client_socket.connect((ip, port))
        print("Connect success")
        self.frame()
        
        
    def frame(self):
        while True:
            try:
                ret,frame = self.cap.read()
                ret,frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                frame = pickle.dumps(frame)
                self.client_socket.sendall(struct.pack(">L", len(frame))+frame)
                time.sleep(0.001)
                cen_x = self.client_socket.recv(self.size)
                cen_x = struct.unpack(">f", cen_x)[0]
                print(cen_x)
                error_val = cen_x-320
                error = self.get_PID(error_val)
                print("Camera Optinizer : ",error_val,"Camera pid : ",error)
                # print(error)
                # print(error_val)
                # self.run()
                if error_val<-41:
                    motor_left(min(abs(error),100))
                elif error_val>41:
                    motor_right(min(abs(error),100))
                elif error_val == 0.0:
                    motor_stop()
                elif error_val>=-40 and error_val<=40:
                    if cen_x!=320.0:
                        error_sensor= min(self.sensor_list)-100
                        sensor_pid = self.get_sensor_pid(error_sensor)
                        print("Sensor : ",error_sensor,"Sensor pid : ",sensor_pid)
                        if sensor_pid>11:
                            motor_go(min(abs(sensor_pid),100))
                        elif sensor_pid<-11:
                            motor_back(min(abs(sensor_pid),100))
                        elif sensor_pid>=-10 and sensor_pid<=10:
                            motor_stop()
                        else:
                            continue
                        pass
                    else:
                        motor_stop()
                else:
                    motor_stop()
                
            except ConnectionResetError:
                print("Exception")
                motor_stop()
                return
            except Exception as e:
                print(e)
                time.sleep(0.1)
            
    def get_PID(self,error):
        global cumError,rateError,lastError,previousTime,X_KP,X_KI,X_KD
        elapsedTime=time.time()-previousTime
        cumError = error*elapsedTime
        rateError = (error-lastError)/elapsedTime
        pid= self.get_P(error,X_KP)+self.get_I(cumError,X_KI)+self.get_D(rateError,X_KD)
        lastError = error
        previousTime = time.time()
        return pid
    
    def get_sensor_pid(self,error_sensor):
        global sen_cumError,sen_rateError,sen_lastError,sen_previousTime,SEN_KP,SEN_KI,SEN_KD
        elapsedTime=time.time()-sen_previousTime
        sen_cumError = error_sensor*elapsedTime
        sen_rateError = (error_sensor-lastError)/elapsedTime
        pid= self.get_P(error_sensor,SEN_KP)+self.get_I(sen_cumError,SEN_KI)+self.get_D(sen_rateError,SEN_KD)
        sen_lastError = error_sensor
        sen_previousTime = time.time()
        return pid
    
    def get_P(self,error,kp):
        return kp*error
    def get_I(self,cumError,ki):
        return ki*cumError
    def get_D(self,rateError,kd):
        return kd*rateError
    
    #sensor
    def sensor(self):
        while True:
            try:
                GPIO.output(self.TRIG,True)
                time.sleep(0.00001)
                GPIO.output(self.TRIG,False)
                while GPIO.input(self.ECHO)==0:
                    start = time.time()
                while GPIO.input(self.ECHO)==1:
                    stop = time.time()
                check_time = stop-start
                self.distance =check_time*34300/2
                time.sleep(0.04)
                if self.distance<200:
                    if len(self.sensor_list)<4:
                        self.sensor_list.append(self.distance)
                    else:
                        self.sensor_list.pop(0)
                        self.sensor_list.append(self.distance)
                    print(self.sensor_list)
                
            except:
                pass
            # print(self.distance)
            
def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client = Client(client_socket)
    except Exception as e:
        print(e)
        motor_stop()
main()