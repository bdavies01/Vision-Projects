import cv2
import numpy as np
import urllib2
from networktables import NetworkTable

stream = urllib2.urlopen("http://10.0.8.3/mjpg/video.mjpg")
IP = "roborio-8-frc.local"
NetworkTable.setIPAddress(IP)
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("visiondata")

COLOR_MIN = np.array([40, 75, 130], np.uint8) #min and max hsv thresholds
COLOR_MAX = np.array([65, 254, 254], np.uint8)

def draw_HUD(img, x, y, angle):
	cv2.line(img, (x, y), (319, 239), (0, 255, 0), 2) #line from screen center to goal edge
	displacement_x = 319 - x
	displacement_y = 239 - y
	text = "<%d, %d>" % (displacement_x, displacement_y)
	cv2.putText(img, "%s" % text, (2, 35), cv2.FONT_HERSHEY_TRIPLEX, 1.2, (0, 255, 0)) #x and y displacement

def calcDistance(p1, p2):
	return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))

def calcAspectRatioInRange(d1, d2, minimum, maximum):
	return (d1/d2 > minimum) and (d1/d2 < maximum)

def getStartIndex(contour):
    biggest_dist = -1
    start_index = -1
    for i in range(0, len(contour)):
        dist = contour[i][0][0]**2 + contour[i][0][1]**2
        if dist > biggest_dist:
            biggest_dist = dist
            start_index = i

    return start_index

def get_nth_point(contour, n, start_index=-1):
    if start_index == -1:
        start_index = getStartIndex(contour)

    return contour[(start_index + n) % len(contour)][0]

def main():
	bytes = ' ' #bytestream from the camera
	last_approx = np.array([[319, 240], [319, 240], [319, 240], [319, 240], [319, 240], [319, 240], [319, 240], [319, 240]]).reshape((-1, 1, 2)).astype(np.int32)
		bytes += stream.read(1024) #read the bytes
		a = bytes.find('\xff\xd8')
		b = bytes.find('\xff\xd9')

		if a!=-1 and b!=-1:
			jpg = bytes[a:b+2]
			bytes= bytes[b+2:]
			img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1) #turn into image

			flipped_img = cv2.resize(img, (640, 480))
			hsv_img = cv2.cvtColor(flipped_img, cv2.COLOR_BGR2HSV) #convert image to HSV
			threshold = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX) #hsv threshold 

			areaArray = []
			contours, heirarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #find all contours in the image

			if len(contours) != 0: #put contours in an array
				for i, c in enumerate(contours):
					area = cv2.contourArea(c)
					areaArray.append(area)

				sortedData = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse = True) #sort array for biggest contour
				largestContour = sortedData[0][1]

				epsilon = 0.012 * cv2.arcLength(largestContour, True) 
				approx = cv2.approxPolyDP(largestContour, epsilon, True) #approvimate polygon from contour

				if len(approx) != 8: 
					approx = last_approx
				else:
					vertical = calcDistance(get_nth_point(approx, 0), get_nth_point(approx, 1))
					horizontal = calcDistance(get_nth_point(approx, 7), get_nth_point(approx, 0))
					if not calcAspectRatioInRange(vertical, horizontal, 0.64, 0.72):
						approx = last_approx

				last_approx = approx
				x = get_nth_point(approx, 1)[0]
				y = get_nth_point(approx, 1)[1]
				angle = np.rad2deg(np.arctan((x - 319.5) / 282.2047))
				draw_HUD(flipped_img, x, y, angle) #draw the hud on the flipped image
				cv2.drawContours(flipped_img, [approx], -1, (255, 150, 0), 2) #draw the contours on the flipped image

				table.putNumber("skewangle", angle)
				table.putNumber("xdisplacement", (319.5 - x))

				cv2.namedWindow('tyr-vision', cv2.WINDOW_NORMAL)
				cv2.imshow('tyr-vision', flipped_img) #create a window with the complete image
			else :
				angle = 0
				print 'Nothing found. '
				table.putNumber("skewangle", 100000) #values at 100,000 if nothing found
				table.putNumber("xdisplacement", 100000)
				draw_HUD(flipped_img, 319, 239, angle) #draw a hud with no contour detected 
				cv2.namedWindow('tyr-vision', cv2.WINDOW_NORMAL)
				cv2.imshow('tyr-vision', flipped_img)


			key = cv2.waitKey(30) & 0xff #press ESC to quit
			if key == 27:
				break
		else:
			bytes += stream.read(1024) #read the bytes
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
	cv2.destroyAllWindows()

if __name__ == '__main__':
		main()