import cProfile

import cv2
from cvzone.HandTrackingModule import HandDetector
import time


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        # For Rectangle
        # cv2.rectangle(img, (100, 100), (200, 200), (178, 161, 255), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (178, 161, 255), cv2.FILLED)

        # for the border
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        # for the Text
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                    cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 2)

    def checkClick(self, x, y):
        # x1 < x < x1 + width
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)

            # for the border
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)

            # for the Text
            cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70),
                        cv2.FONT_HERSHEY_PLAIN, 4, (0, 0,), 5)

            return True
        else:
            False


# Webcam Access
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # set the width (prop id 3)
cap.set(4, 720)  # set the width (prop id 4)

# Creating the Buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', 'C', '=']]
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

# Variables
myEquation = ""
delayCounter = 0

# This code is for detecting one Hand with minimal Error
detector = HandDetector(detectionCon=0.8, maxHands=1)
# Here We are giving the Confidance 80%


# For Showing The Video
# We are taking each image frame from the video and Showing by Loop

while True:
    # Get Image from Webcam
    success, img = cap.read()

    # flipping the image
    img = cv2.flip(img, 1)  # 0 for vertically and 1 for horizontaly

    # Dtection of Hand
    hands, img = detector.findHands(img, flipType=False)
    # To detect the hand before the flip and name it right

    # draw all Buttons
    # result Window Rectangle
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100,), (225, 225, 225), cv2.FILLED)
    # border result window
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100,), (50, 50, 50), 3)
    # all button
    for button in buttonList:
        button.draw(img)

    # Check for Hand
    if hands:
        lmList = hands[0]["lmList"]  # lmList --> Landmark list
        # lmList have the different points of hand. Here in the project We are only interested in index finger
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        # print(length)
        x, y = lmList[8][:2]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    # print(i)
                    myValue = (buttonListValues[int(i % 4)][int(i / 4)])

                    if myValue == "=":
                        try:
                            myEquation = str(eval(myEquation))
                        except Exception as e:
                            myEquation = "Error"
                    elif myValue == "C":
                        myEquation = ''

                    elif len(myEquation) > 10:
                        myEquation = ''

                    else:
                        myEquation += myValue

                    # time.sleep(0.2) # Avoid multiTouch or Duplicate

                    delayCounter = 1

        # Avoid multiTouch or Duplicate
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # Display the result
    cv2.putText(img, myEquation, (800 + 10, 100 + 25),
                cv2.FONT_HERSHEY_PLAIN, 4, (50, 50, 50), 3)

    # Displaying the image
    cv2.imshow("AI CALCULATOR", img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
