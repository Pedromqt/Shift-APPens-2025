import cv2


def capture():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Cam não abriu")
        exit()
        
    while True:
        ret, frame = cam.read()

        if not ret:
            print("tira")
            
        cv2.imshow("asda",frame)
        
        if (cv2.waitKey(5) > 0):
            break
        
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()