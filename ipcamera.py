import cv2
import queue
import time
import threading
import os
import detect



q=queue.Queue()


def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.43.245:8554/unicast")
    ret, frame = cap.read()
    q.put(frame)
    while ret and p2.is_alive():
        ret, frame = cap.read()
        q.put(frame)
    cap.release()


def Display():
     print("Start Displaying")
     a = False
     while True:
        if q.empty() !=True:
            frame=q.get()
            if frame is not None:
                if a:
                    idxs, boxes, classIDs, confidences = detect.detect(frame)
                    frame2 = detect.draw_frame(idxs, boxes, classIDs, confidences, frame)
                    cv2.imshow("frame2", frame2)
                    a = False
                cv2.imshow("frame1", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) == ord('x'):
            a = True

p1 = threading.Thread(target=Receive)
p2 = threading.Thread(target=Display)

if __name__=='__main__':

    p1.start()
    p2.start()




