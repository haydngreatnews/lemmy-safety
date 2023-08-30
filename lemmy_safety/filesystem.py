import os
from loguru import logger
import sys
import PIL.Image
from os.path import join, getmtime

image_directory = os.getenv("IMAGE_DIRECTORY")
if image_directory is None:
    logger.error("You need to provide an IMAGE_DIRECTORY var in your .env file")
    sys.exit(1)


def get_image(path):
    img = PIL.Image.open(path)
    return img


def delete_image(path):
    os.remove(path)


def get_all_images_after(cutoff_time):
    images = get_all_images()
    unix_cutoff = cutoff_time.timestamp()
    logger.info(
        f"Starting seek of images after: {cutoff_time:%Y-%m-%d %H:%M:%S} (timestamp {unix_cutoff})"
    )
    filtered_iterator = filter(lambda fp: getmtime(fp) > unix_cutoff, images)
    return filtered_iterator


def get_all_images():
    for dir, _, fnames in os.walk(image_directory):
        yield from [join(dir, fname) for fname in fnames]