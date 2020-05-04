import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from markdown import markdown
from taggit.models import Tag
from QA.forms import QuestionForm, AnswerForm
from QA.models import Question, Answer

def is_user_owner(func):
    def check(request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

def is_question_owner(func):
    def check(request, *args, **kwargs):
        question_id = kwargs["question_id"]
        question = Question.objects.get(id=question_id)
        if question.user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

@login_required
@is_user_owner
def post_question(request, user_id):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(commit=False)
            new_question.title = question_form.cleaned_data['title']
            new_question.body = question_form.cleaned_data['body']
            new_question.user_id = user_id
            new_question.save()

            question_form.save_m2m()
        return redirect(reverse('QA:questions'))

    else:
        question_form = QuestionForm()
        user = User.objects.get(id=user_id)
        context = {
            'question_form': question_form,
            'user': user
        }
        return render(request, 'QA/post_questions.html', context)

@login_required
def Questions(request):
    questions = Question.objects.all().order_by('uploaded_at')
    common_tags = Question.tags.most_common()[:4]
    context = {
        'questions': questions,
        'user_id': request.user.id,
        'common_tags': common_tags,
    }
    return render(request, 'QA/questions.html', context)

@login_required
def show_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.increase_views()
    question.body = markdown(question.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    question_type = ContentType.objects.get(app_label='QA', model='question')
    answer_type = ContentType.objects.get(app_label='QA', model='answer')

    answers = Answer.objects.filter(question_id=question_id)
    for answer in answers:
        answer.content = markdown(answer.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    answer_count = len(answers)
    answer_form = AnswerForm()
    context = {
        'question': question,
        'user_id': request.user.id,
        'answer_form': answer_form,
        'answers': answers,
        'answer_count': answer_count,
        'question_type_id': question_type.id,
        'answer_type_id': answer_type.id,
    }
    return render(request, 'QA/show_question.html', context)

@login_required
def post_answer(request, question_id):
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            new_answer = answer_form.save(commit=False)
            new_answer.content = answer_form.cleaned_data['content']
            new_answer.user_id = request.user.id
            new_answer.question_id = question_id
            new_answer.save()

        return redirect(reverse('QA:show_question', args=(question_id,)))

@login_required
@is_question_owner
def edit_question(request, question_id):
    edited_question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        new_question_form = QuestionForm(request.POST, instance=edited_question)
        if new_question_form.is_valid():
            edited_question = new_question_form.save(commit=False)
            edited_question.title = new_question_form.cleaned_data['title']
            edited_question.body = new_question_form.cleaned_data['body']
            edited_question.uploaded_at = datetime.datetime.now()
            edited_question.save()

            new_question_form.save_m2m()
            return redirect(reverse('QA:show_question', args=(question_id,)))
    else:
        new_question_form = QuestionForm(instance=edited_question)
        context = {
            'new_question_form': new_question_form,
            'question_id': question_id,
        }
        return render(request, 'QA/post_questions.html', context)

@login_required
@is_question_owner
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect(reverse('QA:questions'))

@login_required
def questions_tagged(request, tag_slug=None):
    questions = Question.objects.all()
    # tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        question_list = questions.filter(tags__in=[tag])

        context = {
            'tag': tag,
            'question_list': question_list,
        }
        return render(request, 'QA/tag_list.html', context)
