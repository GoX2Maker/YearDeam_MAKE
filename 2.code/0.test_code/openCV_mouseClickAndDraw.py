import cv2
import pandas as pd

imgPath = r'1.data\1.img\prescription.png'
dbPath = r'1.data\0.test\db\test.csv'
title = 'test'

drawing = False # 마우스가 클릭된 상태 확인용
ix,iy = -1,-1
img_history = [] # 이미지 이력을 저장할 리스트
imgPoint_history = [] #이미지 포인트 저장

# 마우스 콜백 함수
def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,img_history

    if event == cv2.EVENT_LBUTTONDOWN: # 마우스를 누른 상태
        drawing = True 
        ix,iy = x,y
        img_history.append(img.copy()) # 복사본 저장
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drawing == True:            # 마우스를 누른 상태 일경우
            img[:] = img_history[-1][:] # 마지막 저장된 이미지로 복원
            cv2.rectangle(img,(ix,iy),(x,y),(0,0,255),1) # 빨간색으로 테두리 그리기
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False;             # 마우스를 때면 상태 변경
        cv2.rectangle(img,(ix,iy),(x,y),(0,0,255),1) # 빨간색으로 테두리 그리기
        imgPoint_history.append({ 'id' : len(imgPoint_history) , 'x1' : ix, 'y1' : iy, 'x2' : x, 'y2' : y})
        print(f"start : ({ix},{iy}), end : ({x},{y})")

img = cv2.imread(imgPath)
cv2.namedWindow(title)
cv2.setMouseCallback(title,draw_rectangle)

while True:
    cv2.imshow(title,img)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:    # ESC 키를 누르면 종료
        break
    elif k == ord('z') and len(img_history) >= 1: # Ctrl + z를 누르면 마지막 그림을 지움
       
        img[:] = img_history[-1][:] # 마지막 저장된 이미지로 복원
        img_history.pop() # 가장 최근의 이력 제거
        imgPoint_history.pop()
        
    elif k == ord('s'): # s를 누르면 이미지 저장
        cv2.imwrite('saved_image.jpg', img)

cv2.destroyAllWindows()
df = pd.DataFrame(imgPoint_history)
df.to_csv(dbPath, index=False)

