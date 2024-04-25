import socket
import cv2
import numpy as np
from threading import Thread

IP_ROBOT = "192.168.1.6"
PORT = 6601
INDEX_CAMERA = 1
MIN_AREA = 6500

lower_red = np.array([0,81,154])
upper_red = np.array([15,184,255])

lower_blue = np.array([89,75,135])
upper_blue = np.array([179,255,255])

lower_green = np.array([40,50,75])
upper_green = np.array([99,255,255])

lower_yellow = np.array([10,66,149])
upper_yellow = np.array([31,170,255])

List_Colors = [(lower_red, upper_red),
               (lower_blue, upper_blue),
               (lower_green, upper_green),
               (lower_yellow, upper_yellow)]
str_color = ["Red", "Blue", "Green", "Yellow"]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (IP_ROBOT, PORT)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

cap = cv2.VideoCapture(INDEX_CAMERA)

class Mg400(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()
        sock.send(Robot_Active.encode())
    def run(self):
        global X_robot, Y_robot, R_robot, color , Robot_Active
        Robot_Active = "0"
        first_send = 0
        while True:
            if cap.isOpened():
                if Robot_Active == "1" and first_send == 0:
                    sock.send(Robot_Active.encode())
                    first_send = 1
                    print(Robot_Active)
                if first_send == 1:
                    data = sock.recv(50)
                    print("receive: " + str(data))
                    if data == b'pose_color':
                        print("Color NO: ",color,": ", str_color[idx_color])
                        point = str(X_robot) + "," + str(Y_robot) + "," + str(R_robot) + "," + str(color)
                        sock.send(point.encode())
                        print("R: " , R_robot)
                        print("Y: " , Y_robot)
                    elif data == b'finish':
                        Robot_Active = "0"
                        first_send = 0

Mg400()
while True:

    ret, frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if ret:
        roi = frame[10:450, 180:450]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        for idx_color, (low, high) in enumerate(List_Colors):
            mask = cv2.inRange(hsv, low, high)
            contours , _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                for i, c in enumerate(contours):
                    area = cv2.contourArea(c)
                    if area < MIN_AREA:
                        continue

                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    box = np.intp(box)

                    cv2.drawContours(roi, [box], 0, (221, 160, 221), 3)
                    
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.circle(roi, (cX, cY), 3, (50, 50, 50), -1)
                        cv2.putText(roi, str_color[idx_color], (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

                    if str_color[idx_color] == "Red":
                        color = 0
                    elif str_color[idx_color] == "Green":
                        color = 1
                    elif str_color[idx_color] == "Blue":
                        color = 2
                    elif str_color[idx_color] == "Yellow":
                        color = 3

                    angle = rect[2]
                    R_robot = round(-angle,2)
                    X = ( -1 * 0.204 * cY ) + 318.50
                    X_robot = round(X,2)


                    if R_robot <= 0.00 and R_robot >= -5.00:
                        Y_robot = 133.00

                    elif R_robot < -5.00 and R_robot >= -10.00:
                        Y_robot = 134.50

                    elif R_robot < -10.00 and R_robot >= -15.00:
                        Y_robot = 135.00

                    elif R_robot < -15.00 and R_robot >= -20.00:
                        Y_robot = 135.27 

                    elif R_robot < -20.00 and R_robot >= -25.00:
                        Y_robot = 134.20

                    elif R_robot < -25.00 and R_robot >= -30.00:
                        Y_robot = 132.59 

                    elif R_robot < -30.00 and R_robot >= -35.00:
                        Y_robot = 131.46 

                    elif R_robot < -35.00 and R_robot >= -40.00:
                        Y_robot = 130.62 

                    elif R_robot < -40.00 and R_robot >= -45.00:
                        Y_robot = 130.24 

                    elif R_robot < -45.00 and R_robot >= -50.00:
                        Y_robot = 130.39 

                    elif R_robot < -50.00 and R_robot >= -55.00:
                        Y_robot = 130.40 

                    elif R_robot < -55.00 and R_robot >= -60.00:
                        Y_robot = 129.92 

                    elif R_robot < -60.00 and R_robot >= -65.00:
                        Y_robot = 130.48 

                    elif R_robot < -65.00 and R_robot >= -70.00:
                        Y_robot = 131.06 

                    elif R_robot < -70.00 and R_robot >= -75.00:
                        Y_robot = 131.25 

                    elif R_robot < -75.00 and R_robot >= -80.00:
                        Y_robot = 131.90 

                    elif R_robot < -80.00 and R_robot >= -85.00:
                        Y_robot = 132.37

                    elif R_robot < -85.00 and R_robot >= -90.00:
                        Y_robot = 133.00

                    Robot_Active = str(1)
            else:
                Robot_Active = str(0)  
                      

        cv2.imshow("Frame", frame)
        cv2.imshow("Roi", roi)
       
cap.release()
cv2.destroyAllWindows()


