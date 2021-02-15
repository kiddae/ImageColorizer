import subprocess
from .ClassModule import ImageColorizer
import argparse


def output(command):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='File to generate image from.')
    parser.add_argument('-o', '--output', help='File to generate image to.')
    parser.add_argument(
        '-x', '--xresources', help='Get palette from Xresources.', action='store_true')
    parser.add_argument(
        '-c', '--colorer', help='Get palette from colorer', action='store_true')
    parser.add_argument(
        '-s', '--show', help='Show image using xdg-open when image is generated.', action='store_true')
    args = parser.parse_args()

    img_col = ImageColorizer()

    values = []
    if args.xresources:
        values = output('xrdb -query | cut -f 2').split('\n')
    elif args.colorer:
        values = output('colorer --get all').split('\n')
    img_col.load_palette(values)

    img_col.generate(args.input, args.output, show=args.show)


if __name__ == '__main__':
    main()
