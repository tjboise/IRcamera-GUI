import cv2
import matplotlib.pyplot as plt
from util import damage_density_func
import numpy as np
import traceback
from PIL import Image

image_path = 'images/cropped_image.jpg'
img = cv2.imread(image_path)
print(img.shape)
img, damage_density, IR_seg, gm0, gm = damage_density_func.damage_density(image_path)

print(img.shape)
print(IR_seg.shape)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print(img2.shape)