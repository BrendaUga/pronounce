from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from forms import AddWordPronouncingForm, SearchWordForm

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddWordPronouncingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            word = form.word.data
            file = form.audio_file.data
            filename = file.filename
            print(word)
            print(filename)
            mongo.db.words.insert_one({'word': word, 'filename': filename})
            mongo.save_file(filename, file)
            return render_template('index.html', form=form)
        else:
            print("form not validated")
            return render_template('index.html', form=form)
    else:
        print("method is get")
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


@app.route('/get_file/<path:filename>', methods=['GET'])
def get_file(filename):
    return mongo.send_file(filename)


if __name__ == "__main__":
    app.run(debug=True)
