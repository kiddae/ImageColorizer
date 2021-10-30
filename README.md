# ![Image](Demo/demo1.jpg)


**`ImageColorizer` is a Python module and a CLI tool** that you can easily use to colorize wallpapers for them to fit a terminal colorscheme.

It currently supports importing colorschemes from the currently set `Xresources` variables, `pywal` and `colorer` (my [colorscheme management engine](https://github.com/ngynLk/colorer)).

## 📓 How it works

The module uses two different algorithms: 
+ pixel by pixel (default): goes through each pixel and replaces it with the right color from the colorscheme
+ average box: calculates the average color of each pixel before processing. This one gives smoother and better results in some cases.

Average                          | Pixel by pixel
:-------------------------------:|:-----------------------------:
![Average](Demo/montage_avg.png) | ![Original](Demo/montage.png)


### Usage

```
usage: ImageColorizer [-h] [-x] [-c COLORSCHEME] [-w] [-p COLOR [COLOR ...]] [-s]
                      [-b] [--average BOX_SIZE] [--no_quantize]
                      input output

positional arguments:
  input                 File to generate image from.
  output                File to generate image to.

optional arguments:
  -h, --help            show this help message and exit
  -x, --xresources      Get palette from Xresources.
  -c COLORSCHEME, --colorer COLORSCHEME
                        Get palette from colorer.
  -w, --pywal
                        Gets palette from pywal.
  -p COLOR [COLOR ...], --palette COLOR [COLOR ...]
                        Manually set colors.
  -s, --show            Show image using xdg-open when image is generated.
  -b, --blur            Blur the image
  --average BOX_SIZE    Use average algorithm (calculate the average color of
                        each pixel with the pixels around) to generate the
                        wallpaper, and set the size of the box to calculate
                        the color from
  --no_quantize         Do not quantize the image before processing (may make
                        the image look better)

```

### Examples

```shell
ImageColorizer a.jpg output.jpg -x # Generate the wallpaper from colors of the currently used ~/.Xresources or ~/.Xdefaults file
ImageColorizer a.jpg output.jpg -c ~/Configuration/colorschemes/nord # Generate the wallpaper using colorscheme nord from colorer
ImageColorizer a.jpg output.jpg -c ~/Configuration/colorschemes/nord --average 2 # Use average algorithm with box size of 2
ImageColorizer a.jpg output.jpg -c ~/Configuration/colorschemes/nord --average 2 -s # Show image at the end
ImageColorizer a.jpg output.jpg -p "#3b4252" "#bf616a" "#a3be8c" -s # Use these colors.
```

## 💻 Installation

Clone the repo and run `./install.sh` (or `pip3 install .`)

## ✔️ Todo

- [ ] Multi-threading
- [ ] More colorscheme importing options

## ❎ Troubleshoot

Any common fixes to any errors will be added here.

## 👍 Credits

Heavily inspired by [ImageGoNord](https://github.com/Schrodinger-Hat/ImageGoNord-pip).
