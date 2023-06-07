#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import pathlib
import os
import sys
import subprocess
import logging
import platform

from dataclasses import dataclass

import cv2 as cv

def fatal_error(msg):
  logging.critical(msg)
  breakpoint()
  sys.exit()

def warn(msg):
  logging.warning(msg)
  # NOTE(Ryan): Disable by passing -O to interpreter
  if __debug__:
    breakpoint()
    sys.exit()

def trace(msg):
  if __debug__:
    logging.debug(msg)




# what is format of input image?
# 1. Open and read image files.
# 2. Display and write image files. (binary segmented image)
# 3. Perform basic image processing operations on images.
# 4. Implement and apply various automatic thresholding techniques to images.

# For this assignment (same as for the labs), make sure that in your Jupyter notebook the
# input images are readable from the location specified as an argument, and all output images
# and other requested results are displayed in the notebook environment. All cells in your
# notebook should have been executed so that the tutor/marker does not have to execute the
# notebook again to see the results.
def otsu(image):
  pass

def make_empty_matrix(n):
  return [[0] * n for i in range(n)]


def clamp(val, limit):
  clamped_val = val

  if val < 0:
    clamped_val = 0
  elif val >= limit:
    clamped_val = limit - 1
  
  return clamped_val

def make_k3x3_laplace():
  k3x3 = make_empty_matrix(3)

  k3x3[0][0] = 0 
  k3x3[1][0] = 1 
  k3x3[2][0] = 0 

  k3x3[0][1] = 1 
  k3x3[1][1] = -4 
  k3x3[2][1] = 1 

  k3x3[0][2] = 0 
  k3x3[1][2] = 1 
  k3x3[2][2] = 0 

  return k3x3

def make_m3x3_from_cv_image(cv_img, centre_x, centre_y):
  m3x3 = make_empty_matrix(3)

  w = cv_img.shape[1]
  h = cv_img.shape[0]

  # NOTE(Ryan): Duplicating last pixel for border problem   
  x00 = clamp(centre_x - 1, w)
  x01 = clamp(centre_x, w)
  x02 = clamp(centre_x + 1, w)

  y00 = clamp(centre_y - 1, h)
  y01 = clamp(centre_y, h)
  y02 = clamp(centre_y + 1, h)

  # first pixel is fine as greyscale
  m3x3[0][0] = cv_img[y00, x00][0] 
  m3x3[0][1] = cv_img[y00, x01][0]
  m3x3[0][2] = cv_img[y00, x02][0]

  m3x3[1][0] = cv_img[y01, x00][0]
  m3x3[1][1] = cv_img[y01, x01][0]
  m3x3[1][2] = cv_img[y01, x02][0]

  m3x3[2][0] = cv_img[y02, x00][0] 
  m3x3[2][1] = cv_img[y02, x01][0]
  m3x3[2][2] = cv_img[y02, x02][0]

  return m3x3


def convolve_3x3(k3x3, m3x3):
  result = 0

  #k3x3_sum = 0

  for x in range(3):
    for y in range(3):
      result += (k3x3[y][x] * m3x3[y][x])
      #k3x3_sum += k3x3[y][x]

  # avoid numpy runtime error
  # assert(k3x3_sum != 0)
  # result /= k3x3_sum

  return result


def main():
  trace(f"opencv: {cv.__version__}")

  images_dir="COMP9517_23T2_Lab1_Images"

  img = cv.imread(f"{images_dir}/Einstein.png")
  img_width = img.shape[1]
  img_height = img.shape[0]

  output_img = img.copy()

  k3x3_laplace = make_k3x3_laplace() 

  for x in range(img_width):
    for y in range(img_height):
      m3x3 = make_m3x3_from_cv_image(img, x, y)
      gray_value = convolve_3x3(k3x3_laplace, m3x3)
      # TODO: map gray value to 0-255
      output_img[y, x] = [gray_value] * 3


  #cv.imshow('image', img)
  cv.imshow('image', output_img)
  cv.waitKey()
# 
# for i in range(0, height):
#     for j in range(0, (width/4)):
#         img[i,j] = [0,0,0]  
# 
# for i in range(0, height):
#     for j in range(3*(width/4), width):
#         img[i,j] = [0,0,0]        





if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  logging.basicConfig(level=logging.DEBUG)

  trace(f"python: {platform.python_version()}")

  main()
