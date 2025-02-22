from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import math

cap = cv2.VideoCapture(0)
model = YOLO('./best.pt')
classNames = [
            "apple",
            "banana",
            "beef",
            "blueberries",
            "broccoli",
            "butter",
            "carrot",
            "cauliflower",
            "cheese",
            "chicken",
            "chocolate",
            "corn",
            "cream_cheese",
            "cucumber",
            "dates",
            "eggplant",
            "eggs",
            "ginger",
            "grapes",
            "green_beans",
            "green_bell_pepper",
            "green_chillies",
            "ground_beef",
            "heavy_cream",
            "kiwi",
            "lemon",
            "lettuce",
            "lime",
            "milk",
            "mineral_water",
            "mint",
            "mushrooms",
            "olives",
            "onion",
            "orange",
            "parsley",
            "peach",
            "peas",
            "pickles",
            "potato",
            "radish",
            "red_bell_pepper",
            "red_cabbage",
            "red_grapes",
            "red_onion",
            "salami",
            "sausage",
            "shrimp",
            "spinach",
            "spring_onion",
            "strawberries",
            "sweet_potato",
            "tangerine",
            "tomato",
            "tomato_paste",
            "yellow_bell_pepper",
            "yoghurt",
            "zucchini"
        ]
while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()