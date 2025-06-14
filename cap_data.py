import cv2
import time

class Cap_Data:
    def __init__(self):
        self.mode = 0
        self.cap = cv2.VideoCapture(0)
        self.begin = 9901
        self.end = 10000
        self.interval = 0.5
    
    def capture(self):
        ret, img = self.cap.read()
        img = cv2.flip(img, 1)
        return img     

    def msTime(self):
        return 1000 * time.time()   

if __name__=="__main__":
    capData = Cap_Data()
    keep = time.time()
    print("Waiting for 10 sec...")
    while 1:
        pict = capData.capture()
        cv2.imshow("window",pict)
        key = cv2.waitKey(1) 
        if key == 27: break
        if time.time() > keep + 10: break
    print("--- Start ---")
    count = capData.begin
    keep = time.time()
    if capData.mode == 0:
        while 1:
            pict = capData.capture()
            cv2.imshow("window",pict)
            key = cv2.waitKey(1) 
            if key == 27: break
            if time.time() > keep + capData.interval:
                filename = "data/img_%03d.png" % count
                cv2.imwrite(filename,pict)
                print("captured: %03d" %count)
                count += 1
                keep = time.time()
            if count == capData.end + 1: break
    else:
        while 1:
            pict = capData.capture()
            cv2.imshow("window",pict)
            key = cv2.waitKey(1)
            if key == 27: break
            if time.time() > keep:
                filename = "data/img_fixed.png"
                cv2.imwrite(filename,pict)
                print("captured: fixed")
                break
    cv2.destroyAllWindows()        
    print("--- End ---")
