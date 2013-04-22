from django.core.urlresolvers import reverse
from django.db import models
from orderable.models import Orderable


class Question(Orderable):
    name = models.CharField(max_length=255)
    live = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def next_question_url(self):
        return reverse('question', args=(self.pk+1,))


class Answer(Orderable):
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
