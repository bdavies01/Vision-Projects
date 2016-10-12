import cv2
import numpy as np

def main() :
	capture = cv2.VideoCapture(0);
	capture.set(15, -5)
	cv2.namedWindow("its just a stream, bro", cv2.WINDOW_NORMAL)
	while True:
		ret, img = capture.read()
		cv2.imshow("its just a stream, bro", cv2.resize(cv2.flip(img, 1), (640, 480)))
		k = cv2.waitKey(30) & 0xff

		if k == 27:
			break
	capture.release()
	cv2.destroyAllWindows()
if __name__ == '__main__':
	main()