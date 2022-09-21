import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, util
from skimage.measure import label, regionprops
from skimage import measure, morphology

def account_area(erosion):
    img = erosion.copy()
    label_img = label(img, connectivity=img.ndim)
    props = regionprops(label_img)
    # props = account_area(erosion)
    areas = []
    major_length = []
    min_length = []
    for prop in props:

        if prop.area > 4000:
            areas.append(prop.area)
            major_length.append(prop.major_axis_length)
            min_length.append(prop.minor_axis_length)

    return areas, major_length, min_length

def damage_density(img_path):

    img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
    m,n = img.shape
    histeq = cv2.equalizeHist(img)
    t2, otsu_img = cv2.threshold(histeq, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # plt.imshow(otsu_img)

    #postprocess
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    erosion = cv2.morphologyEx(otsu_img, cv2.MORPH_CLOSE, kernel, iterations=1)
    # account area
    areas, major_length, min_length = account_area(erosion)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)#默认ksize=3
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1)
    gm = cv2.sqrt(sobelx ** 2 + sobely ** 2)
    # print(gm/255)
    # plt.imshow(gm)
    #erosion = otsu_img
    sobelx0 = cv2.Sobel(erosion,cv2.CV_64F,1,0,ksize=3)#默认ksize=3
    sobely0 = cv2.Sobel(erosion,cv2.CV_64F,0,1)
    gm0 = cv2.sqrt(sobelx0 ** 2 + sobely0 ** 2)
    # plt.imshow(gm0)

    b = np.nonzero(gm0)

    gm = gm/255
    mean_gradient = np.mean(gm[b[0]][b[1]])

    damage_density=mean_gradient*sum(areas)/(m*n)

    '''
    damage_density
    gm0: the contour of the postprocess image
    gm: the gradient map of the raw image
    otsu_img: segmented images
    '''

    return img, damage_density, otsu_img,erosion, gm0, gm


if __name__ == '__main__':

    img_path = '../images/cropped_image.jpg'
    img, damage_density, otsu_img, erosion, gm0, gm = damage_density(img_path)
    # img = cv2.imread(erosion)
    print(type(erosion))
    plt.imshow(gm0)
    plt.show()




