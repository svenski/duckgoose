# duckgoose
Utils for fast.ai course

## `fetchImagesAndPrepForClassification`
Utility for Lesson 1 experimentation with external classes. The script:
* Downloads images from google images download for specific classes
* Sanity check that images can be opened and have three channels
* Organises the images into separate folders (train/valid/test + classes) as expected by the fast.ai library
