from perler import app
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('palette')
    args = parser.parse_args()
    app.image_to_perler_pdf(args.image, args.palette)

if __name__ == '__main__':
    main()