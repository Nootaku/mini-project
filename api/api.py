import os
import tempfile
from flask import Flask, request, send_file
from flask_restful import Resource, Api

# Internal imports
import db
import audio

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

"""Normally I would place the following variables in a .env file and call them
up using a library like 'dotenv'.
"""
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_FOLDER=os.path.join(os.getcwd(), "cdn"),
    UPLOAD_TMP_FOLDER=os.path.join(os.getcwd(), "cdn", "tmp"),
    ALLOWED_EXTENSIONS=set(['mp3', 'm4a', 'mp4', 'wav'])
)


class GetAudio(Resource):
    # will be used with curl as:
    # curl --request GET http://localhost:5000/audio/user/1/phrase/1/m4a -o './test_response_file_1_1.m4a'
    def get(self, user_id, phrase_id, audio_format):
        if audio_format in app.config['ALLOWED_EXTENSIONS']:
            # get resource URI
            uri = db.getAudioUri(user_id, phrase_id)
            format_aliases = {
                "m4a": "mp4",
                "wave": "wav"
            }
            format = format_aliases[audio_format] if \
                audio_format in format_aliases else audio_format

            audio_file = audio.getAudio(uri)

            with tempfile.NamedTemporaryFile("w+") as f:
                audio_file.export(f.name, format=format)
                return send_file(f.name)

        return {'message': 'Error: extention of file is not allowed'}, 400


class PostAudio(Resource):
    # will be used with curl as:
    # curl --request POST "http://localhost:5000/audio/user/1/phrase/1" --form 'audio_file=@"./test_audio/car.mp3"'
    def post(self, user_id, phrase_id):
        # Check if there is a file in the request
        if 'audio_file' not in request.files:
            return {'message': 'Error: no file was found in query'}, 400

        audio_file = request.files['audio_file']

        if '.' in audio_file.filename and audio_file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
            upload_path = audio.saveFile(audio_file, app.config, phrase_id)

            # save to db
            db.postAudioFile(user_id, phrase_id, upload_path)
            return {'message': 'Success: file uploaded'}, 201

        return {'message': 'Error: extention of file is not allowed'}, 400


api.add_resource(
    GetAudio,
    '/audio/user/<int:user_id>/phrase/<int:phrase_id>/<string:audio_format>'
)
api.add_resource(PostAudio, '/audio/user/<int:user_id>/phrase/<int:phrase_id>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
