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



def make_empty_matrix(n):
  return [[0] * n for i in range(n)]


def clamp(val, limit):
  clamped_val = val

  if val < 0:
    clamped_val = 0
  elif val >= limit:
    clamped_val = limit - 1
  
  return clamped_val

def translate(x0, x1, val, x2, x3):
  val_fraction = ((val - x0) / (x1 - x0))
  
  return x2 + (val_fraction * (x3 - x2))

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

def convolve_k3x3_laplace(k3x3, m3x3):
  result = 0

  for x in range(3):
    for y in range(3):
      result += (k3x3[y][x] * m3x3[y][x])

  return result

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

  # NOTE(Ryan): First pixel is fine as greyscale
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


def find_first_index_larger(arr, val):
  result = -1

  for i, j in enumerate(arr):
    if j > val:
      result = i
      break

  return result

def get_grayscale(img):
  w = img.shape[1]
  h = img.shape[0]
  grayscale = [0] * (w * h)

  for x in range(w):
    for y in range(h):
      grayscale[y * w + x] = img[y, x][0]

  return grayscale

def otsu_thresholding(img):
  img_copy = img.copy()

  grayscale_values = get_grayscale(img_copy)
  grayscale_values.sort()

  otsu_threshold = 0
  max_interclass_variance = 0

  threshold_test = 0
  while threshold_test <= 255:
    # no elements smaller
    if grayscale_values[0] > threshold_test:
      threshold_test += 1
      continue

    p0_start = 0
    # no elements larger
    p1_start = find_first_index_larger(grayscale_values, threshold_test)
    if p1_start == -1:
      break

    p0_end = p1_start - 1
    p1_end = len(grayscale_values) - 1

    p0 = p0_end / len(grayscale_values)
    p1 = (1.0 - p0)

    p0_mean = sum(grayscale_values[0:(p0_end+1)]) / (p0_end)
    p1_mean = sum(grayscale_values[p1_start:(p1_end+1)]) / (p1_end - p1_start)

    # max value for: p0p1(p0_mean - p1_mean)^2
    interclass_variance = (p0 * p1) * ((p0_mean - p1_mean)**2)

    if interclass_variance > max_interclass_variance:
      max_interclass_variance = interclass_variance
      otsu_threshold = threshold_test

    threshold_test += 1

  print(otsu_threshold)
  #return apply_threshold(img_copy, ostu_threshold)

def isodata_thresholding(img):
  result = img.copy()

  return result

def triangle_thresholding(img):
  result = img.copy()

  return result



def main():
  trace(f"opencv: {cv.__version__}")

  images_dir="COMP9517_23T2_Assignment_Images"

  img = cv.imread(f"{images_dir}/Algae.png")

  otsu_thresholding(img)


  #cv.imshow('image', output_img)
  #cv.waitKey()

if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  logging.basicConfig(level=logging.DEBUG)

  trace(f"python: {platform.python_version()}")

  main()
