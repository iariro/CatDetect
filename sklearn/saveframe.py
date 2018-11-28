import os
import sys
import cv2
import numpy as np

orgfilename, ext = os.path.splitext(os.path.basename(sys.argv[1]))
print(orgfilename)
movie = cv2.VideoCapture(sys.argv[1])
skip = int(sys.argv[2])
end = int(sys.argv[3])

total = 0
while(movie.isOpened()):
	ret, frame = movie.read()
	if ret:
		if total % skip == 0:
			newfilename = 'frame/%s_frame_%03d.png' % (orgfilename, total)
			print('%s %d %d' % (newfilename, total , skip))
			cv2.imwrite(newfilename, frame)
		total += 1
	else:
		break
	if total>end: break

movie.release()
