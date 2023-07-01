#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

# python3 -m venv name 
# source name/bin/activate; deactivate (.gitignore name)
# pip freeze > requirements.txt

# penguins and turtles classifier

# cannot use popular detection or classification methods
# can expand upon them, modify or brand new

# train/train/image_id_001.jpg (for supervised learning)
#  {
#    "id": 0,
#    "image_id": 0,
#    "category_id": 1,
#    "bbox": [
#      119,
#      25,
#      205,
#      606
#    ],
#    "area": 124230,
#    "segmentation": [],
#    "iscrowd": 0
#  },

# valid/valid/image_id_001.jpg (for testing)
#{
#    "id": 0,
#    "image_id": 0,
#    "category_id": 1,
#    "bbox": [
#      227,
#      93,
#      298,
#      525
#    ],
#    "area": 156450,
#    "segmentation": [],
#    "iscrowd": 0
#  },

# detect or classifier first?

# The presentation must start with an introduction of the problem and then explain the usedmethods, show the obtained results, and discuss these results as well as ideas for future improvements.

# (introduction, methods, results, discussion, demonstration)


# genetic algorithm to optimise cell selection?
# so, say segmentation based on 7 parameters. genetic algorithm to calculate optimum value for these parameters?

# YOLO
# a cell can only contain 1 object (so for more, need finer grid, i.e. higher S value)
# 1. divide img into SxS grid. of these cells, select cell that has objects midpoint. bounding boxes relative to cell. probability of an object in cell
