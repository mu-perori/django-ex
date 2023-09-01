from django import forms

class TestForm(forms.Form):
    text = forms.CharField(label='文字入力')
    num = forms.IntegerField(label='数量')

class PracticeForm(forms.Form):
    choices = (
            (1, "頭痛"),
            (2, "発熱"),
            (3, "歯痛"),
            (4, "腰痛"),
            (5, "めまい"),
            (6, "皮疹"),
            (7, "捻挫")
    )
    consultation_day = forms.CharField(label='受診希望日')
    condition = forms.ChoiceField(choices, initial=0, label='症状')

