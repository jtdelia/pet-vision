from flask import Flask, request, jsonify
import json
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
import os


#load the model here.
processor = BlipProcessor.from_pretrained("/app/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("/app/blip-vqa-base")

app = Flask(__name__)

# Health check at /
@app.route("/", methods=["GET", "POST"])
def health_check():
    return jsonify({"status": "OK"}), 200

@app.route("/inference", methods=["POST"])
def classify_pet():
    """
    This function will retrieve the image in image_url value extracted from the request body and 
    then infer using a vision model what kind of pet the animal is and its breed.

    Args:
        id, image_url.
    Returns:
        The id, petType, petBreed
    """
    
    headers = dict(request.headers)
    try:
        body = request.get_json()
        id = body.get("id")
        image_url = body.get("image_url")
    except Exception as e:
        print(f"Error parsing JSON body: {e}")
        return jsonify({"error": "Invalid JSON body"}), 400

    # check that image_url is a jpeg or png
    if not image_url.lower().endswith((".jpg", ".jpeg", ".png")):
        return jsonify({"error": "Invalid image URL. Must be a JPG or PNG."}), 400
    
    img_url = image_url
    print(f'Image URL: {img_url}')
    
    try:
        raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return jsonify({"error": "Error opening image"}), 400
    

    question = "what kind of animal is this?"
    inputs = processor(raw_image, question, return_tensors="pt")

    out = model.generate(**inputs)
    petType = processor.decode(out[0], skip_special_tokens=True)

    question = f'what breed of {petType}?'
    inputs = processor(raw_image, question, return_tensors="pt")

    out = model.generate(**inputs)
    petBreed = processor.decode(out[0], skip_special_tokens=True)

    print(json.dumps({"petType": petType, "petBreed": petBreed}, indent=4))

    return (jsonify({"id": id, "petType": petType, "petBreed": petBreed}),200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
