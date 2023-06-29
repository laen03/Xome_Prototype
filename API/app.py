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

def concatenateJSONs():
    highSeedArrayJSON = open('highSeedArray.json')
    lowSeedArrayJSON = open('lowSeedArray.json')
    
    mediumSeedArray1JSON = open('mediumSeedArray1.json')
    mediumSeedArray2JSON = open('mediumSeedArray2.json')
    
    
    highSeedArray = json.load(highSeedArrayJSON)
    lowSeedArray = json.load(lowSeedArrayJSON)
    
    mediumSeedArray1 = json.load(mediumSeedArray1JSON)
    mediumSeedArray2 = json.load(mediumSeedArray2JSON)
    
    properties = []
    properties.extend(highSeedArray)
    properties.extend(lowSeedArray)
    properties.extend(mediumSeedArray1)
    properties.extend(mediumSeedArray2)
    
    return properties


def converMultiHouse():
    tempList = ["TOWNHOUSE", "DUPLEX"]
    # hacer random para que elija entre townhouse y duplex
    return random.choice(tempList)


@app.route('/read')
def readJson():
    concatenateJSONs()
    

    # Opening JSON file
    f = open('data.json')
    
    # returns JSON object as 
    # a dictionary
    #properties = json.load(f)
    
    properties = concatenateJSONs()
    
    # Iterating through the json
    # list
    
    # A house photography taken from the street, two-story single family house, 2 bedrooms, outdoors, 
    # summer day in Jackson city, extreme long-shot on iPhone 6
    
    for property in properties:
        print("*****************************************************")
        usePrompt1 = random.choice([False, True])
        prompt = "A charming "
        
        places = {
            "Utah":"Salt Lake", 
            "Florida":"Miami", 
            "New York": "Brooklyn", 
            "Pennsylvania": "Philadelphia",
            "New Mexico": "Albuquerque"
        }
        state, district = random.choice(list(places.items()))
        prompt2 = "A photography taken from the street in " + state + " of "
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
        print(propertyType)
        print(propertyValue)
        if propertyType == "MOBILE":
            weather = ["a summer", "a winter", "a cloudy", "an overcast"]
            prompt = "A cozy, weathered mobile home nestled in a nice neighborhood surrounded by other mobile houses, with a clear blue sky overhead. The photo was taken from the street in " + random.choice(weather) + " day by a skilled photographer with a professional-grade DSLR camera."
            prompt2 = prompt
        else:
            if property["propertyType"] == "MULTI":
                propertyType = converMultiHouse()
            # "Cheap" properties
            if propertyValue <= 250000:
                print("barato")
                if propertyType == "SINGLE":
                    prompt2 += "a low-cost, one-story house built in 80's, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                    prompt = prompt2
                elif propertyType == "DUPLEX":
                    prompt2 += "a low-cost, two-story house built in 80's, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                    prompt = prompt2
                elif propertyType == "TOWNHOUSE":
                    prompt2 += "a townhouse, with cheap facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban low class architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles. The photo was captured by a skilled photographer with a professional-grade DSLR camera"
                    prompt = prompt2
                elif propertyType == "CONDO":
                    prompt2 += "a low-cost, condo property from " + state + ", captured by a skilled photographer with a professional-grade DSLR camera, on a cloudy day."
                    prompt = prompt2
            
            # "Mid-range" properties
            elif propertyValue > 250000 and propertyValue <= 700000:
                # "Cheap" properties
                if int(rooms) > 10:
                    print("barato")
                    if propertyType == "SINGLE":
                        prompt2 += "a low-cost, one-story house built in 80's, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                        prompt = prompt2
                    elif propertyType == "DUPLEX":
                        prompt2 += "a low-cost, two-story house built in 80's, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                        prompt = prompt2
                    elif propertyType == "TOWNHOUSE":
                        prompt2 += "a townhouse, with cheap facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban low class architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles. The photo was captured by a skilled photographer with a professional-grade DSLR camera."
                        prompt = prompt2
                    elif propertyType == "CONDO":
                        prompt2 += "a low-cost, condo property from " + state + ", captured by a skilled photographer with a professional-grade DSLR camera, on a cloudy day."
                        prompt = prompt2

                # "Expensive" properties
                elif int(rooms) <= 10:
                    print("caro")
                    if propertyType == "SINGLE":
                        prompt += "single-family house, featuring a welcoming porch with steps leading up and a side porch. The photo is taken from the street at midday by a skilled photographer with a professional-grade DSLR camera."
                    
                        prompt2 += "an new, one-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                    elif propertyType == "DUPLEX":
                        prompt += "duplex house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday, captured by a skilled photographer with a professional-grade DSLR camera."
                        
                        prompt2 += "an new, two-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                    elif propertyType == "TOWNHOUSE":
                        prompt += "brick townhouse, nestled in a tree-lined street, with unique architectural details that add character and charm. The sun is shining and the photo is captured from the street by a skilled photographer with a professional-grade DSLR camera."
                        
                        prompt2 += "a townhouse, with elegant facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles. The photo was captured by a skilled photographer with a professional-grade DSLR camera"
                    
                    elif propertyType == "CONDO":
                        prompt2 += "a a modern, sleek condo property from " + state + ", captured by a skilled photographer with a professional-grade DSLR camera, on a cloudy day."
                        prompt = prompt2
            # "Expensive" properties high-key lighting
            else:
                print("caro")
                if propertyType == "SINGLE":
                    prompt += "single-family house, featuring a welcoming porch with steps leading up and a side porch. The photo is taken from the street at midday by a skilled photographer with a professional-grade DSLR camera."
                
                    prompt2 += "an new, one-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                elif propertyType == "DUPLEX":
                    prompt += "duplex house, featuring a welcoming porch with steps leading up and a side porch. The image is taken from the street at midday, captured by a skilled photographer with a professional-grade DSLR camera."
                    
                    prompt2 += "an new, two-story fancy house built in 2000, nestled in a peaceful suburban neighborhood, surrounded by neat and tidy greenery, captured by a skilled photographer with a professional-grade DSLR camera."
                elif propertyType == "TOWNHOUSE":
                    prompt += "brick townhouse, nestled in a tree-lined street, with unique architectural details that add character and charm. The sun is shining and the photo is captured from the street by a skilled photographer with a professional-grade DSLR camera."
                    
                    prompt2 += "a townhouse, with elegant facade. The scene is rich with detail and character, featuring lush green trees. The image captures the essence of urban architecture in this iconic " + state + ". The prompt's careful attention to detail, composition, and mood ensures that the DALL-E model can produce stunning and high-quality images of one of " + district + "'s most iconic architectural styles. The photo was captured by a skilled photographer with a professional-grade DSLR camera"
                
                elif propertyType == "CONDO":
                    prompt2 += "a a modern, sleek condo property from " + state + ", captured by a skilled photographer with a professional-grade DSLR camera, on a cloudy day."
                    prompt = prompt2
                    
        if usePrompt1:
            if  propertyType != "TOWNHOUSE":
                finalPrompt = prompt
            else:
                finalPrompt = prompt2
            
        else:
            finalPrompt = prompt2

        print(finalPrompt)         
        try:
            response = openai.Image.create(
                prompt = finalPrompt,
                n = 2,
                size ="1024x1024"
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
                        image.save(f, "JPEG", quality = 45, optimize=True)

                    print("Success")
                except Exception as e:
                    print('FAILED -', e)
        except openai.error.InvalidRequestError as e:
            return str(e)

    # Closing file
    f.close()
    
    return str(finalPrompt)

@app.route("/resize")
def resize():
    pathIMG = "C:\\Users\\Journey Admin\OneDrive - Icrave Design\\Desktop\\Git\\Xome_Prototype\API\\resizeIMG\\"
    dir = os.listdir(pathIMG)
    try:
        for imgHQ in dir:
            print(pathIMG+imgHQ)
            img = Image.open(pathIMG+imgHQ)
            f, e = os.path.splitext(pathIMG+imgHQ)
            img.save(f + ' resized.jpeg', 'JPEG', quality=30, optimize=True)
            print("actualizado")
    except:
        print("error")
    return "Succes"



@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


if __name__ == "__main__":
    app.run(debug=True)