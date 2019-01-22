import cv2
import sys
import numpy as np

frame = cv2.imread(sys.argv[1])
cascade = cv2.CascadeClassifier('cascade.xml')
print('cascade loaded')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
objects = cascade.detectMultiScale(gray, 1.07, 3)
if len(objects) > 0:
	for (x, y, w, h) in objects:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.imwrite('cat_frame.png', frame)

