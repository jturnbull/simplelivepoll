from __future__ import division
from django.core.urlresolvers import reverse
from django.db import models
from orderable.models import Orderable


class Question(Orderable):
    name = models.CharField(max_length=255)
    live = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def next_question_url(self):
        if Question.objects.filter(pk=self.pk+1).exists():
            return reverse('question', args=(self.pk+1,))
        else:
            return ''


class Answer(Orderable):
    name = models.CharField(max_length=255)
    question = models.ForeignKey(Question)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def percentage(self):
        total = self.question.answer_set.all().aggregate(sum=models.Sum('votes'))['sum']
        return "%.0f%%" % ((self.votes / total) * 100)

