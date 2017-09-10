import cv2

drawing = False
ix, iy, fx, fy = -1, -1, -1, -1


def drawRectangle(event, x, y, flags, param):

    global ix, iy, fx, fy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        fx, fy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fx, fy = x, y

if __name__ == '__main__':

    img = cv2.imread('berry.jpg')
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', drawRectangle)

    while 1:
        if drawing:
            img = cv2.imread('berry.jpg')
            cv2.rectangle(img, (ix, iy), (fx, fy), (255, 0, 0), 2)
        cv2.imshow('image', img)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    feature = img[iy+2:fy-2, ix+2:fx-2]
    cv2.imwrite('feature.jpg', feature)
    cv2.destroyAllWindows()