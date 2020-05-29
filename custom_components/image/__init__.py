# coding=utf-8
import logging

from esphome import core
from esphome.components import display, font
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import CONF_FILE, CONF_ID, CONF_RESIZE, CONF_TYPE
from esphome.core import CORE, HexInt
_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['display']
MULTI_CONF = True

Image_ = display.display_ns.class_('Image')

CONF_RAW_DATA_ID = 'raw_data_id'

IMAGE_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.declare_id(Image_),
    cv.Required(CONF_FILE): cv.file_,
    cv.Optional(CONF_RESIZE): cv.dimensions,
    cv.Optional(CONF_TYPE): cv.string,
    cv.GenerateID(CONF_RAW_DATA_ID): cv.declare_id(cg.uint8),
})

CONFIG_SCHEMA = cv.All(font.validate_pillow_installed, IMAGE_SCHEMA)


def to_code(config):
    from PIL import Image

    path = CORE.relative_config_path(config[CONF_FILE])
    try:
        image = Image.open(path)
    except Exception as e:
        raise core.EsphomeError(u"Could not load image file {}: {}".format(path, e))

    if CONF_RESIZE in config:
        image.thumbnail(config[CONF_RESIZE])

    if config[CONF_TYPE].startswith('RGB565'):
        width, height = image.size
        image = image.convert('RGB')
        pixels = list(image.getdata())
        data = [0 for _ in range(height * width * 2)]
     
        pos = 0
        for pix in pixels:
            r = (pix[0] >> 3) & 0x1F
            g = (pix[1] >> 2) & 0x3F
            b = (pix[2] >> 3) & 0x1F
            p = (r << 11) + (g << 5) + b
            data[pos] = (p >> 8) & 0xFF
            pos += 1
            data[pos] = p & 0xFF
            pos += 1
        rhs = [HexInt(x) for x in data]
        prog_arr = cg.progmem_array(config[CONF_RAW_DATA_ID], rhs)
        cg.new_Pvariable(config[CONF_ID], prog_arr, width, height, 1)
    else:
        image = image.convert('1', dither=Image.NONE)
        width, height = image.size
        if width > 500 or height > 500:
            _LOGGER.warning("The image you requested is very big. Please consider using the resize "
                            "parameter")
        width8 = ((width + 7) // 8) * 8
        data = [0 for _ in range(height * width8 // 8)]
        for y in range(height):
            for x in range(width):
                if image.getpixel((x, y)):
                    continue
                pos = x + y * width8
                data[pos // 8] |= 0x80 >> (pos % 8)

        rhs = [HexInt(x) for x in data]
        prog_arr = cg.progmem_array(config[CONF_RAW_DATA_ID], rhs)
        cg.new_Pvariable(config[CONF_ID], prog_arr, width, height)
