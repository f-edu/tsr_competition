import time
import numpy
import cv2
from PIL import Image

from PyV4L2Camera.camera import Camera
# from PyV4L2Camera.controls import ControlIDs

import os


def setup_camera():
    cam_id = '/dev/video1'  # type: str
    os.system('v4l2-ctl -d ' + cam_id + ' -c exposure_auto=1')
    time.sleep(0.5)
    camera = Camera(cam_id, 1280, 720)
    time.sleep(0.5)
    return camera

if __name__ == '__main__':

    camera = setup_camera()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (1280, 720))

    while True:
        last_time = time.time()
        frame = camera.get_frame()
        # Decode the imagecv/FastCameraCapture/main.py:27
        im = Image.frombytes('RGB', (camera.width, camera.height), frame, "raw", "BGR")
        # Convert the image to a numpy array
        cv_arr = numpy.asarray(im)
        # cv2.imshow("im", cv_arr)
        out.write(cv_arr)

        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    camera.close()
    cv2.destroyAllWindows()
