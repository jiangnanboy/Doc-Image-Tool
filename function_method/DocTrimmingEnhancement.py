import cv2
import numpy as np
import os
import PIL.Image as Image

import torch
import torchvision.transforms as transforms
from torchvision.models.segmentation import deeplabv3_resnet50
from torchvision.models.segmentation import deeplabv3_mobilenet_v3_large

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_path = './weights/image_trimming_enhancement'
model_path = os.path.join(model_path, 'model_mbv3_iou_mix_2C049.pth')

transforms_list = [transforms.ToTensor(), transforms.Normalize(mean=(0.4611, 0.4359, 0.3905), std=(0.2193, 0.2150, 0.2109))]
transformer = transforms.Compose(transforms_list)

def order_points(pts):
    rect = np.zeros((4, 2), dtype='float32')
    pts = np.array(pts)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect.astype('int').tolist()

def find_dest(pts):
    (tl, tr, br, bl) = pts
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
    return order_points(destination_corners)

def load_model(num_classes=2, model_name="mbv3", checkpoint_path=None):
    print('init and load doc trimming enhancement model...')
    if model_name == "mbv3":
        model = deeplabv3_mobilenet_v3_large(num_classes=num_classes)
    else:
        model = deeplabv3_resnet50(num_classes=num_classes)
    model.to(DEVICE)
    checkpoints = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(checkpoints, strict=False)
    model.eval()
    return model

def doc_trimming_enhancement_pred(image, image_size=384, BUFFER=10):
    IMAGE_SIZE = image_size
    half = IMAGE_SIZE // 2
    imH, imW, C = image.shape
    image_resize = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_NEAREST)

    scale_x = imW / IMAGE_SIZE
    scale_y = imH / IMAGE_SIZE

    image_transformer = transformer(image_resize)
    image_transformer = torch.unsqueeze(image_transformer, dim=0)

    with torch.no_grad():
        out = doc_trimming_enhancement_model(image_transformer)["out"].cpu()


    out = torch.argmax(out, dim=1, keepdims=True).permute(0, 2, 3, 1)[0].numpy().squeeze().astype(np.int32)

    r_H, r_W = out.shape

    _out_extended = np.zeros((IMAGE_SIZE + r_H, IMAGE_SIZE + r_W), dtype=out.dtype)
    _out_extended[half : half + IMAGE_SIZE, half : half + IMAGE_SIZE] = out * 255
    out = _out_extended.copy()
    # Edge Detection.
    canny1 = cv2.Canny(out.astype(np.uint8), 225, 255)

    canny = cv2.dilate(canny1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    # 查找轮廓
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    page = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    # 计算轮廓的逼近==========================================
    # 计算轮廓周长
    epsilon = 0.02 * cv2.arcLength(page, True)
    # 多边形拟合
    corners = cv2.approxPolyDP(page, epsilon, True)
    # 原始轮廓
    # cv2.drawContours(canny, [page], -1, (0, 255, 0), 3)
    # 逼近轮廓
    cv2.drawContours(canny1, [corners], -1, (255, 0, 0), 3)

    # 数组拼接
    corners = np.concatenate(corners).astype(np.float32)

    corners[:, 0] -= half
    corners[:, 1] -= half

    corners[:, 0] *= scale_x
    corners[:, 1] *= scale_y


    # check if corners are inside.if not find smallest enclosing box, expand_image then extract document else extract document

    if not (np.all(corners.min(axis=0) >= (0, 0)) and np.all(corners.max(axis=0) <= (imW, imH))):
        print('enter check...')
        left_pad, top_pad, right_pad, bottom_pad = 0, 0, 0, 0
        # 获取最小外接矩阵
        rect = cv2.minAreaRect(corners.reshape((-1, 1, 2)))
        # 获取矩形四个顶点
        box = cv2.boxPoints(rect)
        box_corners = np.int32(box)
        #     box_corners = minimum_bounding_rectangle(corners)

        box_x_min = np.min(box_corners[:, 0])
        box_x_max = np.max(box_corners[:, 0])
        box_y_min = np.min(box_corners[:, 1])
        box_y_max = np.max(box_corners[:, 1])

        # Find corner point which doesn't satify the image constraint and record the amount of shift required to make the box corner satisfy the constraint
        if box_x_min <= 0:
            left_pad = abs(box_x_min) + BUFFER

        if box_x_max >= imW:
            right_pad = (box_x_max - imW) + BUFFER

        if box_y_min <= 0:
            top_pad = abs(box_y_min) + BUFFER

        if box_y_max >= imH:
            bottom_pad = (box_y_max - imH) + BUFFER

        # new image with additional zeros pixels
        image_extended = np.zeros((top_pad + bottom_pad + imH, left_pad + right_pad + imW, C), dtype=image.dtype)

        # adjust original image within the new 'image_extended'
        image_extended[top_pad : top_pad + imH, left_pad : left_pad + imW, :] = image
        image_extended = image_extended.astype(np.float32)

        # shifting 'box_corners' the required amount
        box_corners[:, 0] += left_pad
        box_corners[:, 1] += top_pad

        corners = box_corners
        image = image_extended

    corners = sorted(corners.tolist())
    corners = order_points(corners)
    destination_corners = find_dest(corners)
    M = cv2.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))

    final = cv2.warpPerspective(image, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv2.INTER_LANCZOS4)
    final = np.clip(final, a_min=0., a_max=255.)
    if len(final.shape) == 3: final = final.astype(np.uint8)
    return final[:,:,::-1]

doc_trimming_enhancement_model = load_model(2, model_name='mbv3', checkpoint_path=model_path)







