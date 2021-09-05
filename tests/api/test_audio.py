import os
import pytest
import pydub
import api.audio as audio


@pytest.fixture
def mock_config():
    return {
        "SECRET_KEY": 'dev',
        "UPLOAD_FOLDER": os.path.join(os.getcwd(), "tests",
                                      "api",
                                      "samples",
                                      "audio_files",
                                      "output"),
        "UPLOAD_TMP_FOLDER": os.path.join(os.getcwd(), "tests",
                                          "api",
                                          "samples",
                                          "audio_files",
                                          "output"),
        "ALLOWED_EXTENSIONS": set(['mp3', 'm4a', 'mp4', 'wav']),
        "TEST_FOLDER": os.path.join(os.getcwd(), "tests",
                                    "api",
                                    "samples",
                                    "audio_files",
                                    "input"),
    }


def test_generateRandomFileName():
    random_filename_list = [
        audio.generateRandomFileName(1) for i in range(10000)]
    for i in random_filename_list:
        assert random_filename_list.count(i) == 1


def test_convertAsOgg(mock_config):
    # Using PyDub to test extensions
    input_file = os.path.join(mock_config["TEST_FOLDER"], "car.mp3")
    output_file = os.path.join(mock_config["UPLOAD_FOLDER"], "foo.ogg")

    audio.convertAsOgg(input_file, output_file)

    try:
        pydub.AudioSegment.from_ogg(output_file)
        assert True
    except pydub.exceptions.CouldntDecodeError:
        pytest.fail(msg="Conversion failed")

    os.remove(output_file)
