from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO
from collections import Counter

app = FastAPI()

@app.post("/extract-hex")
async def extract_hex(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert('RGB')
    pixels = list(image.getdata())

    # Get the most common color
    most_common_color = Counter(pixels).most_common(1)[0][0]
    hex_color = '#{:02x}{:02x}{:02x}'.format(*most_common_color).upper()

    return {"hex": hex_color}
