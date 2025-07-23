from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post("/extract-colors")
async def extract_colors(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    # Resize to speed up processing
    image = image.resize((150, 150))

    # Reduce to top 6 colors
    image = image.convert("P", palette=Image.ADAPTIVE, colors=6).convert("RGB")
    colors = image.getcolors(150 * 150)

    hex_colors = list({f"#{r:02x}{g:02x}{b:02x}" for count, (r, g, b) in colors})
    return {"hex_colors": hex_colors}
