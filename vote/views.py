import datetime
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse

from QA.models import Answer
from vote.models import Votes

def QuestionVotes(request, question_id, vote_type):
    user = request.user
    question_type = ContentType.objects.get(app_label="QA", model="question")
    date = datetime.datetime.now()

    if vote_type == "up":
        vote_type = True
    else:
        vote_type = False

    if user.is_authenticated:
        hasbeen_voted = Votes.objects.filter(
            user=user,
            content_type=question_type,
            object_id=question_id,
        )
        if hasbeen_voted:
            if vote_type:
                hasbeen_voted.delete()
            else:
                obj = hasbeen_voted.get()
                obj.vote_type = False
                obj.save()

        else:
            Votes.objects.create(
                user=user,
                content_type=question_type,
                object_id=question_id,
                date=date,
                vote_type=vote_type,
            )
        return HttpResponseRedirect(reverse('QA:show_question', args=(question_id,)))

    else:
        return HttpResponseRedirect('accounts:login')

def AnswerVotes(request, answer_id, vote_type):
    user = request.user
    answer_type = ContentType.objects.get(app_label="QA", model="answer")
    date = datetime.datetime.now()
    question_id = Answer.objects.get(id=answer_id).question_id

    if vote_type == "up":
        vote_type = True
    else:
        vote_type = False

    if user.is_authenticated:
        hasbeen_voted = Votes.objects.filter(
            user=user,
            content_type=answer_type,
            object_id=answer_id,
        )
        if hasbeen_voted:
            if vote_type:
                hasbeen_voted.delete()
            else:
                obj = hasbeen_voted.get()
                obj.vote_type = False
                obj.save()

        else:
            Votes.objects.create(
                user=user,
                content_type=answer_type,
                object_id=answer_id,
                date=date,
                vote_type=vote_type,
            )
        return HttpResponseRedirect(reverse('QA:show_question', args=(question_id,)))

    else:
        return HttpResponseRedirect('accounts:login')
