# Interactive Brush Masking

## About the Project
Interactive Brush Masking is a web-based application that allows users to interactively create masks on images using a brush-like tool. This project is built using Flask, a Python web framework, and incorporates HTML, JavaScript, and OpenCV for image processing. Users can click and drag their mouse over the image to draw a mask, which is updated in real-time.

## Features
Real-Time Interaction: Users can draw on an image to create a mask, seeing the results of their actions immediately.
User-Driven Masking: The masking process is entirely controlled by the user, offering a high degree of precision.
Image and Mask Output: The application outputs both the original image with the mask applied and a separate mask image.
How It Works
The application uses Flask to serve a webpage where an image is displayed. JavaScript is used to capture mouse events when a user clicks and drags on the image. These points are sent to the Flask server, which uses OpenCV to create and update a mask based on the user's input. The mask is then applied to the original image, and both the masked image and the mask itself are saved and updated on the webpage.
