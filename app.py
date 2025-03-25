import os
import requests
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for cross-origin requests

# Model Path
MODEL_PATH = "u2net.onnx"

# Model Auto-Download
MODEL_URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

# 🔄 Check if model exists, else download it
if not os.path.exists(MODEL_PATH):
    print("🔄 Downloading U2-Net Model...")
    response = requests.get(MODEL_URL, stream=True)
    with open(MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print("✅ Model Downloaded Successfully!")

@app.route("/")
def home():
    return jsonify({"message": "Welcome to AI Background Remover API!"})

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image_file = request.files["image"]
    input_image = image_file.read()

    try:
        # Process Image with rembg
        output_image = remove(input_image)

        # Save & Send Processed Image
        output_path = "output.png"
        with open(output_path, "wb") as f:
            f.write(output_image)

        return send_file(output_path, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
