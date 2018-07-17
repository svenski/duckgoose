# duckgoose
Utility scripts for the online [fast.ai](www.fast.ai) course

1. Utility for Lesson 1 experimentation with external classes. The script:
* Downloads images from google images download for specific classes
* Sanity check that images can be opened and have three channels
* Organises the images into separate folders (train/valid/test + classes) as expected by the fast.ai library

2. Utility for creating Class Activation Maps for both classifications.

## Prerequisites 

* `chromedriver` is required. On ubuntu/debian: `sudo apt-get chromium-chromedriver`

## Installation

```python
pip install duckgoose
```

## Usage

```python
from duckgoose import fetchImagesAndPrepForClassification

# dictionary structure `class_name => search term`
image_classes = { 'ducks' : 'ducks -rubber' , 'geese' : 'geese' }
download_path = '/home/myuser/data/downloaded_from_google'
output_path = '/home/myuser/data/ducksgeese/'
number_of_images = 100

fetchImagesAndPrepForClassification(image_classes, download_path, output_path, number_of_images)
```

TODO: add usage for CAM

# License
[The MIT License (MIT)](LICENSE.txt)
