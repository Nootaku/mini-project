# SpeakBUDDY mini-service

## Guide

### Pytest

This guide assumes that you have Python and pip installed.

```bash
# cd to root of project
cd speakbuddy

# install dependencies
pip install -r requirements.txt

# set the flask environment to development
export FLASK_ENV=development

# install the 'api' module (required for pytest)
# see: https://docs.pytest.org/en/latest/explanation/goodpractices.html
pip install -e .

# you can now run the tests
pytest
```

### Docker

This guide assumes that you have Docker installed.<br />I would advise to use the volume option (`-v`) of the `docker run` command to read and write files directly from the local disk. That way, should the container be shut down, you still have your audio files.

```bash
# cd to root of project
cd speakbuddy

# build docker image
docker build -t your-name:your-tag

# run docker image with mounted volumes
docker run -p 5000:5000 -v /path/speackbuddy/cdn:/speakbuddy/cdn your-name:your-tag
```

### Query the api

```bash
# From root of the project
cd speakbuddy

# POST request
curl --request POST "http://localhost:5000/audio/user/1/phrase/1" --form audio_file=@"./test/api/samples/audio_files/input/car.mp3"

# GET request
curl --request GET http://localhost:5000/audio/user/1/phrase/1/m4a -o './test_response_file_1_1.mp3'
```

Feel free to change the user id / phrase id as you please. You can also change the input audio _file and the extension.

---

## Information and choices

- I've chosen to write the service using Python3 and the Flask framework on top of which I chose to use Flask-Restful.
- My database is a simple SQLite at the root of the project.
- Finally for the conversion of the audio files, I've decided to go with [pydub](http://pydub.com) for its simplicity.

I chose to save all files as `.ogg` as it is a very small format.
It requires `ffmpeg` to work, though.

```
apt-get install ffmpeg libavcodec-extra
```

### Data structure

You can find the database structure in the `/info/db_schema.sql` file.

### File architecture

I like to have my API and its dependencies in a separate directory: `/api`.

I chose to save all the files in the `/cdn` directory. To protect the anonymity of the users,  I prefixed a short UUID (max 8 chars) as follows: `<short_uuid>_<phrase_id>.oog`.

### Encountered problems

#### Converting a temporary file

The conversion of a temporary file seemed to be more complex than expected when using `PyDub` since a file path is required. Taking the time limit into consideration, I've decided to work around the problem by:

1. Saving the original file
2. Convert the original file
3. Save the converted file
4. Delete the original file

#### Extension aliases

This was not really a problem, but I found important to note that the `pydub` documentation states that some extensions are aliased: see line 84 of [audio_segments.py](https://github.com/jiaaro/pydub/blob/master/pydub/audio_segment.py).

I decided to replicate this behaviour.

## Improvements

One clear improvement that I could implement is to have my functions linked to API routes.<br />For example, instead of having a monolithic function that posts the entire audio file, I could create a second API route that converts audio files.

```
POST user_id, phrase_id, file
 |-- /api/convert "--request POST file"
 |-- /api/save_to_db
...
```

A second improvement is the unit-testing of the functions. I clearly did the minimum for this project. But I could also test the status responses of the API provide with correct / wrong paths and information.
