import cv2
import queue
import time
import threading
import detect
import sys
q=queue.Queue()

def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.105:8554/unicast")
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)



def Display():
    print("Start Displaying")
    while True:
        if q.empty() !=True:
            frame=q.get()
            if frame is not None:
                idxs, boxes, classIDs, confidences = detect.detect(frame)
                frame = detect.draw_frame(idxs, boxes, classIDs, confidences, frame)
                cv2.imshow("frame1", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()

if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    threads = [p1, p2]
    p1.start()
    p2.start()
    p1.join(p2)

