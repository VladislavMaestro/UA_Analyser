import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
from keras.models import load_model
import api.img_api.img_characteristics as ic


def img_data_viewer(final_data):
    model = load_model("d:\\py\\saved_model")
    print(final_data[0])
    answer = model.predict(np.expand_dims(final_data[0], axis=0))
    answer = answer.tolist()
    print(answer)
    index_of_max_answer = answer[0].index(max(answer[0])) + 1
    if index_of_max_answer == 1:
        return "normal"
    if index_of_max_answer == 2:
        return "low"
    if index_of_max_answer == 3:
        return "high"
    if index_of_max_answer == 4:
        return "very high"
