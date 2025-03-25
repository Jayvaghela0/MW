from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import onnxruntime as ort
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)  # ✅ CORS Enable (Sabhi Origins Allowed Hain)

# ✅ AI Model Sirf Ek Baar Load Karein (Startup Pe)
model_path = "static/u2net.onnx"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

ort_session = ort.InferenceSession(model_path)

def remove_bg(image):
    image = image.convert("RGB")
    image = image.resize((320, 320))
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.transpose(2, 0, 1)[None, :, :, :]

    # Model Prediction
    input_name = ort_session.get_inputs()[0].name
    output = ort_session.run(None, {input_name: img_array})[0][0][0]

    # Create Mask
    mask = (output > 0.5).astype(np.uint8) * 255
    mask = cv2.resize(mask, (image.width, image.height))

    # Remove Background
    img_np = np.array(image)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2RGBA)
    img_np[:, :, 3] = mask

    return Image.fromarray(img_np)

@app.route('/')
def home():
    return jsonify({"message": "U²-Net Background Remover API is Running!"})

@app.route('/remove-bg', methods=['POST'])
def remove_bg_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = Image.open(request.files['image'])
    result = remove_bg(image)

    img_io = io.BytesIO()
    result.save(img_io, "PNG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
