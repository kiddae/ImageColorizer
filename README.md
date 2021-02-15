# Generate wallpapers and images using `ImageColorizer`!

It's a Python module and a CLI tool that you can easily use to colorize wallpapers for them to fit a colorscheme.
Currently supports importing colorschemes from `Xresources` and `colorer` (my [colorscheme management engine](https://github.com/ngynLk/colorer)).

Using the OneDark colorscheme:

![Colorscheme](Demo/Onedark.png)

![Image](Demo/demo1.jpg)

![Image2](Demo/demo2.jpg)

![Image3](Demo/montage.png.jpg)

# Usage

```
usage: ImageColorizer [-h] [-i INPUT] [-o OUTPUT] [-x] [-c] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File to generate image from.
  -o OUTPUT, --output OUTPUT
                        File to generate image to.
  -x, --xresources      Get palette from Xresources.
  -c, --colorer         Get palette from colorer
  -s, --show            Show image using xdg-open when image is generated.
```

# Installation

Clone the repo and run `./install.sh`. You can also run `pip3 install -e .`

# Todo

+ Implement multi-threading (I don't have enough knowledge yet to do it)
+ More colorscheme importing options

# Troubleshoot

Any common fixes to any errors will be added here.

# Credits

Heavily inspired by [ImageGoNord](https://github.com/Schrodinger-Hat/ImageGoNord-pip)
