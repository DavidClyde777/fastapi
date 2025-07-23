from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/extract-colors")
async def extract_colors(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")
    colors = image.getcolors(maxcolors=1000000)  # returns list of (count, color)

    if not colors:
        return {"error": "Too many colors to process."}

    hex_colors = list({f"#{r:02x}{g:02x}{b:02x}" for count, (r, g, b) in colors})
    return {"hex_colors": hex_colors}
