from UserIdentificationModule.IdentificationCore.our_mfcc import learning_with_kmeans
from UserIdentificationModule.Models.record import Record
from UserIdentificationModule.Models.user import User


def create_user(name):
    new_user = User.create(name=name)
    return new_user


def add_record(filename, user_id):
    record = Record.create(filename=filename, owner=user_id)
    return record


def identify_user(filename):
    models = learning_with_kmeans()
    coincidence_model = None
    max_coincidence = 0

    for model in models:
        curr_coincidence = model.check_accessory(filename)

        if curr_coincidence > max_coincidence:
            coincidence_model = model
            max_coincidence = curr_coincidence

    return coincidence_model
