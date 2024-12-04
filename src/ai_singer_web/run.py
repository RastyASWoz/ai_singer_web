from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = './src/ai_singer_web/static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 接收音频文件
@app.route('/recv', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200

# 发送音频文件到另一个服务器
@app.route('/send', methods=['POST'])
def send_file():
    target_url = request.json.get('target_url')
    filename = request.json.get('filename')

    if not target_url or not filename:
        return jsonify({'error': 'target_url and filename are required'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File does not exist'}), 404

    with open(filepath, 'rb') as f:
        files = {'file': ("test_"+filename, f)}
        try:
            response = requests.post(target_url, files=files)
            return jsonify({'message': 'File sent successfully', 'response': response.json()}), response.status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
