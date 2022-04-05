
import datetime
from operator import concat
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Choice, Question

def create_question(question_text,days):
    """
    Create a question with the given 'question_text' and bublished the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

def create_question_with_choices(question_text,days,number_of_choices = 1):
    question = create_question(question_text=question_text,days=days)
    for i in range(number_of_choices):
        create_choice(question=question,choice_text=concat(concat("Choice ",str(i)),"."),votes= i)
    return question

def create_choice(question,choice_text,votes):
    return Choice.objects.create(question=question,choice_text=choice_text,votes=votes)
# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older then 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,seconds=59)        
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question_with_choices(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question_with_choices(question_text="Future question.",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exists, only past question are displayed."""
        past_question = create_question_with_choices(question_text="Past question.", days=-30)
        create_question_with_choices(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question],
        )
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question_with_choices(question_text="Past question 1.", days=-5)
        question2 = create_question_with_choices(question_text="Past question 2.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1,question2],
        )
    def test_past_question_with_no_choice(self):
        """
        The questions index page do not displays questions with no related choices.
        """
        question_with_no_choices = create_question(question_text="Question", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertNotContains(response,question_with_no_choices.question_text)

    def test_past_question_with_choice(self):
        """
        The questions index page shows questions with related choices.
        """
        question = create_question_with_choices(question_text="Question", days=-5)
        response = self.client.get(reverse('polls:index'))        
        self.assertContains(response,question.question_text)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question_with_choices(question_text="Future question.", days=5)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question_with_choices(question_text="Past Question.", days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)
    
    def test_past_question_with_no_choices(self):
        """
        The detail vew of a question without related choices returns a 404 not found.
        """
        question = create_question(question_text="Question.", days=-5)
        url = reverse('polls:detail',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


class QuestionResultsViewTests(TestCase):
    
    def test_future_question(self):
        """
        The questions with future pub_date are not shown in result view. 404 instead.
        """
        future_question = create_question_with_choices(question_text="Future Question",days=30)
        response = self.client.get(reverse('polls:results',args=(future_question.id,)))
        self.assertEquals(response.status_code,404)
    
    def test_past_question_with_choices(self):
        """
        The result view of a question with a pub_date in the past
        displays the question's and choice's texts.
        """
        past_question = create_question(question_text="Future Question",days=-30)
        choice1 = create_choice(past_question,"Choice 1.",1)
        choice2 = create_choice(past_question,"Choice 2.",2)
        response = self.client.get(reverse('polls:results',args=(past_question.id,)))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,past_question.question_text)
        self.assertContains(response,choice1.choice_text)
        self.assertContains(response,choice2.choice_text)

    def test_past_question_with_no_choices(self):
        """
        The results view of a question without related choices returns a 404 not found.
        """
        question = create_question(question_text="Question.", days=-5)
        url = reverse('polls:results',args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    

