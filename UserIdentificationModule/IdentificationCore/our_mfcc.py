
from UserIdentificationModule.IdentificationCore.cluster import Cluster
from UserIdentificationModule.IdentificationCore.model import Model


def learning_with_kmeans():

    users_count = 10
    cluster = Cluster(users_count)
    learning_records = cluster.get_learning_records()

    return [Model(users_count, speaker, learning_records[speaker], cluster) for speaker in learning_records]