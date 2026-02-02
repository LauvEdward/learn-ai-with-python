import streamlit as st
import cv2
from PIL import Image
import numpy as np

def main():
    st.title('Object Detection for Images')
    file = st.file_uploader("Upload image", type = ['jpg', 'png', 'jpeg'])
    if file is not None:
        st.image(file, caption= "Uploaded Image")
        image = Image.open(file)
        image = np.array(image)
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)),
            0.007843,
            (300, 300),
            127.5
        )
        net = cv2.dnn.readNetFromCaffe(
        "./model/MobileNetSSD_deploy.prototxt.txt",
        "./model/MobileNetSSD_deploy.caffemodel")
        net.setInput(blob)
        detections = net.forward()
        (h, w) = image.shape[:2]
        print(detections)
        for i in np.arange(0 , detections.shape[2]):
            confidence = detections[0 , 0 , i , 2]
            
            if confidence > 0.5 :
                # extract the index of the class label from the ‘detections ‘ ,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                ( startX , startY , endX , endY ) = box.astype("int")
                cv2.rectangle(image, (startX, startY) , (endX ,endY), 100 , 2)

        st.image(image, caption="Processed Image")
if __name__ == "__main__":
    main()
