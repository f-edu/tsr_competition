#https://pymotw.com/3/socket/tcp.html
# string example: 00/1500/90
import socket
import cv2 as cv
import time

def send_cmd(cmd):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the CarControl is listening
    # server_address = ('localhost', 1081)
    server_address = ('172.24.1.1', 1080)
    sock.connect(server_address)
    try:
        # Send data
        message = cmd.encode()
        print(cmd)
        sock.sendall(message)
    finally:
        print('closing socket')
        sock.close()

State=0 # 0-stop noreleased   1-FerstSpeed    2-SecondSpeed    3-ThirdSpeed   4-BackSpeed
Acceleration=0 # 0-Off   1-On
speed=1500
StartTime=0   #Время начала ускорения
SpedGain=0  #Прирост скорости
speedState=[1500,1600,1650,1700,1400]
angle=90
DEFAULT_CMD = '11/1500/90'
joystick = cv.imread("joystick.jpg")
cv.imshow("loystick",joystick)
while True:

    key = cv.waitKey(25)# подобрать время нужно

    if key == ord('q'):
        send_cmd(DEFAULT_CMD)
        break

    if key == ord('1'):
        Acceleration = 0
        State=1
        speed = speedState[State]
        pass
    if key == ord('2'):
        Acceleration = 0
        State = 2
        speed = speedState[State]
        pass
    if key == ord('3'):
        Acceleration = 0
        State = 3
        speed = speedState[State]
        pass
    if key == ord('4'):
        Acceleration = 0
        State = 4
        speed = speedState[State]
        pass

    if State==4:
        if key == ord('w'):
            speed = speedState[0]
            pass
        if key == ord('s'):
            speed = speedState[4]
            pass

    if State<4:
        if key == ord('w'):
            if Acceleration==0:
                speed = speedState[State]
                Acceleration=1
                StartTime=time.time()
                pass
            else:
                spedGain=(time.time()-StartTime)*0.07 #Тут нужно подобрать в зависимости от единиц в которых вернётся время, сейчас на миллисекунды расчитано
                if spedGain>100:
                    spedGain=100
                sped=speedState[State]+spedGain
                pass

        if key == ord('s'):
            Acceleration = 0
            speed=speedState[0]
            pass

    if key == ord('a'):
        Acceleration = 0
        angle = angle + 5
        pass
    if key == ord('d'):
        Acceleration = 0
        angle = angle - 5
        pass
    if key == ord(' '):
        Acceleration = 0
        speed = 1500
        pass
    if key == ord('f'):
        Acceleration = 0
        angle = 90
        pass

    if key == -1:
        Acceleration=0
        sped=speedState[State]
        pass

send_cmd('00/'+str(speed)+'/'+str(angle))