import cv2
import numpy as np
import HandTrackingModule as htm
import  time
import autopy
wCam,hCam=640,480
pTime=0
detector=htm.handDetector(maxHands=1)
frameR=100
smoothening=7
plocx,plocy=0,0
clocx,clocy=0,0
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
wScr,hScr=autopy.screen.size()
#print(wScr,hScr)
while True:
    #1.Hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    #2.Get tips of middle finger and index
    if len(lmList)!=0:
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]
        #print(x1,y1,x2,y2)
    #3.Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (720 - frameR,540 - frameR), (255, 0, 255), 2)
    # print(fingers)
    #4. Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:

    #5. Convert Coordinates

          x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
          y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))
          clocx = plocx + (x3-plocx)/smoothening
          clocy = plocy + (y3-plocy)/smoothening
    #6. Smoothen Values

    #7. Move Mouse
          autopy.mouse.move(wScr-clocx,clocy)
          cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
          plocx,plocy=clocx,clocy
    #8. Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            #9. Distance Between Fingers
            length,img,LineInfo = detector.findDistance(8,12,img)
            print(length)
            if length<40:
                cv2.circle(img,(LineInfo[4],LineInfo[5]),15,(0,255,255),cv2.FILLED)
                autopy.mouse.click()
    #11.Frame Rates
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
    #12.display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
