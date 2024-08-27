import cv2
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem
import numpy as np
from function_method.TextOrientationCorrection import eval_angle
from function_method.DocBleach import sauvola_threshold
from function_method.HandwritingDenoisingBeautifying import docscan_main, get_argument_parser
from function_method.DocShadowRemoval import removeShadow
from function_method.DocSharpening import doc_sharpening_pred, img_enh
from function_method.DocTrimmingEnhancement import doc_trimming_enhancement_pred
from function_method.document_image_dewarping.correct import dewarping_pred

class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setSizeHint(QSize(120, 60))  # size

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)

class BleachItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('漂白', parent=parent)

    def __call__(self, img):
        img = sauvola_threshold(img)
        return img

class OrientationCorrectionItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('文字方向矫正', parent=parent)

    def __call__(self, img):
        img, _ = eval_angle(img, [-30, 30])
        return img

class HandwritingDenoisingBeautifyingItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('笔记去噪美化', parent=parent)

    def __call__(self, img):
        img = docscan_main(img, get_argument_parser().parse_args())
        return img

class DocShadowRemovalItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('去阴影', parent=parent)

    def __call__(self, img):
        img = removeShadow(img)
        return img

class DocDewarpingItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('扭曲矫正', parent=parent)

    def __call__(self, img):
        img = dewarping_pred(img)
        return img

class ImageSharpeningItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('清晰增强', parent=parent)

    def __call__(self, img):
        result = doc_sharpening_pred(img)
        result = img_enh(result)
        return result

class DocTrimmingEnhancementItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('切边增强', parent=parent)

    def __call__(self, img):
        img = img[:,:,::-1]
        img = doc_trimming_enhancement_pred(img)
        return img

'''
class DocBlackSpotRemovalItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('去黑点', parent=parent)

    def __call__(self, img):
        img, _ = remove_blackdot_by_cc(img)
        return img
        
class DeWatermarkItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('去水印', parent=parent)

    def __call__(self, img):
        return img

class RemoveStampItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('去印章', parent=parent)

    def __call__(self, img):
        return img

class HandwritingErasureItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('手写体擦除', parent=parent)

    def __call__(self, img):
        return img
'''