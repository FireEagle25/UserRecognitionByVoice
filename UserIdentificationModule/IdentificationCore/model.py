# usr/bin/python3

import numpy as np
import scipy.io.wavfile as wav

from hmmlearn import hmm
from python_speech_features import mfcc

import FileController


class Model:

    def __init__(self, n_clusters, speaker, records, cluster):

        self.__cluster = cluster
        self.__n_clusters = n_clusters
        self.speaker = speaker
        self.__model = None

        if len(records) > 0:
            self.max_label_array_len = max([len(x) for x in records])
            self.__records = [self.equalize_record(record) for record in records]

            self.__build_model()
            self.fit()

        print("Модель успешно создана и обучена")

    def fit(self):
        self.__build_model()
        self.__model.fit(self.__records)

    def __build_model(self):
        n_components = self.get_n_components()

        self.__model = hmm.MultinomialHMM(n_components=self.__n_clusters,
                                          startprob_prior=Model.make_startprob(n_components),
                                          transmat_prior=Model.make_transmat(n_components),
                                          params=self.__records)

        self.__model.emissionprob = Model.make_emissionprob(n_components, self.__n_clusters)

    def check_accessory(self, filename):

        if self.__model:
            print(filename)
            (rate, sig) = wav.read(FileController.UPLOAD_FOLDER + '/' + filename)
            equalized_record = self.equalize_record(self.__cluster.k_means.predict(mfcc(sig, rate)))

            res = [[coef] for coef in equalized_record]
            predicted = self.__model.predict_proba(res)
            print(predicted)

            print('res: ', sum([max(arr) for arr in predicted])/self.max_label_array_len)

            return sum([max(arr) for arr in predicted])/self.max_label_array_len

    def equalize_record(self, record):
        diff_between_curr_and_max = self.max_label_array_len - len(record)

        if diff_between_curr_and_max >= 0:
            record = np.array(list(record) + [0 for _ in range(diff_between_curr_and_max)])
        else:
            record = record[:abs(diff_between_curr_and_max)]

        return record

    def get_n_components(self):
        return self.max_label_array_len

    @staticmethod
    def make_startprob(n):
        a = [1.]
        tmp = [0] * (n - 1)
        a.extend(tmp)
        return a

    @staticmethod
    def make_emissionprob(m, n):
        matr = np.zeros((m, n), float)
        for i in range(0, matr.shape[0]):
            for j in range(0, matr[i].shape[0]):
                matr[i][j] = 1. / matr[i].shape[0]

        return matr

    @staticmethod
    def make_transmat(n):
        matr = np.zeros((n, n), float)
        for i in range(0, matr.shape[0]):
            sum_exp = 0.
            for k in range(1, n - i + 1):
                sum_exp += np.math.e ** (-k)
            for j in range(i, matr[i].shape[0]):
                matr[i][j] = np.math.e ** (-j + i - 1) / sum_exp
        return matr
