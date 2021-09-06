import os
import uuid
from pydub import AudioSegment as Audio
from pydub.utils import which
from werkzeug.utils import secure_filename


def generateRandomFileName(phrase_id):
    random_string = str(uuid.uuid4())[:8]
    random_file_name = random_string + "_{}.ogg".format(phrase_id)
    return random_file_name


def convertAsOgg(audio_file, output_path):
    """Convert an audio_file to the 'OGG' format and saves the ogg file.
    """
    input_format = audio_file.rsplit('.', 1)[1].lower()
    Audio.converter = which("ffmpeg")

    file = Audio.from_file(audio_file, input_format)

    file.export(output_path, format="ogg")


def getAudio(audio_file):
    """Return audio from a file.
    """
    input_format = audio_file.rsplit('.', 1)[1].lower()
    Audio.converter = which("ffmpeg")

    file = Audio.from_file(audio_file, input_format)

    return file


def saveFile(audio_file, config, phrase_id):
    # Save file
    # ensure filename is not harmful
    filename = secure_filename(audio_file.filename)
    tmp_file_path = os.path.join(config["UPLOAD_TMP_FOLDER"], filename)
    audio_file.save(tmp_file_path)

    # Get random name
    new_filename = generateRandomFileName(phrase_id)
    new_file_path = os.path.join(config["UPLOAD_FOLDER"], new_filename)

    # Convert File
    convertAsOgg(tmp_file_path, new_file_path)

    # Delete temporary file
    os.remove(tmp_file_path)

    return new_file_path
