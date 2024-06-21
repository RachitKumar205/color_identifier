# Urine Strip Colour Detection

### Link to the frontend: 

https://github.com/RachitKumar205/color_identifier_frontend

## Overview

This project is the backend for the urine strip colour detection project. It is built using Django and OpenCV to process images and detect colors. The project includes an API endpoint to process images and return the detected colors.

## Dependencies

- Python
- Django
- Django Rest Framework
- OpenCV
- Numpy
- Sklearn

## Project Structure

The project is structured as a standard Django project with the following main components:

- `settings.py`: Contains the configuration settings for the Django project.
- `urls.py`: Defines the URL routes for the project.
- `views.py`: Contains the view functions that handle HTTP requests and responses.

### `settings.py`

This file contains the configuration settings for the Django project. It includes settings for the database, installed apps, middleware, templates, and more.

### `urls.py`

This file defines the URL routes for the project. It includes routes for the admin site and the API endpoints.

### `views.py`

This file contains the view functions that handle HTTP requests and responses. It includes a function to process images and detect colors.

## Key Functions

### `process_image(request)`

This function handles POST requests to process an image. It checks if an image file is included in the request, saves the image temporarily, reads the image using OpenCV, processes the image to detect colors, deletes the temporary file, and returns the detected colors in the response.

### `detect_colors(image)`

This function processes an image to detect colors. It preprocesses the image, defines regions of interest (ROIs) for each color strip, converts each ROI to the HSV color space, gets the median color of each ROI, converts the median color back to RGB, and returns a dictionary of the detected colors.

### `preprocess_image(image)`

This function preprocesses an image for color detection. It resizes the image, converts it to the HSV color space, applies CLAHE to the V channel, increases saturation, merges the enhanced S and V channels with the original H channel, and converts the image back to the BGR color space.

## Setup

Install all the dependencies using the following command:

```bash
pip install -r requirements.txt
```

Run the server with `python manage.py runserver`

## Usage

To use the Color Identifier project, send a POST request to the `/api/process_image` endpoint with an image file included in the request body: `{"image":the image file}`. The response will include a dictionary of the detected colors.
