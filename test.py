import cv2

# open test.mp4 file using video capture
cap = cv2.VideoCapture('test.mp4')
# check if the file is opened and show it on the screen
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
