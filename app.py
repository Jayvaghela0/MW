import os
import requests
from flask import Flask, request, send_file
from rembg import remove

app = Flask(__name__)

# Model Path
MODEL_PATH = "u2net.onnx"

# Model Auto-Download
MODEL_URL = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

if not os.path.exists(MODEL_PATH):
    print("🔄 Downloading U2-Net Model...")
    response = requests.get(MODEL_URL, stream=True)
    with open(MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    print("✅ Model Downloaded Successfully!")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return "No file uploaded", 400

    image_file = request.files["image"]
    input_image = image_file.read()

    # Process Image with rembg
    output_image = remove(input_image)

    # Save & Send Processed Image
    output_path = "output.png"
    with open(output_path, "wb") as f:
        f.write(output_image)

    return send_file(output_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
