from PIL import Image, ImageColor, ImageFilter
from subprocess import run


class ImageColorizer:
    def __init__(self):
        self.palette = []
        self.use_average = False

    # Utilities
    def _color_difference(self, color1, color2):
        return sum([abs(c2-c1) for c1, c2 in zip(color1, color2)])

    def _average_color(self, pixels, x, y):
        """
        Return the average color of a pixel and the pixels around it.
        + pixels (raw PIL image): pixels to operate on
        + x (int): x coord. of pixel
        + y (int): y coord. of pixel
        """
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

    def _quantize(self, image):
        """
        Generates the image using quantize algorithm.
        """
        palette_data = []
        for i in self.palette:
            palette_data.extend(i)

        img_palette = Image.new('P', (1, 1))
        img_palette.putpalette(palette_data)

        quantized_image = image.quantize(
            colors=256, method=0, kmeans=5, palette=img_palette)
        quantized_image = quantized_image.convert('RGB')
        return quantized_image

    # Functions
    def load_palette(self, values):
        """
        Load a palette to generate wallpapers from.
        + values (list): color palette, either as a hex code '#ffffff' or RGB tuple (255, 255, 255)
        """
        if values is None or values == []:
            raise ValueError("No values given for the palette.")
        for i in values:
            try:
                self.palette.append(ImageColor.getcolor(i, "RGB"))
            except ValueError:
                continue

    def set_average(self, bool, box_size=2):
        """
        Use average algorithm or not, and set the box size to use for it.
        + bool (bool): whether to use it or not.
        + box_size (int): size of the box for the average algorithm
        """
        self.use_average = bool
        self.avg_box_size = box_size

    def generate(self, input, output, show=False, blur=False, quantize=True):
        """
        Generate the image with the pixel/average algorithm.
        """
        # Load image
        image = Image.open(input)
        width, height = image.width, image.height
        # Quantize image first
        if quantize:
            image = self._quantize(image)
        # To show progress
        counter = 0
        limit = width*height
        # Already checked colors for better performance
        checked_colors = {}
        # Get the pixels from the image
        pixels = image.load()
        original_img = image.copy()
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
        if blur:
            image = image.filter(ImageFilter.GaussianBlur(1))
        # Export the image
        image.save(output, quality=100, subsampling=0)
        # Show it
        if show:
            run('xdg-open {}'.format(output), shell=True)
