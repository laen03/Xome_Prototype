import os
import io
import openai
from flask import Flask
from PIL import Image
openai.api_key = "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"


app = Flask(__name__)
"""
@app.route('/generation')
def index():
    try:
        response = openai.Image.create(
            prompt = "a cat fishing on a lake, cartoon style",
            n = 1,
            size ="512x512"
        )
        return response.data[0].url
    except openai.error.InvalidRequestError:
        return "Error de conexión"
"""

@app.route('/edit')
def index():
    image = Image.open("Img4.png")
    width, height = 256, 256
    image = image.resize((width, height))
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    maskImg = Image.open("Mask.png")
    maskImg = maskImg.resize((width, height))
    byte_streamMask = io.BytesIO()
    maskImg.save(byte_streamMask, format='PNG')
    byte_arrayMask = byte_streamMask.getvalue()

    response = openai.Image.create_edit(
        image=byte_array,
        mask=byte_arrayMask,
        prompt = "A photo of a colonial stylehouse, outdoors in PA, sunny day, summer, with a pool on the frontyard",
        n = 5,
        size="1024x1024"
    )
    return response.data


"""
@app.route('/variation')
def index():
    image = Image.open("Img1.png")
    width, height = 256, 256
    image = image.resize((width, height))
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    response = openai.Image.create_variation(
        image=byte_array,
        #prompt = "A two-story house with a garden with a fountain",
        n = 4,
        size="512x512"
    )
    return response.data
"""

if __name__ == "__main__":
    app.run(debug=True)