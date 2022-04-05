from dataclasses import fields
from django.contrib import admin

from polls.models import Question, Choice

# default admin form
#admin.site.register(Question)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields =['choice_text']

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date','question_text']
    fieldsets = [
        (None, {'fields':['question_text']}),
        ('Date information',{'fields':['pub_date']}),
    ]
    inlines =[ChoiceInline]
    list_display = ('question_text','pub_date','was_published_recently')
    list_filter =['pub_date']
    search_fields = ['question_text']
    list_per_page = 2
admin.site.register(Question,QuestionAdmin)
