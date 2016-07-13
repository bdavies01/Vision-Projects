import cv2
import numpy as np
import time

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

def detect_color(img, box):
	h = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 0])
	s = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 1])
	v = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 2])
	return (h,s,v)

def main():
	a = 313 #upper left coords
	b = 147
	ab = (a, b)
	c = 327 #lower right coords
	d = 167
	cd = (c, d)
	while True:
		ret, img = capture.read()
		if not ret:
			time.sleep(0.08)
			continue
		hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		flipped_img = cv2.flip(hsv_img, 1)
		cv2.rectangle(flipped_img, ab, cd, (0, 100, 255), 3) #it uses bgr lol
		cv2.imshow('HSV detect', flipped_img)
		h, s, v = detect_color(flipped_img, (ab, cd))

		print "H value: %f" % h
		print "S value: %f" % s
		print "V value: %f" % v

		key = cv2.waitKey(30) & 0xff
		if key == 27:
			break

	capture.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()