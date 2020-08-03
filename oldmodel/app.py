import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


kivy.require('1.11.1')


import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import csv

class Jaden:
    _model = None
    _vector = None
    _vocabulary = None
    
    def __init__(self):
        self._model = pickle.load(open('_model.sav', 'rb'))
        self._vector = pickle.load(open('_vectorized.sav', 'rb'))
        with open('_tarih.csv', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            _vocabulary = list(reader)
        self._vocabulary = _vocabulary
    
    def find_answer(self, question):
        _cos_sim = linear_kernel(self._model.transform([question.lower()]), self._vector).flatten()
        _cos_sim = np.ndarray.argsort(-_cos_sim)[:5]
        _result = []
        for i in _cos_sim:
            _result.append(self._vocabulary[i+1][1])
        return _result

class JadenApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        
        self.solution = TextInput(
            multiline=False, readonly=False, halign="right", font_size=30
        )
        main_layout.add_widget(self.solution)
        
        self.button = Button(
            text="Enter the question",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.button.bind(on_press=self.on_button_press)
        main_layout.add_widget(self.button)
        
        self.text = Label(text="", font_size=16)
        main_layout.add_widget(self.text)
        
        return main_layout
    
    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        if button_text == "Enter the question":
            if current != "":
                _jaden = Jaden().find_answer(current.lower())
                self.text.text="\n".join(_jaden)
                self.button.text="Clear"
                self.solution.readonly=True
            else:
                self.text.text='Enter the question to input'
        else:
            self.button.text="Enter the question"
            self.solution.text = ""
            self.text.text = ""
            self.solution.readonly=False
            
            
            
    
JadenApp().run()