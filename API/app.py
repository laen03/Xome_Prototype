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
import random


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
        
        usePrompt1 = random.choice([False, True])
        prompt = "A charming "
        
        places = {
            "Utah":"Salt Lake", 
            "Florida":"Miami", 
            "New York": "Brooklyn", 
            "Pennsylvania": "Philadelphia"
        }
        state, district = random.choice(list(places.items()))
        prompt2 = "Create a color photography taken from the street in " + state + " of "
        # Number of rooms
        rooms = str(len(property["rooms"]))
        prompt += rooms + "-room, "
        
        # Property size
        buildingSize = str(property["buildingSize"])
        prompt += buildingSize + " sq. ft. "
        
        
        # Property value
        propertyValue = property["expectedValue"]


        # barata 0-250 000
        # medio: 250 001 - 700 000
        # alto: 700 001 - en adelante
        
        
        propertyType = property["propertyType"]
        if propertyType == "MOBILE":
            weather = ["a summer", "a winter", "a cloudy", "an overcast"]
            prompt = prompt2 = "A cozy, weathered mobile home nestled in a nice neighborhood surrounded by other mobile houses, with a clear blue sky overhead. The photo was taken from the street in " + random.choice(weather) + " day"
        else:
            # "Cheap" properties
            if propertyValue <= 250000:
                if propertyType == "SINGLE":
                    prompt2 += "an old, one-story house built in 1971, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                    prompt = prompt2
                elif propertyType == "DUPLEX":
                    prompt2 += "an old, two-story house built in 1971, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                    prompt = prompt2
                elif propertyType == "TOWNHOUSE":
                    prompt2 += "a townhouse, with cheap facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban low class architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles."
                    prompt = prompt2
            
            # "Mid-range" properties
            elif propertyValue > 250000 and propertyValue <= 700000:
                # "Cheap" properties
                if int(rooms) > 10:
                    if propertyType == "SINGLE":
                        prompt2 += "an old, one-story house built in 1971, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                        prompt = prompt2
                    elif propertyType == "DUPLEX":
                        prompt2 += "an old, two-story house built in 1971, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                        prompt = prompt2
                    elif propertyType == "TOWNHOUSE":
                        prompt2 += "a townhouse, with cheap facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban low class architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles."
                        prompt = prompt2

                # "Expensive" properties
                elif int(rooms) <= 10:
                    if propertyType == "SINGLE":
                        prompt += "single-family house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
                    
                        prompt2 += "an new, one-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                    elif propertyType == "DUPLEX":
                        prompt += "duplex house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
                        
                        prompt2 += "an new, two-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                    elif propertyType == "TOWNHOUSE":
                        prompt += "brick townhouse, nestled in a tree-lined street, with unique architectural details that add character and charm. The sun is shining and the photo is taken from the street."
                        
                        prompt2 += "a townhouse, with elegant facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles."

            # "Expensive" properties
            else:
                if propertyType == "SINGLE":
                    prompt += "single-family house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
                    
                    prompt2 += "an new, one-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                elif propertyType == "DUPLEX":
                    prompt += "duplex house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday."
                    
                    prompt2 += "an new, two-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery."
                elif propertyType == "TOWNHOUSE":
                    prompt += "brick townhouse, nestled in a tree-lined street, with unique architectural details that add character and charm. The sun is shining and the photo is taken from the street."
                    
                    prompt2 += "a townhouse, with elegant facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles."
        
        if usePrompt1:
            if  propertyType != "TOWNHOUSE":
                finalPrompt = prompt
            else:
                finalPrompt = prompt2
            
        else:
            finalPrompt = prompt2
        
            
                    
        try:
            response = openai.Image.create(
                prompt = finalPrompt,
                n = 3,
                size ="512x512"
            )
            
            
            for url in response.data:
                file_name = url["url"].split("/")[6].split("?")[0].split(".")[0]
                print(file_name)
                try:
                    image_content = requests.get(url["url"]).content
                    image_file = io.BytesIO(image_content)
                    image = Image.open(image_file)
                    file_path = "images/" + file_name + ".jpeg"

                    with open(file_path, "wb") as f:
                        image.save(f, "JPEG", quality = 35, optimize=True)

                    print("Success")
                except Exception as e:
                    print('FAILED -', e)
        except openai.error.InvalidRequestError as e:
            return str(e)
        print(finalPrompt)

    # Closing file
    f.close()

    return str(prompt)

@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


if __name__ == "__main__":
    app.run(debug=True)