from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

import FileController
from UserIdentificationModule.Controllers.UserController import identify_user, create_user, add_record

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return app.send_static_file('index.html')


@app.route('/user_registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        return create_user(name=user_name)
    else:
        return app.send_static_file('registration_page.html')


@app.route('/add_record', methods=['POST'])
def register_user():
    file = FileController.File(request.files['audio-blob'])
    file.save()
    return add_record(file.filename, request.form.get('user_id'))


@app.route('/user_identification', methods=['GET', 'POST'])
def user_identification():
    if request.method == 'POST':
        file = FileController.File(request.files['audio-blob'])
        file.save()
        identify_res = identify_user(file.filename)
        file.delete()
        return url_for('.identification_result', name=identify_res.speaker)
    else:
        return app.send_static_file('identification.html')


@app.route('/identification_result/<name>', methods=['GET'])
def identification_result(name=None):
    return render_template('views/identification_result.html', name=name)

if __name__ == '__main__':
    # User.create_table()
    # Record.create_table()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
