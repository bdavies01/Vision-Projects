import cv2
import numpy as np 
import time
import urllib2

COLOR_MAX = np.array([20, 255, 110], np.uint8)

def main():
	capture = cv2.VideoCapture(0)
	capture.set(15, -5)
	h = 5
	s = 90
	v = 50
	while True:
		has_frame, img = capture.read()
		
		flipped_img = cv2.flip(img, 1) 
		COLOR_MIN = np.array([h, s, v], np.uint8)
		hsv_img = cv2.cvtColor(flipped_img, cv2.COLOR_BGR2HSV)
		frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
		cv2.imshow('tyr-vision', frame_threshed)
		key = cv2.waitKey(30) & 0xff #quit on pressing 'esc'
		if key == 27:
			break
		elif key == ord('w'):
			h += 1
		elif key == ord('s'):
			h -= 1
		elif key == ord('a'):
			s += 1
		elif key == ord('d'):
			s -= 1
		elif key == ord('1'):
			v -= 1
		elif key == ord('2'):
			v += 1
			
		print "H value: %d" % h 
		print "S value: %d" % s
		print "V value: %d" % v
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()