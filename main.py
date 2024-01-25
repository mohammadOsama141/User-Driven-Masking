from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
from PIL import Image

app = Flask(__name__)

# Load and prepare the image
raw_image = Image.open('static/img.png').convert("RGB")
image_height, image_width = raw_image.size
mask = np.zeros((image_width, image_height), dtype=np.uint8)  # Initialize mask

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/draw_mask', methods=['POST'])
def draw_mask():
    data = request.json
    point = data['point']
    action = data['action']  # 'add' or 'remove'
    brush_size = 10  # Adjust brush size as needed

    # Update mask
    if action == 'add':
        cv2.circle(mask, (int(point['x']), int(point['y'])), brush_size, 1, -1)
    elif action == 'remove':
        cv2.circle(mask, (int(point['x']), int(point['y'])), brush_size, 0, -1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (brush_size, brush_size))
    mask_dilated = cv2.dilate(mask, kernel)

    # Apply mask to image
    orig_img = np.array(raw_image)
    mask_img = np.stack([mask_dilated * 255] * 3, axis=-1)
    final_img = cv2.addWeighted(orig_img, 1, mask_img, 0.5, 0)
    final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)

    # Save the combined image
    result_path = 'static/result.png'
    cv2.imwrite(result_path, final_img)

    # Save the mask image
    mask_path = 'static/mask.png'
    cv2.imwrite(mask_path, mask_dilated * 255)  # Save mask as a black & white image

    return jsonify({'image_path': result_path, 'mask_path': mask_path})


if __name__ == '__main__':
    app.run(debug=True)