import cv2

def extract_line_points(image):
  # Convert the image to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  # Apply Canny edge detection
  edges = cv2.Canny(gray, 50, 150)
  
  # Find the lines using Hough transform
  lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
  
  # Initialize an empty list to store the points
  points = []
  
  # Iterate over the lines and extract the points
  for line in lines:
    x1, y1, x2, y2 = line[0]
    points.append((x1, y1))
    points.append((x2, y2))
  
  # Return the points
  return points
