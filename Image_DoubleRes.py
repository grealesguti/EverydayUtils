import argparse
from skimage.transform import resize
import cv2

def double_resolution(lr_image_path, hr_image_path):
  # Load the low-resolution image
  lr_image = cv2.imread(lr_image_path)

  # Use cv2.resize() to create a high-resolution version of the image
  hr_image = cv2.resize(lr_image, (0,0), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

  # Save the high-resolution image
  cv2.imwrite(hr_image_path, hr_image)

def double_resolution(lr_image_path, hr_image_path):
  # Load the low-resolution image
  lr_image = imread(lr_image_path)

  # Use resize() to create a high-resolution version of the image
  hr_image = resize(lr_image, (lr_image.shape[0] * 2, lr_image.shape[1] * 2),
                    mode='reflect', anti_aliasing=True, order=3)

  # Save the high-resolution image
  imsave(hr_image_path, hr_image)

def parse_args():
  # Create an argument parser
  parser = argparse.ArgumentParser(description='Double the resolution of an image')

  # Add arguments to the parser
  parser.add_argument('lr_image_path', help='Path to the low-resolution image')
  parser.add_argument('hr_image_path', help='Path to the output high-resolution image')
  parser.add_argument('--method', choices=['cv2', 'skimage'], default='cv2',
                      help='Interpolation method to use (cv2 or skimage)')

  # Parse the arguments
  args = parser.parse_args()

  # Return the parsed arguments
  return args


# Parse the command-line arguments
args = parse_args()

if args.method == 'cv2':
  double_resolution_cv2(args.lr_image_path, args.hr_image_path)
elif args.method == 'skimage':
  double_resolution_skimage(args.lr_image_path, args.hr_image_path)
