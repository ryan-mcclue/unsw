#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement
import sys
import os
import pathlib

# https://pyresearch.org/product/fruit-quality-detection-system-using-artificial-intelligence/

# TODO: use jupyter notebook with conda?

# fruit coming up on conveyor belt, humans may ireggularly determine if rotten
# machine offers consistency; from bunch of fruit, outline what ones to throw away;
# so AI based quality inspection
# could 

# CNN (good at feature extraction) MobileNetV2 model (less computationally intensive) pretrained on imagenet ()
# add layers to this 'base' model according to requirements?

# python3 -m venv name 
# source name/bin/activate; deactivate (.gitignore name)
# pip freeze > requirements.txt

valid (what we know) and train (evaluate) so require annotations to verify

dataset/test/
   freshapple/
   rottenapple/
   ...
dataset/train/

enum Categories:
  fresh
  rotten

def load_training_data():
  cv_imgs = []
  
  imgs = []
  labels = []
  for img in tqdm(test_dir):
    if 'fresh' in img_name:
      imgs.append(cv2.resize(100, 100); cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
      labels.append(Categories.fresh)

      # might want to crop fruit out of images

  return [imgs, labels]

def train():
  # using CNN neural network?

  imgs, labels = load_data("dataset/train")
  np_imgs = np.array(imgs)
  np_labels = np.array(labels)
  # np_imgs.shape
  # debug_display_img_array(np_imgs)

  y_ser = pd.Series(np_labels)
  y_ser.value_counts()

  imgs_val, labels_val = load_data("dataset/test")

  # keras setup

  # model.fit() actually trains

  # display model accuracy with graph

  # model.save()




def run():
  # will have .pickle, .h5, .model files that have been generated?
  # dataset/test/freshapples,rottenapples
  # dataset/train/

  # model = tf.keras.modules.load_module('fruit-cnn.model')
  # prediction = model.predict(preprocess_img('test/freshapples/app1.jpg'))
  # if prediction[][] == 1: fresh

# TODO: seems .evalute() for testing on images and .predict() for new images

def create_testing_data():
  for img in test_dir:
    TEST_DATA.append([preprocess_img, category])

  pickle.dump(preprocessed_imgs)
  pickle.dump(img_categories)

def test_run():
  # load_test_data()
  # model.evaluate(p)


def main():
  print("brick by brick")

if __name__ == '__main__':
  if sys.gettrace() is None:
    os.environ["PYTHONBREAKPOINT"] = "0"
    directory_of_running_script = pathlib.Path(__file__).parent.resolve()
    os.chdir(directory_of_running_script)

  main()

def main():
  recorded_video = get_video_drag_and_drop();
  output = process(recorded_video)

# TODO
