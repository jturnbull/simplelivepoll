from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import TemplateView, FormView, RedirectView, DetailView
from django.views.generic.detail import SingleObjectMixin

from .forms import QuestionForm
from .models import Question


class HomeView(TemplateView):
    template_name = 'home.html'


class NextQuestion(RedirectView):
    def get_redirect_url(self, **kwargs):
        try:
            live_question = Question.objects.filter(live=True, closed=False)[0]
            return reverse('question', args=[live_question.pk])
        except IndexError:
            raise Http404


class QuestionView(FormView, SingleObjectMixin):
    form_class = QuestionForm
    queryset = Question.objects.filter(live=True)
    template_name = 'question.html'

    def form_valid(self, form):
        form.increment_answer()
        return super(QuestionView, self).form_valid(form)

    def get_form_kwargs(self):
        self.object = self.get_object()
        kwargs = super(QuestionView, self).get_form_kwargs()
        kwargs['question'] = self.object
        return kwargs

    def get_success_url(self):
        return reverse('results', args=(self.object.pk,))


class ResultView(DetailView):
    queryset = Question.objects.filter(live=True, closed=True)
    template_name = 'results.html'
