import sqlite3


# DB initialization
# For the sake of documentation, I added the file 'db_schema.sql'
# Normally I would use the flask configuration instead of a static string
def get_db():
    """Connect to the DB
    """
    conn = None
    try:
        conn = sqlite3.connect('database.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn


# DB Queries
def postAudioFile(user_id, phrase_id, audio_file_path):
    """Insert line into db
    """
    db = get_db()
    cursor = db.cursor()

    query = """INSERT INTO audio_files (phrase_id, user_id, file_path)
    VALUES (?, ?, ?)"""

    cursor.execute(query, (phrase_id, user_id, audio_file_path))
    db.commit()


def getAudioUri(user_id, phrase_id):
    """Return the URI of the audio file.
    Will always get the latest uploaded file.
    """
    db = get_db()
    cursor = db.cursor()

    query = """SELECT file_path, MAX(created) FROM audio_files
    WHERE phrase_id = {}
    AND user_id = {}""".format(phrase_id, user_id)

    cursor.execute(query)
    result = cursor.fetchone()[0]  # we query a date but don't need it

    return result
