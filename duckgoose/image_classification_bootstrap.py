from PIL import Image
import os
import glob
from os import path
import random
from tempfile import TemporaryDirectory
import gzip
import tarfile
import shutil
from hashlib import md5

from google_images_download import google_images_download

def fetchImagesAndPrepForClassification(image_classes, download_path, output_path, number_of_images, chromedriver='/usr/lib/chromium-browser/chromedriver'):
    """
    Main entry point to prepare for image classification. The function will
    1. Download jpg images from google images search for the search terms
    2. Sanity check they can be opened and have three channels
    3. Organise into train/valid/test folder as expected by the fastai library

    Parameters:
    The image_classes is a dictionary of image_class to search term. Often they are identical
    """

    downloadImagesForClasses(image_classes, download_path, number_of_images=number_of_images, chromedriver=chromedriver)

    for image_class in image_classes.keys():
        sanitised_images, cannot_open, one_channel = santityCheckAndOrganiseFromGoogle(image_class, download_path, output_path)
        partitonIntoTrainValidTest(sanitised_images, image_class, output_path)


def file_hash(filepath):
    with open(filepath, "rb") as f:
            return md5(f.read()).hexdigest()
        
def santityCheckAndOrganiseFromGoogle(image_prefix, base_path, output_path):
    """ Check that the images can be opened and that there are three channels. Organise into train/valid/test split by 60/30/10% """
    
    # This is tied to the google download settings: specifically using the prefix == class
    gg = f'{base_path}/**/*{image_prefix} *.jpg'

    files = glob.glob(gg, recursive=True)
    outfiles = []
    ioe_error_files = []
    one_channel_files = []
    image_hashes = set()   

    num = 1
    for ff in files:
        try:
            is_ok = True
            ii = Image.open(ff)
            number_of_channels = len(ii.getbands())
            
            if number_of_channels != 3: 
                is_ok = False
                print(f'Figure does not have 3 channels: {ff}')
            
            hash = file_hash(ff)
            if hash in image_hashes: 
                is_ok = False
                print(f'Found duplicate: {ff}')
            
            image_hashes.add(hash)
            
            if is_ok:
                outfiles.append(ff)
                num +=1

        except IOError as ioe:
            ioe_error_files.append(ff)
            print(f'Error encountered for {ff}: {ioe}')

    return(outfiles, ioe_error_files, one_channel_files)

def partitonIntoTrainValidTest(all_files, prefix, output_path, fraction_train = .6, fraction_valid = 0.3):
    """
    Randomnly parititons and copies files into train/valid/test directories with by default a 60/30/10% split.
    The target is [output_path]/train/[prefix] 
    """

    train_files, valid_files, test_files = shuffledSplit(all_files, fraction_train, fraction_valid)

    copyFilesToPath(train_files, output_path, prefix, 'train')
    copyFilesToPath(valid_files, output_path, prefix, 'valid')
    copyFilesToPath(test_files, output_path, prefix, 'test')

def shuffledSplit(all_files, fraction_train, fraction_valid):
    total_number_of_files = len(all_files)

    train_num = round(total_number_of_files * fraction_train)
    valid_num = round(total_number_of_files * fraction_valid)
    test_num = total_number_of_files - train_num - valid_num

    random.shuffle(all_files)

    train_files = all_files[:train_num]
    valid_files = all_files[train_num:(train_num+valid_num)]
    test_files = all_files[(train_num+valid_num):]

    return(train_files, valid_files, test_files)


def copyFilesToPath(files_to_move, output_path, prefix, ml_type):
    this_path = path.join(output_path,ml_type, prefix)
    os.makedirs(this_path, exist_ok=True)
    for tt in files_to_move:
        shutil.copy2(tt, path.join(this_path, path.basename(tt)))


def downloadImagesForClasses(image_classes, download_path, number_of_images=1000, chromedriver='/usr/lib/chromium-browser/chromedriver'):
    """
    Download images for the specified image classes
    """

    if not path.exists(download_path):
        os.makedirs(download_path)

    common_arguments = {'limit' : number_of_images, 
            'format' : 'jpg',
            'color_type' : 'full-color',
            'type' : 'photo',
            'output_directory':download_path,
            'chromedriver': chromedriver} 
            
    for image_class, search_term in image_classes.items():
        downloadImagesFor(image_class, search_term, common_arguments)


def downloadImagesFor(keyword, prefix = None, common_arguments = {}):
    if prefix is None:
        prefix = keyword

    search = common_arguments.copy()
    search['keywords'] = keyword
    search['prefix'] = prefix

    resp = google_images_download.googleimagesdownload()
    paths = resp.download(search)


