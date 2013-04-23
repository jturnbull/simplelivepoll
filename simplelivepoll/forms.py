import logging

from django import forms

logger = logging.getLogger('simplelivepoll.default')


class QuestionForm(forms.Form):

    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.question_obj = question
        self.fields['question'] = forms.IntegerField(widget=forms.HiddenInput, initial=question.pk)
        self.fields['answer'] = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=question.answer_set)
        self.fields['answer'].empty_label = None

    def increment_answer(self):
        answer = self.cleaned_data['answer']
        logger.debug('answer has {} votes'.format(answer.votes))
        answer.votes = answer.votes + 1
        answer.save()
        return True
