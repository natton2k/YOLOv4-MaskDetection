import detect
import cv2
import time
import cascade
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
i = 0
#c = cascade.get_cascade()
while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) == ord('x'):
        start = time.time()
        idxs, boxes, classIDs, confidences = detect.detect(frame)
        #frame = detect.draw_frame(idxs, boxes, classIDs, confidences, frame)
        print(detect.output_info(idxs, boxes, classIDs, confidences))
        #frame = cascade.detect_face(frame, c)

        end = time.time()
        print(end-start)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
