#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

# TODO: only merge branch into master if that branch passes CI

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


def main():
  pass

if __name__ == "__main__":
  # NOTE(Ryan): Disable breakpoints if not running under a debugger
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"

  directory_of_running_script = pathlib.Path(__file__).parent.resolve()
  os.chdir(directory_of_running_script)

  main()
