import cv2

def main():
	capture = cv2.VideoCapture(0)

	while 1:
		has_frame, img = capture.read()
		small_img = cv2.flip(cv2.resize(img, (640, 360)), 1)
		
		cv2.imshow('detection', small_img)
		key = cv2.waitKey(30) & 0xff

		if key == 27:
			break
	capture.release()
	cv2.destroyAllWindows()
if __name__ == "__main__":
	main()