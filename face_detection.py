import cv2
import numpy as np
import time

face_cascade = cv2.CascadeClassifier('C:/Users/Bert/Downloads/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('C:/Users/Bert/Downloads/opencv/sources/data/haarcascades/haarcascade_eye.xml')

capture = cv2.VideoCapture(0)

showEyes = False

def drawDisplacement(flipped_img, x, y, w, h, fps):
	face_center_x = (x + x + w) / 2
	face_center_y = (y + y + h) / 2
	displacement_x = 319 - face_center_x
	displacement_y = 239 - face_center_y
	text = "<%d, %d>" % (displacement_x, displacement_y)
	cv2.putText(flipped_img, "%s" % text, (2, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
	cv2.putText(flipped_img, "FPS: %s" % fps, (592, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0))

def main():
	initial_time = time.time()
	total_frames = 0
	times = [time.time()]

	cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)
	while True:

		ret, img = capture.read()

		total_frames += 1
		times.append(time.time())

		if len(times) > 10:
			times.pop(0)

		fps = int(1.0 / (times[-1] - times[-2]))

		flipped_img = cv2.flip(cv2.resize(img, (640, 480)), 1)
		gray = cv2.cvtColor(flipped_img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.05, 10)
		cv2.rectangle(flipped_img, (0, 0), (100, 48), (255, 255, 255), 2)
		cv2.rectangle(flipped_img, (590, 0), (638, 40), (255, 255, 255), 2)

		for(x, y, w, h,) in faces:
			cv2.rectangle(flipped_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
			drawDisplacement(flipped_img, x, y, w, h, fps)

			if showEyes:
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = flipped_img[y:y+h, x:x+w]
				eyes = eye_cascade.detectMultiScale(roi_gray, 1.05, 7)

				for(ex, ey, ew, eh) in eyes:
					cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

		cv2.imshow('Face Detection', cv2.resize(flipped_img, (640, 480)))

		k = cv2.waitKey(30) & 0xff

		if k == 27:
			break

	capture.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()