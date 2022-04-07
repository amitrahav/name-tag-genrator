# Name Tags Gen
A CLI that excepts xslx of names and image as inputs and creates a lot of images from those names. 

## Requirements
1. libmagic client - [installation](https://github.com/ahupp/python-magic#installation)
2. Python 3.9
3. openpyxl

## Run and play
Install dependencies and run `$ python _main__.py`
Parameters:
* --names: Str of Absolute path of a xslx file with column filled with names - REQUIRED
* --image: Str of Absolute path of a png image to be the nameTag template - REQUIRED
* --column: Int of Index of column at the names xslx file - default: 0  
* --font: Str of Absolute path of your local installed ttf font to write the names with - default: /Library/Fonts/Space Mono Italic for Powerline.ttf
* --bottom_margin: Int of the number of pixels from the bottom to write the text from - default: 150

### Example:
```bash
 python __main__.py --names=/Users/me/data.xlsx --image=/Users/me/image.png
```