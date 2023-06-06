#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

import pathlib
import os
import sys
import subprocess
import logging

from dataclasses import dataclass

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


def main():
  pass

if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  main()
