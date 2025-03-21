from flask import Flask, request, send_file, render_template_string
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

# 網頁介面
INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube 轉 MP3</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        input[type="text"] { width: 80%; max-width: 400px; padding: 10px; }
        input[type="submit"] { padding: 10px 20px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>輸入 YouTube 網址下載 MP3</h1>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="貼上 YouTube 網址">
        <br>
        <input type="submit" value="下載 MP3">
    </form>
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(INDEX_HTML, message=None)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if not url:
        return render_template_string(INDEX_HTML, message="請輸入有效的 YouTube 網址！")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
        }
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return render_template_string(INDEX_HTML, message=f"錯誤: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)