from flask import Flask, render_template, request, jsonify, json
from flask_pymongo import PyMongo
from forms import AddWordPronouncingForm, SearchWordForm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['mp3']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'word' not in request.form or len(request.form['word']) == 0:
            return json.jsonify({"success": False, "message": "Word is needed"})

        if 'audio_file' not in request.files:
            return json.jsonify({"success": False, "message": "Audio file must be uploaded"})

        file = request.files['audio_file']
        if file.filename == '':
            return json.jsonify({"success": False, "message": "Audio file must be uploaded"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            word = request.form['word']

            if mongo.db.words.find_one({'word': word}):
                mongo.db.words.update_one({'word': word}, {'$set': {
                    'filename': filename
                }})
            else:
                mongo.db.words.insert_one({'word': word, 'filename': filename})

            mongo.save_file(filename, file)

            return json.jsonify({"success": True, "message": "Word saved!"})

        return json.jsonify({"success": False, "message": "File must be mp3"})

    else:
        return render_template('index.html')


@app.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    return mongo.send_file(filename)


@app.route('/words')
def words():
    cursor = mongo.db.words.find().sort('word', 1)
    word_list = []
    for object in cursor:
        word_list.append({'word': object['word'], 'filename': object['filename']})
    return json.jsonify(word_list)


if __name__ == "__main__":
    app.run(debug=True)
