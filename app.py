from flask import Flask, request, jsonify, render_template_string
from googletrans import Translator
import base64
from gtts import gTTS
import io

app = Flask(__name__)
translator = Translator()

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Translation App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        #translation-form {
            width: 50%;
            margin: 40px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        #translation-output {
            margin-top: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <h1>Language Translation App</h1>
    <form id="translation-form">
        <label for="text">Enter text:</label>
        <textarea cols="50" rows="5" name="text" id="text"></textarea><br><br>
        <label for="target-language">Select target language:</label>
        <select name="target-language" id="target-language">
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="it">Italian</option>
            <option value="pt">Portuguese</option>
            <option value="zh-CN">Chinese (Simplified)</option>
            <option value="ja">Japanese</option>
            <option value="ko">Korean</option>
        </select><br><br>
        <button type="submit">Translate</button>
    </form>
    <div id="translation-output"></div>

    <script>
        document.getElementById('translation-form').addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const text = document.getElementById('text').value;
            const targetLanguage = document.getElementById('target-language').value;
            
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    target_language: targetLanguage
                })
            });
            
            const data = await response.json();
            let output = `<p>Translated Text: ${data.translated_text}</p>`;
            
            document.getElementById('translation-output').innerHTML = output;
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language')
    
    if not text or not target_language:
        return jsonify({"error": "Please provide both text and target language"}), 400
    
    # Detect the language of the input text
    detection = translator.detect(text)
    source_language = detection.lang
    
    # Translate the text to the target language
    translation = translator.translate(text, src=source_language, dest=target_language)
    
    response = {
        'original_text': text,
        'detected_language': source_language,
        'translated_text': translation.text,
        'target_language': target_language
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
