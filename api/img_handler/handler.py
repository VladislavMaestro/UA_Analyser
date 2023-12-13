import os
import numpy as np
from keras.models import load_model
import api.img_api.img_characteristics as ic


def img_data_viewer(final_data):
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_model")
    model = load_model(model_path)
    answer = model.predict(np.expand_dims(final_data[0], axis=0))
    answer = answer.tolist()
    index_of_max_answer = answer[0].index(max(answer[0])) + 1
    if index_of_max_answer == 1:
        return "нормальная"
    if index_of_max_answer == 2:
        return "низкая"
    if index_of_max_answer == 3:
        return "высокая"
    if index_of_max_answer == 4:
        return "очень высокая"
