# usr/bin/python3

import scipy.io.wavfile as wav

from python_speech_features import mfcc
from sklearn.cluster import KMeans

import FileController
from UserIdentificationModule.IdentificationCore import files
from UserIdentificationModule.Models.user import User


class Cluster:

    def __init__(self, n_clusters):
        self.__speakers = {}
        self.k_means = KMeans(init='k-means++', n_clusters=n_clusters)
        self.learn()

    def learn(self):
        print("Обучаем кластер...")

        mfcc_feature = []

        for rec_filename in files.list_audio():
            (rate, sig) = wav.read(rec_filename)

            for tmp in mfcc(sig, rate):
                tmp_feature = []
                for i in tmp:
                    tmp_feature.append(i)
                mfcc_feature.append(tmp_feature)

        self.k_means.fit(mfcc_feature)

        print("Обучение кластера закончено...")

    def forming_dict_with_labels(self):

        for user in User.select():
            if user.name not in self.__speakers.keys():
                self.__speakers[user.name] = []

            for record in user.records:
                (rate, sig) = wav.read(record.filename)
                self.__speakers[user.name].append(self.k_means.predict(mfcc(sig, rate)))


        print("Сформировали словарь с метками...")

    def get_learning_records(self):
        learning_records = {}

        for user in User.select():

            learning_records[user.name] = []

            for record in user.records:
                (rate, sig) = wav.read(FileController.UPLOAD_FOLDER + '/' + record.filename)
                learning_records[user.name].append(self.k_means.predict(mfcc(sig, rate)))

        return learning_records