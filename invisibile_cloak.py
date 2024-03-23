import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initial HSV values for masking the cloak
upper_hue = 115
upper_saturation = 255
upper_value = 255
lower_hue = 96
lower_saturation = 95
lower_value = 80

# Capturing the initial frame for creation of background
while True:
    ret1, first_frame = cap.read()
    cv2.waitKey(1000)
    ret, init_frame = cap.read()      # camera takes a little time to load
    # Check if the frame is returned then break
    if ret:
        break

# Start capturing the frames for actual magic!!
while True:
    ret, frame = cap.read()
    inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kernel to be used for dilation
    kernel = np.ones((3, 3), np.uint8)

    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])

    mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
    mask = cv2.medianBlur(mask, 3)
    mask_inv = 255 - mask
    mask = cv2.dilate(mask, kernel, 5)

    # Apply the mask to both frames and combine
    frame_inv = cv2.bitwise_and(frame, frame, mask=mask_inv)
    blanket_area = cv2.bitwise_and(init_frame, init_frame, mask=mask)

    final = cv2.bitwise_or(frame_inv, blanket_area)

    cv2.imshow("Invisible Cloak", final)
    cv2.imshow("Original", frame)

    if cv2.waitKey(3) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()