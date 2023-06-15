#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import pathlib
import os
import sys
import subprocess
import logging
import bisect
import platform
import math

from dataclasses import dataclass

import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

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
      #grayscale[y * w + x] = img[y, x][0]
      grayscale[y * w + x] = img[y, x]

  return grayscale

def get_grayscale_sums(grayscale_values):
  sums = [0] * len(grayscale_values)

  running_sum = 0
  for i in range(len(sums)):
    running_sum += grayscale_values[i]
    sums[i] = running_sum 

  return sums

def get_avg(sums, l, r):
  assert(r < len(sums))

  if l == 0:
    avg_sum = sums[r]
  else:
    avg_sum = sums[r] - sums[l - 1]

  avg_count = (r - l)

  if avg_count == 0:
    avg = 0
  else:
    avg = avg_sum / (r - l)

  return avg

def apply_threshold(img, threshold):
  w = img.shape[1]
  h = img.shape[0]
  for x in range(w):
    for y in range(h):
      #if img[y, x][0] > threshold:
      #  img[y, x] = [255] * 3
      #else:
      #  img[y, x] = [0] * 3
      if img[y, x] > threshold:
        img[y, x] = 255
      else:
        img[y, x] = 0

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

  trace(f"Otsu threshold: {otsu_threshold}")
  apply_threshold(img_copy, otsu_threshold)

  return img_copy


def isodata_thresholding(img):
  img_copy = img.copy()

  grayscale_values = get_grayscale(img_copy)
  grayscale_values.sort()

  grayscale_sums = get_grayscale_sums(grayscale_values)

  # NOTE(Ryan): Lowering this makes it more like otsu
  cur_threshold = 128
  while True:
    # NOTE(Ryan): No elements smaller
    all_larger = (grayscale_values[0] > cur_threshold)

    # NOTE(Ryan): No elements larger
    p1_start = find_first_index_larger(grayscale_values, cur_threshold)
    all_smaller = (p1_start == -1)

    # NOTE(Ryan): In this case, calculate mean for all pixels
    if all_larger or all_smaller:
      mean = get_avg(grayscale_sums, 0, len(grayscale_sums) - 1)
      new_threshold = mean // 2
    else:
      p0_start = 0
      p0_end = p1_start - 1
      p1_end = len(grayscale_values) - 1

      p0_mean = get_avg(grayscale_sums, p0_start, p0_end)
      p1_mean = get_avg(grayscale_sums, p1_start, p1_end)

      new_threshold = (p0_mean + p1_mean) // 2

    if new_threshold != cur_threshold:
      cur_threshold = new_threshold
    else:
      cur_threshold = new_threshold
      break

  trace(f"Isodata threshold: {cur_threshold}")
  apply_threshold(img_copy, cur_threshold)

  return img_copy


def construct_histogram(gray_values):
  histogram = [0] * 256

  for val in gray_values:
    histogram[val] += 1

  return histogram

def histogram_highest(histogram):
  highest = 0
  for i in range(len(histogram)):
    if histogram[i] > highest:
      highest = i
  return highest

def get_histogram_endpoints(histogram):
  histogram_start = -1
  histogram_end = -1

  for i in range(len(histogram)):
    if histogram[i] != 0:
      if histogram_start == -1:
        histogram_start = i
      else:
        histogram_end = i
  
  return (histogram_start, histogram_end)
   

# NOTE(Ryan): Line is (x1, y1), (x2, y2).
# Point is (x3, y3)
def distance_to_line(x1, y1, x2, y2, x3, y3):
  numerator = abs((x2-x1)*(y1-y3) - (x1-x3)*(y2-y1))
  denominator = math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

  if denominator == 0:
    return 0
  else:
    return (numerator / denominator)


def triangle_thresholding(img):
  img_copy = img.copy()

  grayscale_values = get_grayscale(img_copy)
  grayscale_values.sort()

  histogram = construct_histogram(grayscale_values)

  # max_gray_histogram_index = grayscale_values[-1]

  histogram_peak = max(histogram)
  hisogram_peak_index = -1
  for i in range(len(histogram)):
    if histogram[i] == histogram_peak:
      histogram_peak_index = i
      break

  x0 = histogram_peak_index
  y0 = histogram_peak
  x1 = 0
  y1 = 0

  test_end = 0
  test_inc = 0

  histogram_start, histogram_end = get_histogram_endpoints(histogram)
  # NOTE(Ryan): Flipping triangle
  # https://edstem.org/au/courses/11999/discussion/1440316
  #if (histogram_peak_index - histogram_start) < (histogram_end - histogram_peak_index):
  if histogram_peak_index > 128:
    x1 = histogram_start
    test_end = histogram_start
    test_inc = -1
  else:
    x1 = histogram_end
    test_end = histogram_end
    test_inc = 1
  y1 = histogram[x1]

  max_line_distance = 0
  max_gray_val = 0

  for i in range(x0, test_end, test_inc):
    x2 = i
    y2 = histogram[x2]
    # NOTE(Ryan): Only compute distances for gray intensities > 0 
    if y2 == 0:
      continue
    distance = distance_to_line(x0, y0, x1, y1, x2, y2)

    if distance > max_line_distance:
      max_line_distance = distance
      max_gray_val = x2

  trace(f"Triangle threshold: {max_gray_val}")
  apply_threshold(img_copy, max_gray_val)

  return img_copy

def produce_output_images():
  images_dir="COMP9517_23T2_Assignment_Images"
  images = ["Algae.png", "CT.png", "Nuclei.png", "Rubik.png", "Satellite.png"]

  output_folder="processed_images"
  if not os.path.exists(output_folder):
    os.mkdir(output_folder)

  for image in images:
    img = cv.imread(f"{images_dir}/{image}", cv.IMREAD_GRAYSCALE)

    plt.clf()

    grayscale_values = get_grayscale(img)
    histogram = construct_histogram(grayscale_values)

    plt.bar(np.arange(len(histogram)), histogram)
    plt.savefig(f"{output_folder}/Histogram-{image}", dpi=150)

    otsu_img = otsu_thresholding(img)
    plt.imsave(f"{output_folder}/Otsu-{image}", otsu_img, cmap="gray", dpi=150)

    isodata_img = isodata_thresholding(img)
    plt.imsave(f"{output_folder}/Isodata-{image}", isodata_img, cmap="gray", dpi=150)

    triangle_img = triangle_thresholding(img)
    plt.imsave(f"{output_folder}/Triangle-{image}", triangle_img, cmap="gray", dpi=150)


def jupyter_display():
  images_dir="COMP9517_23T2_Assignment_Images"
  images = ["Algae.png", "CT.png", "Nuclei.png", "Rubik.png", "Satellite.png"]

  for image in images:
    img = cv.imread(f"{images_dir}/{image}", cv.IMREAD_GRAYSCALE)

    plt.clf()

    grayscale_values = get_grayscale(img)
    histogram = construct_histogram(grayscale_values)

    f, axarr = plt.subplots(2, 3)
    axarr[0,0].imshow(img, cmap='gray')
    axarr[0,0].title.set_text(f"{image}")
    axarr[0,1].bar(np.arange(len(histogram)), histogram)
    axarr[0,1].title.set_text("Histogram")
    axarr[1,0].imshow(otsu_img, cmap='gray')
    axarr[1,0].title.set_text("Otsu")
    axarr[1,1].imshow(iso_img, cmap='gray')
    axarr[1,1].title.set_text("Isodata")
    axarr[1,2].imshow(triangle_img, cmap='gray')
    axarr[1,2].title.set_text("Triangle")
    plt.show()


def main():
  #produce_output_images()

  images_dir="COMP9517_23T2_Assignment_Images"
  # this may be affecting histogram?
  # img = cv.imread(f"{images_dir}/Algae.png", cv.IMREAD_GRAYSCALE) 

  # img = cv.imread(f"{images_dir}/Algae.png")
  # img = cv.imread(f"{images_dir}/CT.png", cv.IMREAD_GRAYSCALE)
  # img = cv.imread(f"{images_dir}/Nuclei.png", cv.IMREAD_GRAYSCALE)
  # img = cv.imread(f"{images_dir}/Rubik.png", cv.IMREAD_GRAYSCALE)
  img = cv.imread(f"{images_dir}/Satellite.png", cv.IMREAD_GRAYSCALE)

  otsu_img = otsu_thresholding(img)
  iso_img = isodata_thresholding(img)
  triangle_img = triangle_thresholding(img)

  grayscale_values = get_grayscale(img)
  histogram = construct_histogram(grayscale_values)
  #trace(histogram_highest(histogram))

  f, axarr = plt.subplots(2, 3)
  axarr[0,0].imshow(img, cmap='gray')
  axarr[0,0].title.set_text("original")
  axarr[0,1].bar(np.arange(len(histogram)), histogram)
  axarr[0,1].title.set_text("histogram")
  axarr[1,0].imshow(otsu_img, cmap='gray')
  axarr[1,0].title.set_text("otsu")
  axarr[1,1].imshow(iso_img, cmap='gray')
  axarr[1,1].title.set_text("isodata")
  axarr[1,2].imshow(triangle_img, cmap='gray')
  axarr[1,2].title.set_text("triangle")
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


