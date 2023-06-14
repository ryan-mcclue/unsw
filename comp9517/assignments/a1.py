#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

# matplotlib.pyplot.bar for histogram
# It's normal that the Otsu's method and Isodata produce very similar results

import pathlib
import os
import sys
import subprocess
import logging
import bisect
import platform

from dataclasses import dataclass

import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib as mpl

global global_logger

def fatal_error(msg):
  global_logger.critical(msg)
  breakpoint()
  sys.exit()

def warn(msg):
  global_logger.warning(msg)
  # NOTE(Ryan): Disable by passing -O to interpreter
  if __debug__:
    breakpoint()
    sys.exit()

def trace(msg):
  if __debug__:
    global_logger.debug(msg)

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


def compute_laplacian(img):
  output_img = img.copy()

  img_width = img.shape[1]
  img_height = img.shape[0]

  k3x3_laplace = make_k3x3_laplace() 

  output_img_gray_values = [0] * (img_width * img_height)
  
  for x in range(img_width):
    for y in range(img_height):
      m3x3 = make_m3x3_from_cv_image(img, x, y)

      gray_value = convolve_k3x3_laplace(k3x3_laplace, m3x3)

      output_img_gray_values[y * img_width + x] = gray_value

  min_convolved = min(output_img_gray_values)
  max_convolved = max(output_img_gray_values)

  for x in range(img_width):
    for y in range(img_height):
      cur_gray = output_img_gray_values[y * img_width + x]
      normalised_gray = translate(min_convolved, max_convolved, cur_gray, 0, 255)
      output_img[y, x] = [normalised_gray] * 3
 
  return output_img

def contrast_stretch(i, a, b, c, d):
  return (i - c) * ((b - a) / (d - c)) + a

# TODO(Ryan): For BGR, generalise for number of channels
def contrast_stretch_grayscale(img):
  output_img = img.copy()

  img_width = img.shape[1]
  img_height = img.shape[0]

  min_input = sys.maxsize
  max_input = 0
  for x in range(img_width):
    for y in range(img_height):
      gray_value = img[y, x][0]
      if gray_value > max_input:
        max_input = gray_value
      if gray_value < min_input:
        min_input = gray_value

  for x in range(img_width):
    for y in range(img_height):
      output_img[y, x] = [contrast_stretch(img[y, x][0], 0, 255, min_input, max_input)] * 3

  return output_img


def find_first_index_larger(arr, val):
  possible_index = bisect.bisect_left(arr, val)

  # NOTE(Ryan): No index found, i.e. returns last element
  if arr[possible_index] < val:
    return -1

  # NOTE(Ryan): Could return index of same value
  while possible_index < (len(arr) - 1) and arr[possible_index] == val:
    possible_index += 1
  # NOTE(Ryan): Only equal values found
  if arr[possible_index] == val:
    return -1

  return possible_index

def get_grayscale(img):
  w = img.shape[1]
  h = img.shape[0]
  grayscale = [0] * (w * h)

  for x in range(w):
    for y in range(h):
      grayscale[y * w + x] = img[y, x][0]

  return grayscale

def get_grayscale_sums(grayscale_values):
  sums = [0] * len(grayscale_values)

  running_sum = 0
  for i in range(len(sums)):
    running_sum += grayscale_values[i]
    sums[i] = running_sum 

  return sums

def get_avg(sums, l, r):
  if l == 0:
    avg_sum = sums[r]
  else:
    avg_sum = sums[r] - sums[l - 1]
  avg_count = (r - l)
  assert(avg_count > 0)

  avg = avg_sum / (r - l)

  return avg

def apply_threshold(img, threshold):
  w = img.shape[1]
  h = img.shape[0]
  for x in range(w):
    for y in range(h):
      if img[y, x][0] > threshold:
        img[y, x] = [255] * 3
      else:
        img[y, x] = [0] * 3

# NOTE(Ryan): variance = max(p0p1(u0 - u1)^2) 
def otsu_thresholding(img):
  img_copy = img.copy()

  grayscale_values = get_grayscale(img_copy)
  grayscale_values.sort()

  grayscale_sums = get_grayscale_sums(grayscale_values)

  otsu_threshold = 0
  max_interclass_variance = 0

  threshold_test = 0
  while threshold_test <= 255:
    # NOTE(Ryan): No elements smaller
    if grayscale_values[0] > threshold_test:
      threshold_test += 1
      continue

    p0_start = 0
    # NOTE(Ryan): No elements larger, resulting in 0
    p1_start = find_first_index_larger(grayscale_values, threshold_test)
    if p1_start == -1:
      break

    p0_end = p1_start - 1
    p1_end = len(grayscale_values) - 1

    p0 = p0_end / len(grayscale_values)
    p1 = (1.0 - p0)

    p0_mean = get_avg(grayscale_sums, 0, p0_end)
    p1_mean = get_avg(grayscale_sums, p1_start, p1_end)

    interclass_variance = (p0 * p1) * ((p0_mean - p1_mean)**2)

    if interclass_variance > max_interclass_variance:
      max_interclass_variance = interclass_variance
      otsu_threshold = threshold_test

    threshold_test += 1

  apply_threshold(img_copy, otsu_threshold)

  return img_copy


def isodata_thresholding(img):
  img_copy = img.copy()

  grayscale_values = get_grayscale(img_copy)
  grayscale_values.sort()

  grayscale_sums = get_grayscale_sums(grayscale_values)

  cur_threshold = 128
  while True:
    p0_start = 0
    # NOTE(Ryan): No elements larger, resulting in 0
    p1_start = find_first_index_larger(grayscale_values, threshold_test)
    if p1_start == -1:
      break

    p0_end = p1_start - 1
    p1_end = len(grayscale_values) - 1

    p0_mean = get_avg(grayscale_sums, 0, p0_end)
    p1_mean = get_avg(grayscale_sums, p1_start, p1_end)

    new_threshold = (p0_mean + p1_mean) / 2
    if new_threshold != cur_threshold:
      cur_threshold = new_threshold
    else:
      cur_threshold = new_threshold
      break

  apply_threshold(img_copy, otsu_threshold)

  return img_copy


def triangle_thresholding(img):
  result = img.copy()

  histogram = construct_histogram()

  max_gray_index = gray_values[-1]
  histogram_peak = max(histogram)



  return result

def main():
  images_dir="COMP9517_23T2_Assignment_Images"
  img = cv.imread(f"{images_dir}/Algae.png")

  output_img = otsu_thresholding(img)

  f, axarr = plt.subplots(2, 2)
  axarr[0,0].imshow(img)
  axarr[0,1].imshow(output_img)
  plt.show()

  #plt.imshow(output_img)
  #plt.title('Otsu')
  #plt.show()

  #plt.imshow(cv.cvtColor(image, cv2.COLOR_BGR2RGB)) # cv2 uses BGR but plt uses RGB, hence the conversion
  # cv.imshow('contrast_stretched_laplacian_img', contrast_stretched_laplacian_img)
  # cv.waitKey()

def running_on_jupyter():
  try:
    shell_name = get_ipython().__class__.__name__ 
    if shell_name == "ZMQInteractiveShell":
      return True
    else:
      return False
  except NameError:
      return False

if __name__ == "__main__":
  if not running_on_jupyter():
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
    if sys.gettrace() is None:
      os.environ["PYTHONBREAKPOINT"] = "0"
    directory_of_running_script = pathlib.Path(__file__).parent.resolve()
    os.chdir(directory_of_running_script)

  global_logger = logging.getLogger(__name__)
  global_logger.setLevel(logging.DEBUG)
  global_logger_handler = logging.StreamHandler()
  global_logger_handler.setLevel(logging.DEBUG)
  global_logger_formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
  global_logger_handler.setFormatter(global_logger_formatter)
  global_logger.addHandler(global_logger_handler)

  trace(f"python: {platform.python_version()}")

  trace(f"opencv: {cv.__version__}")
  mpl.rcParams['figure.dpi']= 150

  main()
