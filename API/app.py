import os
import io
import openai
import json
import requests
from flask import Flask
from flask_cors import CORS
from flask import url_for
from flask import request
from PIL import Image


openai.api_key = "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"

'''
Api Key backup account
openai.api_key = "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"
'''

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    try:
        data = request.args.get('prompt')
        print(data)
        response = openai.Image.create(
            prompt = data,
            n = 3,
            size ="512x512"
        )
        return response.data
    except openai.error.InvalidRequestError as e:
        return str(e)


@app.route('/edit')
def edit():
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



@app.route('/variation')
def variation():
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


PATH = "C:\\Users\\Journey Admin\\OneDrive - Icrave Design\\Projects\\Python\\Xome\\API"

@app.route('/read')
def readJson():
    # Opening JSON file
    f = open('data.json')
    
    # returns JSON object as 
    # a dictionary
    properties = json.load(f)
    
    # Iterating through the json
    # list
    
    # A house photography taken from the street, two-story single family house, 2 bedrooms, outdoors, 
    # summer day in Jackson city, extreme long-shot on iPhone 6
    
    for property in properties:
        prompt = "A charming "
        
        # Number of rooms
        rooms = str(len(property["rooms"]))
        prompt += rooms + "-room, "
        
        # Property size
        buildingSize = str(property["buildingSize"])
        prompt += buildingSize + " sq. ft. "
        
        propertyType = property["propertyType"]
        if propertyType == "SINGLE":
            prompt += "single-family house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
        elif propertyType == "DUPLEX":
            prompt += "duplex house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
        elif propertyType == "TOWNHOUSE":
            prompt += "brick townhouse, nestled in a tree-lined street, with unique architectural details that add character and charm. The sun is shining and the photo is taken from the street."
        elif propertyType == "MOBILE":
            continue
        try:
            response = openai.Image.create(
                prompt = prompt,
                n = 4,
                size ="512x512"
            )
            
            
            for url in response.data:
                file_name = url["url"].split("/")[6].split("?")[0].split(".")[0]
                print(file_name)
                try:
                    image_content = requests.get(url["url"]).content
                    image_file = io.BytesIO(image_content)
                    image = Image.open(image_file)
                    file_path = "images/" + file_name + ".png"

                    with open(file_path, "wb") as f:
                        image.save(f, "PNG")

                    print("Success")
                except Exception as e:
                    print('FAILED -', e)
        except openai.error.InvalidRequestError as e:
            return str(e)

    # Closing file
    f.close()

    return str(prompt)

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


if __name__ == "__main__":
    app.run(debug=True)