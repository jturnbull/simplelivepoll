import json

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic import FormView, RedirectView, DetailView
from django.views.generic.detail import SingleObjectMixin

from .forms import QuestionForm
from .models import Question


class HomeView(RedirectView):
    def get_redirect_url(self, **kwargs):
        try:
            live_question = Question.objects.filter(live=True).order_by('-sort_order')[0]
            return reverse('question', args=(live_question.pk,))
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
    model = Question
    template_name = 'results.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():

            response_data = {
                'question': u'%s' % self.object,
                'answers': list(),
            }

            for answer in self.object.answer_set.all():
                response_data['answers'].append(dict(name=u'%s' % answer, data=[int(answer.percentage())]))

            return HttpResponse(json.dumps(response_data), mimetype='application/json')

        else:
            response_kwargs.setdefault('content_type', self.content_type)
            return self.response_class(
                request = self.request,
                template = self.get_template_names(),
                context = context,
                **response_kwargs
            )

class ProjectorView(ResultView):
    template_name = 'projector-results.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.live = True
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
