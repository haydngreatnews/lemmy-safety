from loguru import logger
import PIL.Image

from horde_safety.csam_checker import check_for_csam
from horde_safety.interrogate import get_interrogator_no_blip
from lemmy_safety import filesystem
from PIL import UnidentifiedImageError

interrogator = get_interrogator_no_blip()

def check_image(path):
    try:
        image: PIL.Image.Image = filesystem.get_image(path)
    except UnidentifiedImageError:
        logger.warning(
            "Image %s could not be read. Marking it as CSAM to be sure.", path
        )
        return True
    if not image:
        return None
    try:
        is_csam, results, info = check_for_csam(
            interrogator=interrogator,
            image=image,
            prompt="",
            model_info={"nsfw": True, "tags": []},
        )
    except OSError:
        logger.warning(
            "Image %s could not be read. Marking it as CSAM to be sure.", path
        )
        return True
    if is_csam:
        logger.warning(f"{path} rejected as CSAM")
    else:
        logger.info(f"{path} is OK")
    return is_csam
