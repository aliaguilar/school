import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from keras.preprocessing import image 
from keras import models
import tensorflow as tf
from PIL import Image
import numpy as np
import time 


camera = cv2.VideoCapture(0)
camera_height = 500

class_names = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad','Surprise']




model = models.load_model("dropout_model_2.h5") 
model.summary(line_length=None, positions=None, print_fn=None)

while(True):
    # read a new frame
    _, frame = camera.read()
    
    # flip the frame
    frame = cv2.flip(frame, 1)

    # rescaling camera output
    aspect = frame.shape[1] / float(frame.shape[0])
    res = int(aspect * camera_height) # landscape orientation - wide image
    frame = cv2.resize(frame, (res, camera_height))

    # add rectangle
    cv2.rectangle(frame, (300, 75), (650, 425), (0, 255, 0), 2)

    # show the frame
    cv2.imshow("Capturing frames", frame)

    key = cv2.waitKey(1)



    # save the frame
    leido, frame = camera.read()
    if leido == True:
        status = cv2.imwrite('sayde.png', frame)

        grey_img = cv2.imread('sayde.png', cv2.IMREAD_GRAYSCALE) 
        grey_img =  cv2.resize(grey_img, (48, 48))  
        plt.imshow(grey_img, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
        s = cv2.imwrite('sayde2.png', grey_img)

        #image preprocessing to be used
        img_tensor = image.img_to_array(grey_img)
        img_tensor = np.expand_dims(img_tensor, axis = 0)
        img_tensor /= 255.

        #model response
        answer  = model.predict_classes(img_tensor)
        class_value = model.predict_classes(img_tensor)
        confindence = model.predict(img_tensor)
        print(class_value)
        print(confindence)
        if class_value == 0:
            print('Angry')
            cv2.putText(frame, 'Angry', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        if class_value == 1:
            print('Fear')
            cv2.putText(frame, 'Fear', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        
        if class_value == 2:
            print('Happy')
            cv2.putText(frame, 'Happy', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        
        if class_value == 3:
            print('Neutral')
            cv2.putText(frame, 'Neutral', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        if class_value == 4:
            print('Sad')
            cv2.putText(frame, 'Sad', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        if class_value == 5:
            print('surprise')
            cv2.putText(frame, 'Surprise', (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 240, 150), 2)
        

        cv2.imshow("Real Time emotions detection", frame)
        key = cv2.waitKey(1)
    
    # quit camera if 'q' key is pressed
    if key & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()