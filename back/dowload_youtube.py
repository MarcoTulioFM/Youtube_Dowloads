from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_from_links():
    data = request.json
    links = data.get('links')
    type = data.get('type')
    results = []

    if type not in ['M', 'V']:
        return jsonify({'error': 'Invalid type'})

    for link in links:
        yt = YouTube(link)

        if type == 'M':
            tipo = "music"
            local = './music'
            stream = yt.streams.filter(only_audio=True).first()
        elif type == 'V':
            tipo = "video"
            local = './video'
            stream = yt.streams.get_highest_resolution()

        if stream:
            print(f"Baixando {tipo}: {yt.title}")
            stream.download(output_path=local)
            print("Download concluído!")
            results.append({'status': 'success', 'message': f'{tipo} downloaded for link: {link}'})
        else:
            results.append({'error': f'Stream not found for link: {link}'})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
