
import fnmatch
import logging
import os
import shutil
from utils import get_logger


def find(pattern, path):
    """Utility to find files wrt a regex search"""
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def flatten_files(input_folder, output_folder, pattern='*.*'):
    """Utility to flatten files in a folder to another folder."""
    # Inspired / copied from https://github.com/khanfarhan10/FileCopyFilterFlatten
    logger = get_logger(flatten_files.__name__, logging.INFO)
    logger.info(f"Flattening files from  {input_folder}  to  {output_folder}")
    include_input_foldername = True

    all_files = find(pattern, input_folder)
    os.makedirs(output_folder, exist_ok=True)

    for each_path in all_files:
        relative_path = os.path.relpath(each_path, os.path.dirname(
            input_folder)) if include_input_foldername else os.path.relpath(each_path, input_folder)
        flattened_relative_path = relative_path.replace(os.path.sep, "_")
        flattened_relative_fullpath = os.path.join(
            output_folder, flattened_relative_path)
        shutil.copy(each_path, flattened_relative_fullpath)
        logger.info(f"Copied {each_path} to {flattened_relative_fullpath}")
