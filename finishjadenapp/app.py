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
    _unique_stemmed_words = None
    
    def __init__(self):
        self._model = pickle.load(open('_model.sav', 'rb'))
        self._vector = pickle.load(open('_vectorized.sav', 'rb'))
        with open('_tarih.csv', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            _vocabulary = list(reader)
        self._vocabulary = _vocabulary
        with open('_unique_stemmed_words.csv', newline='', encoding='utf8') as f:
            reader = csv.reader(f)
            _unique_stemmed_words = list(reader)
        self._unique_stemmed_words = _unique_stemmed_words
    
    def find_answer(self, question):
        _cos_sim = linear_kernel(self._model.transform([self.stemming(self._unique_stemmed_words, question.lower())]), self._vector).flatten()
        _cos_sim = np.ndarray.argsort(-_cos_sim)[:5]
        _result = []
        for i in _cos_sim:
            _result.append(self._vocabulary[i+1][1])
        return _result

    def stemming(self, doc1, doc2):
        alldocin = doc1
        docin = doc2.split(' ')
        result = []
        for i in range(len(alldocin)):
            for j in range(len(docin)):
                s = self.comparison(alldocin[i][0], docin[j])
                if(len(s) > 3):
                    docin[j] = s
        
        return " ".join(str(x) for x in docin)
    
    def comparison(self, word1, word2):
        length = len(word2) if len(word1) > len(word2) else len(word1)
        result = ''
        for i in range(length):
            if(word1[i] == word2[i]):
                result = result + word1[i]
            else:
                break
        return result

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
            _jaden = Jaden().find_answer(current.lower())
            self.text.text="\n".join(_jaden)
            self.button.text="Clear"
        else:
            self.button.text="Enter the question"
            self.solution.text = ""
            self.text.text = ""
            
            
            
    
JadenApp().run()