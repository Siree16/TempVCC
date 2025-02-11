from flask import Flask, request, send_file, jsonify
import qrcode
import zbarlight
from PIL import Image
import io

app = Flask(__name__)

# QR Code Generation Endpoint
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json.get("text")
    if not data:
        return jsonify({"error": "No text provided"}), 400
    
    qr = qrcode.make(data)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

# QR Code Decoding Endpoint
@app.route('/decode_qr', methods=['POST'])
def decode_qr():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    img = Image.open(file.stream).convert('L')

    codes = zbarlight.scan_codes(['qrcode'], img)
    if not codes:
        return jsonify({"error": "No QR code detected"}), 400

    return jsonify({"text": codes[0].decode("utf-8")})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
