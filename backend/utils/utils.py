import fnmatch
import json
import os
import pathlib
import shutil
import socket
import re as re
from datetime import datetime, timedelta
from sys import exit
from typing import Dict, Optional

import coloredlogs
import logging
import unidecode
from PIL import Image
from requests import Response, Session


INTERNAL_DATE_FORMAT = "%Y-%m-%d %H:%M:%S-%f"
coloredlogs.install()


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


#internalDateFormat = "%Y-%m-%d %H:%M:%S"



def get_logger(name, log_level=logging.WARN):
    # Get a logger with the given name
    logger = logging.getLogger(name)
    # Disable propagation to the root logger. Makes sense in Jupyter only...
    logger.propagate = False
    logger.setLevel(log_level)
    hostname = socket.gethostname()

    # Check if the logger has handlers already
    if not logger.handlers:
        # Create a handler
        handler = logging.StreamHandler()

        formatter = logging.Formatter(f'\033[92m%(asctime)s\033[0m \033[95m{hostname}\033[0m \033[94m%(name)s[%(process)d]\033[0m \033[1;30m%(levelname)s\033[0m %(funcName)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def transform_date2string(date_to_transform: datetime) -> str:
    logger = get_logger(transform_date2string.__name__)
    try:
        date_str = date_to_transform.strftime(INTERNAL_DATE_FORMAT)
    except:
        logger.error(
            f"Error transforming date: {date_to_transform}. Continuing with empty date string.")
        date_str = ""
    return date_str


def transform_string2date(string_to_transform: str) -> Optional[datetime]:
    """Transforms a String that holds a date in my standard format to a Date. 
        In case it can't transform it, it return None."""
    logger = get_logger(transform_string2date.__name__, logging.INFO)
    try:
        date_obj = datetime.strptime(string_to_transform, INTERNAL_DATE_FORMAT)
    except:
        logger.info("transformString2Date", "Error transforming string to date: ",
                    string_to_transform)
        date_obj = None
    return date_obj


def get_now_as_string() -> str:
    return transform_date2string(datetime.now())


def get_min_date_as_string() -> str:
    return transform_date2string(datetime(1970, 1, 1))


def strip_blanks(string):
    return string.strip(" \t")


def are_variables_set(var_names) -> bool:
    # log("areVariablesSet", "Checking if vars are set: ", varNames)
    for varName in var_names:
        if not is_variable_set(varName):
            return False
    # log("areVariablesSet", "All vars are set: ", varNames)
    return True


def is_variable_set(var_name: str) -> bool:
    logger = get_logger(is_variable_set.__name__, logging.INFO)
    if (os.getenv(var_name) is None) or (os.getenv(var_name) == ""):
        logger.info("isVariableSet", "Error",
                    f'Variable {var_name} is not set in environment.')
        return False
    return True


def date_string_distance_in_days(date_str1: str, date_str2: str) -> int:
    date1 = transform_string2date(date_str1)
    date2 = transform_string2date(date_str2)
    if not (date1 and date2):
        return -1
    diff: timedelta = abs(date1 - date2)
    return diff.days


def date_string_distance_in_hours(date_str1: str, date_str2: str) -> int:
    date1 = transform_string2date(date_str1)
    date2 = transform_string2date(date_str2)
    if not (date1 and date2):
        return -1
    diff: timedelta = abs(date1 - date2)
    diff_in_seconds = 0
    if diff.days > 0:
        diff_in_seconds += diff.days * 24 * 60 * 60
    diff_in_seconds += diff.seconds
    diff_in_hours = diff_in_seconds / (60 * 60)
    # log("dateStringDistanceInHours", "Date1: ", dateStr1,
    #     ", Date2: ", dateStr2, ", Diff in h: ", diffInHours)
    return diff_in_hours


def get_image_size(filename: str) -> Dict:
    """Returns the size of the image in the file given.
    If it's a svg it returns None."""
    logger = get_logger(get_image_size.__name__, logging.INFO)
    file_extension = pathlib.Path(filename).suffix
    # log("getImageSize: ",
    #     "File extension: ", file_extension)
    if file_extension == ".svg":
        return {}
    elif not os.path.exists(filename):
        logger.warn("getImageSize: ", "File does not exist: ", filename)
        return {}
    else:
        try:
            img = Image.open(filename)
            width = img.width
            height = img.height
            return {"width": width, "height": height}
        except:
            logger.warn("getImageSize: ",
                        "Could not open image file: ", filename)
            return {}


def load_page(http_session: Session, url: str) -> Optional[Response]:
    logger = get_logger(load_page.__name__, logging.INFO)
    try:
        page = http_session.get(url)
        return page
    except:
        logger.error("loadPage", url, ": Error!")
        return None


def simplify_text(some_text: str) -> str:
    """
    Simplifies a text to be used as a filename
    """
    simplified_text = some_text.replace('"', "'")
    simplified_text = unidecode.unidecode(simplified_text)
    simplified_text = re.sub("[^A-Za-z-_]+", "_", simplified_text)
    simplified_text = re.sub('_+', '_', simplified_text)
    return simplified_text
