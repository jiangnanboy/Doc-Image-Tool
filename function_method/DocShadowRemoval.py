import numpy as np
from scipy import ndimage
import matplotlib.image as mpimg
from skimage import color
from skimage.filters import threshold_otsu


def read_img(filename, isRGB=False):
  img = mpimg.imread(filename)
  if not isRGB: img = color.rgb2gray(img) # convert to grayscale
  return img

def get_LocalBG(img, kernel_size=5):
  
  L = None
  if len(img.shape) == 3:
    temp_L = []
    for i in range(3):
      Imax = ndimage.maximum_filter(img[:,:,i], size=kernel_size) # apply max filter
      temp_L.append(Imax)
      temp_L[i][temp_L[i] == 0] = 0.000001 # to prevent NaN due to divide by 0
    L = np.stack((temp_L), axis=2)
  else:
    Imax = ndimage.maximum_filter(img, size=kernel_size) # apply max filter
    L = Imax
    L[L == 0] = 0.000001 # to prevent NaN due to divide by 0

  return L

def get_GlobalBG(L):

  unshadow_bg = None
  G = None
  if len(L.shape) == 3:
    unshadow_bgs = []
    for i in range(3):
      thresh = threshold_otsu(L[:,:,i]) # binarize image with thresholding
      unshadowed_area = L[:,:,i] > thresh
      temp_unshadow_bg = L[:,:,i] * unshadowed_area # mask the shadowed areas
      unshadow_bgs.append(temp_unshadow_bg)
      unshadow_bg = np.stack((unshadow_bgs), axis=2)

    for i in range(3):
      unshadow_bgs[i] = unshadow_bgs[i][unshadow_bgs[i] != 0]
      unshadow_bgs[i] = np.mean(unshadow_bgs[i]) # average pixel color
      unshadow_bgs[i] = unshadow_bgs[i] * np.ones(L[:,:,i].shape)
      unshadow_bgs[i] = unshadow_bgs[i].astype(int)
    G = np.stack((unshadow_bgs), axis=2)

  else:
    thresh = threshold_otsu(L) # binarize image with thresholding
    unshadowed_area = L > thresh
    unshadow_bg = L * unshadowed_area # mask the shadowed areas

    temp_unshadow_bg = unshadow_bg[unshadow_bg != 0]
    temp_unshadow_bg = np.mean(temp_unshadow_bg) # average pixel color
    G = temp_unshadow_bg * np.ones(L.shape)

  return G

def get_FinalImg(img, L, G):

  r = G/L # find shadow scale
  final = r * img # relight shadow regions
  if len(img.shape) == 3: final = final.astype(np.uint8)

  return final


def fineTune(img, L, G, final):

  thresh = threshold_otsu(L) # binarize image with thresholding
  shadow_map = L < thresh
  shadow_bg = L * shadow_map # mask the unshadowed areas
  shadow_bg = shadow_bg[shadow_bg != 0]
  shadow_bg = np.mean(shadow_bg) # average pixel color
  shadow_bg = shadow_bg * np.ones(L.shape)

  tau = (G/shadow_bg) * 0.5 # find tone scale
  tuned = final * tau # apply tone scale
  if len(img.shape) == 3: tuned = tuned.astype(np.uint8)
  return tuned

def removeShadow(img):
  img = img[:,:,::-1]
  L = get_LocalBG(img, 13) # get the local background color
  G = get_GlobalBG(L) # get the global background color
  final = get_FinalImg(img, L, G) # show the input vs output
  # mpimg.imsave(r'E:\pycharm project\DocImgTool\test.jpg', final)
  # tuned = fineTune(img, L, G, final) # show effects of tuning
  final = final[:, :, ::-1]
  return final
