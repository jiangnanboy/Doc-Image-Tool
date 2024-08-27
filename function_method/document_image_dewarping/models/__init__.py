from ..models.densenetccnl import *
from ..models.unetnc import *

def get_model_stage_one(n_classes=1, in_channels=3):
    model = UnetGenerator(input_nc=in_channels, output_nc=n_classes, num_downs=7)
    return model

def get_model_stage_two(n_classes=1, in_channels=3):
    model = dnetccnl(img_size=128, in_channels=in_channels, out_channels=n_classes, filters=32)
    return model

