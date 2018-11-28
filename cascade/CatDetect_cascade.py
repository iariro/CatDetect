import cv2
import numpy as np

def detectCatByCascade(movie):
    cascade = cv2.CascadeClassifier('cascade.xml')
    print('cascade loaded')
    count = 0
    cat = 0
    while(movie.isOpened()):
        ret, frame = movie.read()
        if ret:
            cv2.imwrite('background.png', frame)
            break
            if count % 10 == 0:
                dstimg = frame.copy()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                objects = cascade.detectMultiScale(gray, 1.07, 3)
                print('%d : %d' % (count, len(objects)))
                if len(objects) > 0:
                    cat += 1
                    for (x, y, w, h) in objects:
                        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    height = dstimg.shape[0]
                    width = dstimg.shape[1]
                    half_size = cv2.resize(gray, (width//2, height//2))
                    cv2.imwrite('frame/cat_frame_%d.png' % count, half_size)
        else:
            break
        count += 1
    print(cat / count)

def detectCatByDiff(movie):
    count = 0
    frame2 = None
    while(movie.isOpened()):
        ret, frame = movie.read()
        if ret:
            if count > 10:
                imgDiff = cv2.absdiff(frame, frame2)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray,(11,11),0)
                retval, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
                frame3, contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                print('%d %d' % (count, len(contours)))
#                for contour in contours:
#                    if cv2.contourArea(contour) < 2000:
#                        continue
#                    x,y,w,h = cv2.boundingRect(contour)
#                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                contours = [contour for contour in contours if 5000 <= cv2.contourArea(contour) <= 10000]
                cv2.drawContours(frame,contours,-1,(0,255,0),3)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                cv2.imwrite('frame/cat_frame_%d.png' % count, frame)
            frame2 = frame
        count += 1
        if count > 20:
            break

movie = cv2.VideoCapture('cat1.mp4')
detectCatByDiff(movie)
movie.release()
