import datetime
from django.contrib.auth.decorators import login_required
from accounts.models import Coins_Operation
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from markdown import markdown
from taggit.models import Tag
from QA.forms import QuestionForm, AnswerForm, Rewarded_QuestionForm, Rewarded_AnswerForm
from QA.models import Question, Answer, Rewarded_question, Rewarded_answer


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

def is_r_question_owner(func):
    def check(request, *args, **kwargs):
        r_question_id = kwargs["question_id"]
        print(r_question_id)
        r_question = Rewarded_question.objects.get(id=r_question_id)
        if r_question.user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

def is_r_answer_owner(func):
    def check(request, *args, **kwargs):
        r_answer_id = kwargs["r_answer_id"]
        r_answer = Rewarded_answer.objects.get(id=r_answer_id)
        if r_answer.user_id != request.user.id:
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

def Questions(request):
    questions = Question.objects.all().order_by('uploaded_at')
    reward_questions = Rewarded_question.objects.all().order_by('uploaded_at')
    common_tags = Question.tags.most_common()[:4]
    context = {
        'questions': questions,
        'reward_questions': reward_questions,
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

@login_required
def reward_question(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        r_question_form = Rewarded_QuestionForm(request.POST)
        if r_question_form.is_valid():
            reward_money = r_question_form.cleaned_data['reward_money']
            balance = user.coins
            if reward_money > balance:
                error = "Sorry! Your coins are not enough for rewarding this question!"
                context = {
                    'r_question_form': r_question_form,
                    'user': user,
                    'error': error,
                }
                return render(request, 'QA/reward_questions.html', context)
            else:
                new_question = r_question_form.save(commit=False)
                new_question.title = r_question_form.cleaned_data['title']
                new_question.body = r_question_form.cleaned_data['body']
                new_question.reward_money = reward_money
                new_question.note = r_question_form.cleaned_data['note']
                new_question.user_id = user_id
                new_question.save()

                r_question_form.save_m2m()

                user.coins = balance-reward_money
                user.save()
                print(new_question.id)
                Coins_Operation.objects.create(related_profile=user, related_question=new_question, money=-reward_money, reason="Reward question")
        return redirect(reverse('QA:questions'))
    else:
        r_question_form = Rewarded_QuestionForm()
        context = {
            'r_question_form': r_question_form,
            'user': user,
        }
        return render(request, 'QA/reward_questions.html', context)

@login_required
def show_r_question(request, question_id):
    r_question = Rewarded_question.objects.get(id=question_id)
    owner_id = r_question.user.id
    r_question.body = markdown(r_question.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    r_answers = Rewarded_answer.objects.filter(question_id=question_id)
    your_answers = Rewarded_answer.objects.filter(user_id=request.user.id, question_id=question_id)
    for r_answer in r_answers:
        r_answer.content = markdown(r_answer.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    for your_answer in your_answers:
        your_answer.content = markdown(your_answer.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    r_answer_form = Rewarded_AnswerForm()
    context = {
        'r_question': r_question,
        'user_id': request.user.id,
        'owner_id': owner_id,
        'r_answers': r_answers,
        'r_answer_count': len(r_answers),
        'r_answer_form': r_answer_form,
        'your_answers': your_answers,
        'your_answer_count': len(your_answers),
    }
    return render(request, 'QA/show_r_question1.html', context)

@login_required
@is_r_question_owner
def edit_r_question(request, question_id):
    user = request.user
    edited_r_question = get_object_or_404(Rewarded_question, pk=question_id)
    if request.method == "POST":
        new_r_question_form = Rewarded_QuestionForm(request.POST, instance=edited_r_question)
        if new_r_question_form.is_valid():
            reward_money = new_r_question_form.cleaned_data['reward_money']
            balance = user.coins + Rewarded_question.objects.get(id=question_id).reward_money
            if reward_money > balance:
                error = "Sorry! Your coins are not enough for rewarding this question!"
                context = {
                    'new_r_question_form': new_r_question_form,
                    'r_question_id': question_id,
                    'user': user,
                    'error': error,
                }
                return render(request, 'QA/reward_questions.html', context)
            else:
                edited_r_question = new_r_question_form.save(commit=False)
                edited_r_question.title = new_r_question_form.cleaned_data['title']
                edited_r_question.body = new_r_question_form.cleaned_data['body']
                edited_r_question.reward_money = reward_money
                edited_r_question.note = new_r_question_form.cleaned_data['note']
                edited_r_question.uploaded_at = datetime.datetime.now()

                user.coins = balance - reward_money
                user.save()

                edited_r_question.save()
                new_r_question_form.save_m2m()

                operation = Coins_Operation.objects.get(related_question=question_id)
                operation.money = -reward_money
                operation.save()
                return redirect(reverse('QA:show_r_question', args=(question_id,)))
    else:
        new_r_question_form = Rewarded_QuestionForm(instance=edited_r_question)
        context = {
            'new_r_question_form': new_r_question_form,
            'r_question_id': question_id,
            'user': user,
        }
        return render(request, 'QA/reward_questions.html', context)

@login_required
@is_r_question_owner
def delete_r_question(request, question_id):
    user = request.user
    r_question = Rewarded_question.objects.get(id=question_id)
    r_operation = Coins_Operation.objects.get(related_question=question_id)
    r_operation.delete()
    user.coins = user.coins + r_question.reward_money
    user.save()
    r_question.delete()


    return redirect(reverse('QA:questions'))

@login_required
def post_r_answer(request, question_id):
    if request.method == "POST":
        r_answer_form = Rewarded_AnswerForm(request.POST)
        if r_answer_form.is_valid():
            new_r_answer = r_answer_form.save(commit=False)
            new_r_answer.content = r_answer_form.cleaned_data['content']
            new_r_answer.user_id = request.user.id
            new_r_answer.question_id = question_id
            new_r_answer.save()

        return redirect(reverse('QA:show_r_question', args=(question_id,)))

@login_required
@is_r_answer_owner
def edit_r_answer(request, r_answer_id):
    edited_r_answer = get_object_or_404(Rewarded_answer, pk=r_answer_id)
    if request.method == "POST":
        new_r_answer_form = Rewarded_AnswerForm(request.POST, instance=edited_r_answer)
        if new_r_answer_form.is_valid():
            edited_r_answer = new_r_answer_form.save(commit=False)
            edited_r_answer.content = new_r_answer_form.cleaned_data['content']
            edited_r_answer.save()

            return redirect(reverse('QA:show_r_question', args=(edited_r_answer.question.id,)))
    else:
        your_answers = Rewarded_answer.objects.filter(user_id=request.user.id, question_id=edited_r_answer.question.id)
        new_r_answer_form = Rewarded_AnswerForm(instance=edited_r_answer)
        context = {
            'new_r_answer_form': new_r_answer_form,
            'r_question':edited_r_answer.question,
            'r_answer_id': r_answer_id,
            'user_id': request.user.id,
            'owner': edited_r_answer.question.user.id,
            'your_answer_count': len(your_answers),
        }
        return render(request, 'QA/show_r_question1.html', context)

@login_required
@is_r_answer_owner
def delete_r_answer(request, r_answer_id):
    r_answer = Rewarded_answer.objects.get(id=r_answer_id)
    question_id = r_answer.question.id
    r_answer.delete()
    return redirect(reverse('QA:show_r_question', args=(question_id,)))

@login_required
def accept_answer(request, r_answer_id):
    r_answer = Rewarded_answer.objects.get(id=r_answer_id)
    Rewarded_answer.objects.update(status=True)
    profile = r_answer.user
    r_question = r_answer.question
    Rewarded_question.objects.update(status=True)
    profile.coins = profile.coins + r_question.reward_money
    profile.save()
    Coins_Operation.objects.create(related_profile=profile, money=+r_question.reward_money, reason='Solve question')
    return redirect(reverse('QA:show_r_question', args=(r_question.id,)))
