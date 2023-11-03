import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from pytube import YouTube
import zipfile

app = Flask(__name__)
CORS(app)

# Rota para servir o arquivo zip
@app.route('/get_zip', methods=['GET'])
def get_zip():
    uploads = os.path.join(app.root_path, 'downloads')
    return send_from_directory(directory=uploads, filename='download.zip', as_attachment=True)

@app.route('/download', methods=['POST'])
def download_from_links():
    data = request.json
    links = data.get('links')
    type = data.get('type')
    results = []

    if type not in ['M', 'V']:
        return jsonify({'error': 'Invalid type'})

    zip_filename = os.path.join(app.root_path, 'downloads', 'download.zip')
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for link in links:
            yt = YouTube(link)

            if type == 'M':
                tipo = "music"
                local = './musicas'
                stream = yt.streams.filter(only_audio=True).first()
            elif type == 'V':
                tipo = "video"
                local = './video'
                stream = yt.streams.get_highest_resolution()

            if stream:
                print(f"Baixando {tipo}: {yt.title}")
                stream.download(output_path=local)
                print("Download concluído!")
                file_path = os.path.join(local, stream.default_filename)
                zip_file.write(file_path, arcname=os.path.basename(file_path))
                results.append({
                    'status': 'success',
                    'message': f'{tipo} downloaded for link: {link}'
                })
            else:
                results.append({'error': f'Stream not found for link: {link}'})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
