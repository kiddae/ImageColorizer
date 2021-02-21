from PIL import Image, ImageColor, ImageFilter
from subprocess import run
from math import sqrt


class ImageColorizer:
    def __init__(self):
        self.palette = []
        self.use_average = False

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

    def _color_difference(self, color1, color2):
        return sum([abs(c2-c1) for c1, c2 in zip(color1, color2)])

    def set_average(self, bool, box_size=2):
        """
        Use average algorithm or not, and set the box size to use for it.
        + bool (bool): whether to use it or not.
        + box_size (int): size of the box for the average algorithm
        """
        self.use_average = bool
        self.avg_box_size = box_size

    def _average_color(self, pixels, x, y):
        """
        Return the average color of a pixel and the pixels around it.
        + pixels (raw PIL image): pixels to operate on
        + x (int): x coord. of pixel
        + y (int): y coord. of pixel
        """
        # list_r = list_g = list_b = []
        # r = g = b = 0

        # for i in range(-self.avg_box_size, self.avg_box_size+1):
        #     for j in range(-self.avg_box_size, self.avg_box_size+1):
        #         try:
        #             pixel = pixels[x+i, y+j]
        #             list_r.append(pixel[0])
        #             list_g.append(pixel[1])
        #             list_b.append(pixel[2])
        #         except IndexError:
        #             pass

        # r = sum(list_r)//len(list_r)
        # g = sum(list_g)//len(list_g)
        # b = sum(list_b)//len(list_b)

        # return (r, g, b)
        average_sum = []
        for k in range(-self.avg_box_size, self.avg_box_size+1):
            for l in range(-self.avg_box_size, self.avg_box_size+1):
                try:
                    average_sum.append(pixels[x+k, y+l])
                except:
                    pass

        size = len(average_sum)

        r = 0
        g = 0
        b = 0

        for x in average_sum:
            r += x[0]
            g += x[1]
            b += x[2]

        avg_color = (int(r/size), int(g/size), int(b/size))
        return avg_color

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
        original_img = img.copy()
        original_pixels = original_img.load()
        original_img.close()
        # Loop through every pixel
        for x in range(width):
            for y in range(height):
                if self.use_average:
                    current_pixel = self._average_color(original_pixels, x, y)
                else:
                    current_pixel = pixels[x, y]
                if (current_pixel in checked_colors):
                    new_color = checked_colors[current_pixel]
                else:
                    # Getting the differences between color of pixel(x, y) and colors from the palette
                    differences = [
                        (self._color_difference(current_pixel, i), i) for i in self.palette]
                    # Choose the color of which difference is the least
                    new_color = min(differences)[1]
                    # Add it to checked_colors
                    checked_colors[current_pixel] = new_color
                # Replacing the current pixel with the color from the palette
                pixels[x, y] = new_color
                counter += 1
                # Progress
                print('Progress: {:.2f}%'.format(
                    counter/limit*100), end='\r')
        # img = img.filter(ImageFilter.GaussianBlur(1))
        # Export the image
        img.save(output)
        # Show it
        if show:
            run('xdg-open {}'.format(output), shell=True)
