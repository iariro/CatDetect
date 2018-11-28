import sys
import cv2
import numpy as np

def judgeContourIsCat(frame, contour, lowcontour, highcontour, lowcolor, highcolor):
	mu = cv2.moments(contour, False)
	try:
		x, y = int(mu["m10"] / mu["m00"]), int(mu["m01"] / mu["m00"])
		r, g, b = frame[y, x]
		judge = ''
		if lowcontour <= cv2.contourArea(contour) <= highcontour:
			judge += 'areaok'
		if lowcolor <= r <= highcolor and lowcolor <= g <= highcolor and lowcolor <= b <= highcolor:
			judge += 'colorok'
#		if judge != '':
#			print('x=%d, y=%d, contourarea=%d rgb=%x %x %x %s' % (x, y, cv2.contourArea(contour), r, g, b, judge))
		return judge == 'areaokcolorok'
	except ZeroDivisionError:
		return False
	return False

def detectCatByContour(movie, thresh, lowcontour, highcontour, lowcolor, highcolor):
	total = 0
	catcount = 0
	while(movie.isOpened()):
		ret, frame = movie.read()
		if ret:
			if total % 1 == 0:
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				gray = cv2.GaussianBlur(gray, (11, 11), 0)
				retval, bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
				frame3, contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
				contours = [contour for contour in contours if judgeContourIsCat(frame, contour, lowcontour, highcontour, lowcolor, highcolor)]
				if len(contours) > 0:
					catcount += 1
#				cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
#				cv2.imwrite('frame/cat_frame_%d.png' % total, frame)
			total += 1
			if total % 100 == 0:
				print(total)
		else:
			break
#		if total > 80:
#			break
	return catcount / total

movie = cv2.VideoCapture(sys.argv[1])
ratio = detectCatByContour(movie, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
movie.release()
print(ratio)
