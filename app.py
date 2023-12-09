from flask import Flask, request, jsonify
import requests
from PIL import Image
import pytesseract
from io import BytesIO

app = Flask(__name__)


@app.route('/', methods=['POST'])
def transcribe_image():
    image_url = request.json.get('image_url')
    if not image_url:
        return jsonify({'error': 'No image URL provided'}), 400

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Error fetching image'}), 500

        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image, lang='pol')

        return jsonify({'transcription': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
