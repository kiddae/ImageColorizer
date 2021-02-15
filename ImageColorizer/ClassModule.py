from PIL import Image, ImageColor
from subprocess import run
from math import sqrt


class ImageColorizer:
    def __init__(self):
        self.palette = []

    def load_palette(self, values):
        """
        Load a palette to generate wallpapers from.
        + values (list): color palette, either as a hex code '#ffffff' or RGB tuple (255, 255, 255)
        """
        for i in values:
            try:
                self.palette.append(ImageColor.getcolor(i, "RGB"))
            except ValueError:
                continue

    def _color_difference(self, a, b):
        return sqrt(sum(([(c2-c1)**2 for c1, c2 in zip(a, b)])))

    def generate(self, input, output, show=False):
        """
        Generate the image.
        + input (str): path to image to generate from
        + output (str): path to file to save image to
        + show (bool): show the image at the end using the default image-viewer
        """
        if self.palette == []:
            raise ValueError("Palette is empty")
        # Load image
        img = Image.open(input)
        width, height = img.width, img.height
        # To show progress
        counter = 0
        limit = width*height
        # Already checked colors for better performance
        checked_colors = {}
        # Get the pixels from the image
        pixels = img.load()
        # Loop through every pixel
        for x in range(width):
            for y in range(height):
                pixel = pixels[x, y]
                if (pixel in checked_colors):
                    new_color = checked_colors[pixel]
                else:
                    # Getting the differences between color of pixel(x, y) and colors from the palette
                    differences = [
                        [self._color_difference(pixel, i), i] for i in self.palette]
                    differences.sort()
                    # Choose the color of which difference is the least
                    new_color = differences[0][1]
                    # Add it to checked_colors
                    checked_colors[pixel] = new_color
                # Replacing the current pixel with the color from the palette
                pixels[x, y] = new_color
                counter += 1
                # Progress
                print('Progress: {}%'.format(
                    round(counter/limit*100, 2)), end='\r')
        # Export the image
        img.save(output)
        # Show it
        if show:
            run('xdg-open {}'.format(output), shell=True)
