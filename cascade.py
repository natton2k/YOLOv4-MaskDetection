import cv2

def get_cascade():
    config_path = cv2.data.haarcascades + '/haarcascade_frontalface_alt.xml';
    face_cascade = cv2.CascadeClassifier()
    # Load the cascade
    face_cascade.load(cv2.samples.findFile(config_path))
    return face_cascade

def detect_face(frame, cascade):
    faces = cascade.detectMultiScale(frame)
    for (x, y, w, h) in faces:
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, 1, 2)
    return frame


if __name__ == '__main__':
    frame = cv2.imread('images/friend.jpeg')
    frame = detect_face(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
