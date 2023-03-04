import cv2

#create a window
cv2.namedWindow("image")

# Read png image
im_orig = cv2.imread("rock.png")
#crop image in half on the y axis
im_orig = im_orig[im_orig.shape[0]//2:, :]

#display image
cv2.imshow("image", im_orig)
cv2.waitKey(1)

#gaussian blur
im = cv2.GaussianBlur(im_orig, (5,5), 0)
cv2.imshow("image", im)
cv2.waitKey(1)

#use canny edge detection using trackbars
def trackbar_callback(x):
    im2 = cv2.Canny(im, x, x*3)
    #apply contour detection
    contours, hierarchy = cv2.findContours(im2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #filter out contours that are too big or too small
    contours = [c for c in contours if cv2.contourArea(c) > 7 and cv2.contourArea(c) < 700]

    #try to close contours
    for i in range(len(contours)):
        contours[i] = cv2.approxPolyDP(contours[i], 0.1, True)

    #draw contours on the original image
    cp = im_orig.copy()
    cv2.drawContours(cp, contours, -1, (0,255,0), 1)
    cp = cv2.resize(cp, (0,0), fx=2, fy=2)

    #resize image
    #display the original image and the contours
    cv2.imshow("image", cp)
    cv2.waitKey(1)

cv2.createTrackbar("canny", "image", 0, 255, trackbar_callback)
cv2.waitKey(0)



# convert to hsv
# hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
# cv2.imshow("image", hsv)
# cv2.waitKey(0)

# use morphclose on saturation channel
# hsv[:,:,1] = cv2.morphologyEx(hsv[:,:,1], cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
# cv2.imshow("image", hsv)
# cv2.waitKey(0)

# normalize saturation channel
# hsv[:,:,1] = cv2.normalize(hsv[:,:,1], None, 0, 255, cv2.NORM_MINMAX)

# cv2.imshow("image", hsv)
# cv2.waitKey(0)
