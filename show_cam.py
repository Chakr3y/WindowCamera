import cv2

# Helper script to display output ( run simultaneously with main )

# output stream
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:

        # Display the resulting frame (optional)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()