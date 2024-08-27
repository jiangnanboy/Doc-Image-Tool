import cv2
import os

model_path = './weights/image_sharpening'
model_path = os.path.join(model_path, 'espcn_x3.pb')
name = 'espcn'
scale = 3

def img_enh(img, type='usm'):
    if type == 'usm':
        blur_img = cv2.GaussianBlur(img, (0, 0), 5)
        sharp_img = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    elif type == 'sobel':
        blur_img = cv2.medianBlur(img, 3)
        sharp_img = cv2.Sobel(blur_img, cv2.CV_8U, 1, 0, ksize=3)
    return sharp_img

def load_model():
    print('init and load doc sharpening model...')
    model = cv2.dnn_superres.DnnSuperResImpl_create()
    model.readModel(model_path)
    model.setModel(name, scale)
    return model

def doc_sharpening_pred(image):
    result = doc_sharpening_model.upsample(image)
    return result

doc_sharpening_model = load_model()


