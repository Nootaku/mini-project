import os
import pytest
import sqlite3
import api.db as db


# First create a test-db
def getTestDb(delete=True):
    conn = None
    test_db_path = os.path.join(os.getcwd(),
                                "tests",
                                "api",
                                "samples",
                                "test_db.sqlite")
    try:
        conn = sqlite3.connect(test_db_path)
    except sqlite3.error as e:
        print(e)

    if delete:  # start with fresh db for every test
        conn.cursor().execute("DROP TABLE IF EXISTS users;")
        conn.cursor().execute("DROP TABLE IF EXISTS audio_files;")

        conn.cursor().execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            );""")

        conn.cursor().execute("""
            CREATE TABLE audio_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                file_path TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );""")

    return conn


@pytest.mark.parametrize("audio_file, user_id, phrase_id", [
    ("car.mp3", 1, 1),
    ("car.mp3", 2, 1),
    ("marbles.mp3", 1, 2),
    ("marbles.mp3", 2, 2)
])
def test_postAudioFile(monkeypatch, audio_file, user_id, phrase_id):
    def mock_db():
        return getTestDb()

    monkeypatch.setattr(db, "get_db", mock_db)

    audio_file = os.path.join(os.getcwd(),
                              "tests",
                              "api",
                              "samples",
                              "audio_files",
                              "input",
                              audio_file)
    db.postAudioFile(user_id, phrase_id, audio_file)

    query = """SELECT user_id, phrase_id, file_path FROM audio_files
    WHERE phrase_id = {}
    AND user_id = {}""".format(phrase_id, user_id)

    conn = getTestDb(False)
    result = conn.cursor().execute(query).fetchone()

    assert user_id == result[0]
    assert phrase_id == result[1]
    assert audio_file == result[2]


@pytest.mark.parametrize("user_id, phrase_id, expected", [
    (1, 1, "foo.mp3"),
    (1, 2, "bar.mp3"),
    (1, 3, "blah.mp3"),
    (2, 1, "oof.mp3"),
    (2, 2, "rab.mp3"),
    (2, 3, "halb.mp3")
])
def test_getAudioUri(monkeypatch, user_id, phrase_id, expected):
    def mock_db_clean():
        return getTestDb()

    def mock_db():
        return getTestDb(False)

    monkeypatch.setattr(db, "get_db", mock_db_clean)

    audio_file = os.path.join(os.getcwd(),
                              "tests",
                              "api",
                              "samples",
                              "audio_files",
                              "input",
                              expected)
    # we have tested PostAudioFile already, so we can use it here:
    db.postAudioFile(user_id, phrase_id, audio_file)

    monkeypatch.setattr(db, "get_db", mock_db)
    result = db.getAudioUri(user_id, phrase_id)

    assert result == audio_file
