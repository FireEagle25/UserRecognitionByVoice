import os
from datetime import datetime

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')


class File:
    def __init__(self, file):
        self.file = file
        self.filename = secure_filename(file.filename)

    def save(self):
        if self.file:
            self.file.save(os.path.join(UPLOAD_FOLDER, self.filename))

            wav_name = str(datetime.now().timestamp()) + '.wav'
            webm_to_wav_command = "avconv  -i " + UPLOAD_FOLDER + '/' + self.filename \
                                  + " -ab 160k -ac 1 -ar 16000 -vn " + UPLOAD_FOLDER + '/' + wav_name

            self.filename = wav_name
            os.system(webm_to_wav_command)
            return True
        else:
            return False

    def delete(self):
        os.remove(os.path.join(UPLOAD_FOLDER, self.filename))
        return True
