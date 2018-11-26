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
            if count > 100:
                dstimg = frame.copy()
                imgDiff = cv2.absdiff(frame, frame2)
                cv2.imwrite('frame/cat_frame_%d.png' % count, imgDiff)
        count += 1
        frame2 = frame
        if count > 150:
            break

movie = cv2.VideoCapture('cat1.mp4')
detectCatByCascade(movie)
movie.release()
