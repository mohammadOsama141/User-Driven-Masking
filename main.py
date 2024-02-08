from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from PIL import Image
import numpy as np
import cv2
from pydantic import BaseModel

app = FastAPI()

# Mount the 'Images' directory to serve static files
app.mount("/Images", StaticFiles(directory="Images"), name="Images")

# Mount other directories as per Fast API requirement
@app.get("/", response_class=HTMLResponse) # FastAPI route handler for index.html
async def main():
    return FileResponse('templates/index.html')

app.mount("/static", StaticFiles(directory="static"), name="static")



# Load and prepare the image
raw_image = Image.open('Images/img.png').convert("RGB")
image_height, image_width = raw_image.size
mask = np.zeros((image_width, image_height), dtype=np.uint8)  # Initialize mask

class DrawRequest(BaseModel):
    point: dict
    action: str

@app.get("/")
async def main():
    return FileResponse('index.html')

@app.post("/draw_mask")
async def draw_mask(request: DrawRequest):
    data = request.dict()
    point = data['point']
    action = data['action']  # 'add' or 'remove'
    brush_size = 10  # Brush size

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
    result_path = 'Images/result.png'
    cv2.imwrite(result_path, final_img)

    # Save the mask image
    mask_path = 'Images/mask.png'
    cv2.imwrite(mask_path, mask_dilated * 255)  # Save mask as a black & white image

    return JSONResponse(content={'image_path': result_path, 'mask_path': mask_path})

# to run this write in the terminal: uvicorn main:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
