import cv2
import numpy as np
 
img = cv2.imread('./0206/image_20200206161611229132.jpg',0)
 
edges = cv2.Canny(img,100,200)
 
cv2.imshow('edges',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()