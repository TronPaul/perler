from perler import app
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('palette')
    parser.add_argument('--no_crop', action='store_false')
    args = parser.parse_args()
    app.image_to_perler_pdf(args.image, args.palette, args.no_crop)

if __name__ == '__main__':
    main()