from django.views.generic import FormView
from .forms import QuestionForm
from .models import Question

class QuestionView(FormView):
    form_class = QuestionForm
    template_name = 'question.html'

    def get_form_kwargs(self):
        kwargs = super(QuestionView, self).get_form_kwargs()
        question = Question.objects.filter(live=True)[0]
        kwargs.update({
            'question': question,
        })
        return kwargs

    def form_valid(self, form):
        form.increment_answer()
        return super(QuestionView, self).form_valid(form)
