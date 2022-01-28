import cv2 
import numpy as np
import cvzone
import pickle


image = cv2.imread('lot_2.png')

# rectangle measurments 
width = 60
height = 120
with open('CarParking', 'rb') as f:
       posList = pickle.load(f)

def checkspace(imagepro):
    availableSpace = 0
    #rectangle to represent one parking space  
    for pos in posList:
        x,y = pos
        imgcrop = imagepro[y:y+height, x:x+width]
        #cv2.imshow(str(x*y), imgcrop)
        count = cv2.countNonZero(imgcrop)
        cvzone.putTextRect(image, str(count), (x,y+height-5), scale = 1, thickness=2, offset=0, colorR=(0,0,0))

        if count < 500:
            color = (0,255,0)
            thickness = 2
            availableSpace = availableSpace + 1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(image,pos,(pos[0] + width, pos[1] + height),color, thickness)

    cvzone.putTextRect(image, f'Available spaces: {availableSpace}/{len(posList)}', (0,30), scale = 2, thickness=2, offset=10, colorR=(0,0,0))
while True:

    # Read image 
    image = cv2.imread('lot_2.png')
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    #cv2.imshow("Image dilate", imgDilate)

    checkspace(imgDilate)
    #for pos in posList:
        #cv2.rectangle(image,pos,(pos[0] + width, pos[1] + height),(0,0,0), 2)
    cv2.imshow("Parking space", image)
    cv2.waitKey(1)