# deskew.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script reads an image, deskews it, and saves the corrected image over the original
print("Running deskew.py")
import cv2
import numpy as np
import os
import sys

def order_points(pts):
    # Order the points in the rectangle [top-left, top-right, bottom-right, bottom-left]
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def correct_skew(image_path, output_dir):
    # Read the image
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a binary threshold to the image
    _, threshold = cv2.threshold(grayscale, 127, 255, cv2.THRESH_BINARY)
    # Find contours in the threshold image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    # If the polygon has four points, it's a rectangle
    if len(approx) == 4:
        # Get the perspective transform matrix
        rect = order_points(approx.reshape(4, 2))
        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        # Apply the perspective transform to the image
        corrected = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        # Save the corrected image
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        cv2.imwrite(output_path, corrected)

# Get the directory path from the command line argument
dir_path = sys.argv[1]

# Iterate over all images in the directory
for file_name in os.listdir(dir_path):
    if file_name.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(dir_path, file_name)
        correct_skew(image_path, dir_path)  # Save the corrected image in the original directory