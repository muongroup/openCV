import cv2
import numpy as np
 
img_org = cv2.imread('./0206/image_20200206161611229132.jpg')
imgray = cv2.cvtColor(img_org,cv2.COLOR_BGR2GRAY)
imgray = cv2.medianBlur(imgray,5)
 
circles = cv2.HoughCircles(imgray,cv2.HOUGH_GRADIENT,1,20,
                           param1=540,param2=30,minRadius=0,maxRadius=0)
 
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
   # draw the outer circle
   cv2.circle(img_org,(i[0],i[1]),i[2],(0,255,0),2)
   # draw the center of the circle
   cv2.circle(img_org,(i[0],i[1]),2,(0,0,255),3)
 
cv2.imshow('detected circles',img_org)
cv2.waitKey(0)
cv2.destroyAllWindows()