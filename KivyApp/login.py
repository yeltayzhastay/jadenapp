import pandas as pd
import numpy as np

import pickle
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

import csv

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class Jaden:
    _model = None
    _vector = None
    _vocabulary = None
    
    def __init__(self):
        self._model = pickle.load(open('_model.sav', 'rb'))
        self._vector = pickle.load(open('_vectorized.sav', 'rb'))
        with open('dataset/tarih.csv', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            _vocabulary = list(reader)
        self._vocabulary = _vocabulary
    
    def find_answer(self, question):
        _cos_sim = linear_kernel(_model.transform([question]), _vector).flatten()
        _cos_sim = np.ndarray.argsort(-_cos_sim)[:5]
        _result = []
        for i in _cos_sim:
            _result.append(self._vocabulary[i+1][1])
        return _result
    

class LoginScreen(GridLayout):
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MyApp(App):

    def build(self):
        return LoginScreen()



MyApp().run()