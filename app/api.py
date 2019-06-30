#!/usr/bin/env python

from flask import Flask, request, url_for, render_template, jsonify, json

from google.cloud import speech
from google.cloud.speech import types
from google.cloud.speech import enums

app = Flask(__name__)

encoding_types = {
    'LINEAR16': enums.RecognitionConfig.AudioEncoding.LINEAR16 ,
    'AMR': enums.RecognitionConfig.AudioEncoding.AMR ,
    'AMR_WB': enums.RecognitionConfig.AudioEncoding.AMR_WB ,
    'ENCODING_UNSPECIFIED': enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED ,
    'FLAC': enums.RecognitionConfig.AudioEncoding.FLAC ,
    'MULAW': enums.RecognitionConfig.AudioEncoding.MULAW ,
    'OGG_OPUS': enums.RecognitionConfig.AudioEncoding.OGG_OPUS ,
    'SPEEX_WITH_HEADER_BYTE': enums.RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE
}

@app.route('/')
def index():
    return render_template("index.html", action=url_for("speech_to_text_handler"))


@app.route('/api/speech2text', methods=['POST'])
def speech_to_text_handler():
    file = request.files['file']
    if file is None:
        raise ValueError("Parameter 'file' is missing.")
    content = file.read()

    encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED

    if 'parameters' in request.form:
        json_parameters = request.form['parameters']
        if(json_parameters is not None):
            parameters = json.loads(json_parameters)
            encoding_repr = parameters['encoding']
            if encoding_repr and encoding_repr in encoding_types:
                encoding = encoding_types[encoding_repr]

    transcript = convert_audio(content, encoding)

    response = {
        'success': True,
        'transcript': transcript
    }
    return jsonify(response), 200


def convert_audio(content, encoding):
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=encoding,
        language_code='en-US')
    googleResponse = client.recognize(config, audio)
    transcript = ""
    for result in googleResponse.results:
        transcript = transcript + result.alternatives[0].transcript
    return transcript


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred.'
        }
    }
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
