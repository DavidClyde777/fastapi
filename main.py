from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO
from collections import defaultdict

app = FastAPI()

@app.post("/extract-colors")
async def extract_colors(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # Resize to reduce noise and speed up processing
    image = image.resize((150, 150))

    # Count pixel frequencies
    color_counts = defaultdict(int)
    for pixel in image.getdata():
        hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel)
        color_counts[hex_color] += 1

    # Filter: only keep colors that appear >= 20 times and are not black/white
    filtered_colors = [
        color for color, count in color_counts.items()
        if count >= 20 and color not in ("#ffffff", "#000000")
    ]

    return {"hex_colors": filtered_colors}
