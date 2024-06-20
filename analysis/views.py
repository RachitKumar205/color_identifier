import cv2
import numpy as np
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .serializers import ImageUploadSerializer, ColorResultSerializer
from sklearn.cluster import KMeans


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def process_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ImageUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    image_file = request.FILES['image']

    # Save the uploaded file temporarily
    temp_path = default_storage.save('temp_images/temp.jpg', ContentFile(image_file.read()))
    full_temp_path = os.path.join(default_storage.location, temp_path)

    # Read image using OpenCV
    image = cv2.imread(full_temp_path)

    if image is None:
        default_storage.delete(temp_path)
        return Response({'error': 'Unable to read the image file'}, status=status.HTTP_400_BAD_REQUEST)

    # Process image and detect colors
    colors = detect_colors(image)

    # Delete the temporary file
    default_storage.delete(temp_path)

    # Validate the results
    result_serializer = ColorResultSerializer(data=colors)
    if not result_serializer.is_valid():
        return Response(result_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(result_serializer.validated_data)


def detect_colors(image):
    # Preprocess the image
    preprocessed = preprocess_image(image)

    # Define the regions of interest (ROI) for each color strip
    height, width = preprocessed.shape[:2]
    strip_height = height // 10
    strip_width = width // 4  # Use only the middle quarter of the strip width
    x_start = 3 * width // 8  # Start from 3/8 of the width

    colors = {}
    color_names = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']

    for i, name in enumerate(color_names):
        y_start = i * strip_height + strip_height // 4
        roi = preprocessed[y_start:y_start + strip_height // 2, x_start:x_start + strip_width]

        # Convert ROI to HSV color space
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Get median color
        median_color = np.median(hsv_roi.reshape(-1, 3), axis=0)

        # Convert back to BGR and then to RGB
        median_color_bgr = cv2.cvtColor(np.uint8([[median_color]]), cv2.COLOR_HSV2BGR)[0][0]
        median_color_rgb = median_color_bgr[::-1]

        colors[name] = median_color_rgb.tolist()

    return colors


def preprocess_image(image):
    # Resize the image to a standard size
    resized = cv2.resize(image, (300, 600))

    # Convert to HSV color space
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # Split the HSV image into H, S, and V channels
    h, s, v = cv2.split(hsv)

    # Apply CLAHE to V channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cv = clahe.apply(v)

    # Increase saturation
    s = cv2.add(s, 30)

    # Merge the enhanced S and V channels with the original H channel
    enhanced_hsv = cv2.merge((h, s, cv))

    # Convert back to BGR color space
    enhanced = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    return enhanced