import mimetypes
import datetime
from pathlib import Path
from typing import List

import pandas
from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin as JIP
import click


def _ensure_existence(path, file_type):
    location = Path(path)
    exists = location.exists()
    file = location.is_file()
    mime = mimetypes.guess_type(location.as_posix())[0]

    if exists and file and mime == file_type:
        return
    else:
        raise ValueError(
            f"File {location.as_posix()} does not exist, or not in the correct format - {mime} should be {file_type}.")


def _read_names(names_path, column_index) -> List:
    names = pandas.read_excel(names_path, index_col=column_index - 1, header=1)
    vals = names.values
    return vals.tolist()


def _create_container_folder():
    p = Path(str(datetime.datetime.now()))
    p.mkdir(parents=True, exist_ok=True)
    return p.resolve().as_posix()


def _draw_name(origin_image_path, name, dest_image_path, font, bottom_margin):
    img = Image.open(origin_image_path)
    im_width, im_height = img.size
    drawer = ImageDraw.Draw(img)
    font_size = 35
    my_font = ImageFont.truetype(font, font_size)
    w, h = drawer.textsize(name.strip(), font=my_font)
    while im_width - 25 <= w + ((im_width - w) / 2):
        font_size -= 5
        my_font = ImageFont.truetype(font, font_size)
        w, h = drawer.textsize(name.strip(), font=my_font)
    drawer.text((im_width / 2 , im_height - bottom_margin), name.strip(), font=my_font, align="center", anchor='mm', encoding="utf-8", fill="black")
    img.save(dest_image_path, optimize=True)


def _create_tag_names(names, image, font, bottom_margin):
    parent_folder = _create_container_folder()
    suffix = Path(image).suffix
    for name_idx, name in enumerate(names):
        _draw_name(image, name, f"{parent_folder}/{name}{suffix}", font, bottom_margin)


@click.command()
@click.option('--column', default=0, help='Number of names column.')
@click.option('--image', prompt='Image path', help='Absolute path to the image.', required=1, )
@click.option('--names', prompt='Names file path', help='Absolute path to the names data xlsx.', required=1, )
@click.option('--font', prompt='Font path', help='Absolute path to a local font fft.', required=0, default="/Library/Fonts/Space Mono Italic for Powerline.ttf")
@click.option('--bottom_margin', prompt='The bottom margin', help='Num of px from the bottom.', required=0, default=150)
def name_tag(column, image, names, font, bottom_margin):
    try:
        _ensure_existence(image, "image/png")
        _ensure_existence(names, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        names = _read_names(names, column)
        _create_tag_names([name[0] for name in names], image, font, bottom_margin)
    except Exception as e:
        click.echo(click.style(e, fg="red"))


if __name__ == '__main__':
    name_tag()
