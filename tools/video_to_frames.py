import cv2

video_name = 'test.mp4'
cap = cv2.VideoCapture('video/' + video_name)


frame_id = 0

while cap.isOpened():

    ret, frame = cap.read()

    if frame_id > 2001:

        cv2.imwrite('images/dataset/'+ str(frame_id) + ".jpg", frame)
        # cv2.imshow("frame", frame)
    if frame_id > 2500:
        break
    frame_id += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()