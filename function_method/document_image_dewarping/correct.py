# test end to end benchmark data test
import os

import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import cv2

from .models import get_model_stage_one, get_model_stage_two
from .utils import convert_state_dict

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_path = './weights/document_image_dewarping'
wc_model_path = os.path.join(model_path, 'unetnc_doc3d_stage_one.pkl')
bm_model_path = os.path.join(model_path, 'dnetccnl_doc3d_stage_two.pkl')


def load(wc_model_path, bm_model_path):
    print('init and load doc dewarping model...')
    wc_n_classes = 3
    bm_n_classes = 2

    wc_model = get_model_stage_one(wc_n_classes, in_channels=3)
    if DEVICE.type == 'cpu':
        wc_state = convert_state_dict(torch.load(wc_model_path, map_location='cpu')['model_state'])
    else:
        wc_state = convert_state_dict(torch.load(wc_model_path)['model_state'])
    wc_model.load_state_dict(wc_state)
    wc_model.eval()
    bm_model = get_model_stage_two(bm_n_classes, in_channels=3)
    if DEVICE.type == 'cpu':
        bm_state = convert_state_dict(torch.load(bm_model_path, map_location='cpu')['model_state'])
    else:
        bm_state = convert_state_dict(torch.load(bm_model_path)['model_state'])
    bm_model.load_state_dict(bm_state)
    bm_model.eval()

    wc_model.to(DEVICE)
    bm_model.to(DEVICE)
    return  wc_model, bm_model

def unwarp(img, bm):
    w, h = img.shape[0], img.shape[1]
    bm = bm.transpose(1, 2).transpose(2, 3).detach().cpu().numpy()[0, :, :, :]
    bm0 = cv2.blur(bm[:, :, 0], (3, 3))
    bm1 = cv2.blur(bm[:, :, 1], (3, 3))
    bm0 = cv2.resize(bm0, (h, w))
    bm1 = cv2.resize(bm1, (h, w))
    bm = np.stack([bm0, bm1], axis=-1)
    bm = np.expand_dims(bm, 0)
    bm = torch.from_numpy(bm).double()

    img = img.astype(float) / 255.0
    img = img.transpose((2, 0, 1))
    img = np.expand_dims(img, 0)
    img = torch.from_numpy(img).double()

    res = F.grid_sample(input=img, grid=bm)
    res = res[0].numpy().transpose((1, 2, 0))

    return res

def dewarping_pred(img):
    wc_img_size = (256, 256)
    bm_img_size = (128, 128)
    img_copy = img.copy()
    img = cv2.resize(img, wc_img_size)
    img = img[:, :, ::-1]
    img = img.astype(float) / 255.0
    img = img.transpose(2, 0, 1)  # NHWC -> NCHW
    img = np.expand_dims(img, 0)
    img = torch.from_numpy(img).float()

    htan = nn.Hardtanh(0, 1.0)
    image = img.to(DEVICE)
    with torch.no_grad():
        wc_outputs = wc_model(image)
        pred_wc = htan(wc_outputs)
        bm_input = F.interpolate(pred_wc, bm_img_size)
        outputs_bm = bm_model(bm_input)
    uwpred = unwarp(img_copy, outputs_bm)
    uwpred = uwpred[:, :, ::-1] * 255
    if len(uwpred.shape) == 3: uwpred = uwpred.astype(np.uint8)

    return uwpred[:,:,::-1]

wc_model, bm_model = load(wc_model_path, bm_model_path)



