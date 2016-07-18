import cv2
import numpy as np
import time
import urllib2

stream = urllib2.urlopen("http://10.0.8.200/mjpg/video.mjpg")

def detect_color(img, box):
	h = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 0])
	s = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 1])
	v = np.mean(img[box[0][1]+3:box[1][1]-3, box[0][0]+3:box[1][0]-3, 2])
	return (h,s,v)

def main():
	bytes = ''
	a = 317 #upper left coords
	b = 257
	ab = (a, b)
	c = 327 #lower right coords
	d = 277
	cd = (c, d)
	while True:
		bytes += stream.read(1024)
		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')

		if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes= bytes[b+2:]
			img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
			hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			flipped_img = cv2.flip(hsv_img, 1)
			cv2.rectangle(img, ab, cd, (0, 100, 255), 3) #it uses bgr lol
			cv2.imshow('HSV detect', img)
			h, s, v = detect_color(flipped_img, (ab, cd))

			print "H value: %f" % h
			print "S value: %f" % s
			print "V value: %f" % v

			key = cv2.waitKey(30) & 0xff
			if key == 27:
				break

	cv2.destroyAllWindows()

if __name__ == "__main__":
		main()