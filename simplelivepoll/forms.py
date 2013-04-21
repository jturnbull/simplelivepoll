from django import forms


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.question_obj = question
        self.fields['question'] = forms.IntegerField(widget=forms.HiddenInput, initial=question.id)
        self.fields['answer'] = forms.ModelChoiceField(queryset=question.answer_set)

    def increment_answer(self):
        answer = self.cleaned_data['answer']
        print "answer has %d votes" % answer.votes
        answer.votes = answer.votes + 1
        answer.save()
        return True
