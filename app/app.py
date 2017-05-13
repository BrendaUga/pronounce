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
    form = AddWordPronouncingForm()
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
        return render_template('index.html', form=form)


@app.route('/show', methods=['GET', 'POST'])
def show():
    form = SearchWordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            keyword = form.keyword.data
            output = []
            words = mongo.db.words.find({'word': keyword})
            for word in words:
                output.append({'word': word['word'], 'filename': word['filename']})
            return render_template('show.html', form=form, words=output)
        else:
            print("form not validated")
            return render_template('show.html', form=form)
    else:
        print("method is get")
        return render_template('show.html', form=form)


@app.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    return mongo.send_file(filename)


@app.route('/words')
def words():
    cursor = mongo.db.words.find()
    word_list = []
    for object in cursor:
        word_list.append({'word': object['word'], 'filename': object['filename']})
    return json.jsonify(word_list)


if __name__ == "__main__":
    app.run(debug=True)
