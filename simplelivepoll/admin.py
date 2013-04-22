from django.contrib import admin
from orderable.admin import OrderableAdmin, OrderableTabularInline

from .models import Answer, Question


class AnswerInline(OrderableTabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(OrderableAdmin):
    inlines = [AnswerInline]
    list_display = ('__unicode__', 'live', 'sort_order_display')
    list_editable = ('live',)

    class Media:
        js = (
            'scripts/libs/jquery-1.9.1.min.js',
            'scripts/libs/jquery-ui.min.js',
        )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

