from django.core import serializers
from django.shortcuts import render, get_object_or_404, get_list_or_404
import json
import random
import uuid
from django.contrib.auth.hashers import make_password, check_password

from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Avg, Sum, Min, Max

from Api.decorators import check_token
from Api.forms import AnswerForm
from Formula0.utils import get_response, get_problem_cost
from Formula0.models import *


@csrf_exempt
def login(request):
    if request.method == "POST":
        national_id = request.POST.get('national_id')
        team = {}
        if Team.objects.filter(student1__national_id=national_id):
            team = Team.objects.filter(student1__national_id=national_id).first()
        if Team.objects.filter(student2__national_id=national_id):
            team = Team.objects.filter(student2__national_id=national_id).first()
        if Team.objects.filter(student3__national_id=national_id):
            team = Team.objects.filter(student3__national_id=national_id).first()
        if not team:
            return get_response('کد ملی شما در هیچ تیمی عضو نیست!', {}, 404)
        return get_response('خوش آمدید!', '{{"team_id": "{}"}}'.format(team.id))

    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_team_data(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        print(team_id)
        team = get_object_or_404(Team, id=team_id)
        return get_response('اطلاعات تیم با موفقیت دریافت شد!',
                            '{{"name": "{}", "score": "{}", "grade": "{}"}}'.format(team.name, team.score, team.grade))
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_problems(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')

        problem_teams = get_list_or_404(ProblemTeam, team__id=team_id)
        result = []
        for problem_team in problem_teams:
            result.append({
                'id': problem_team.id,
                'status': problem_team.status,
                'name': problem_team.problem.name,
                'score': problem_team.score,
                'subject': problem_team.problem.subject,
            })
        return get_response("سوالات با موفقیت دریافت شد!", format(json.dumps(result)))
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_auction_problems(request):
    if request.method == "POST":

        problem_teams = get_list_or_404(ProblemTeam, status=4)
        result = []
        for problem_team in problem_teams:
            result.append({
                'id': problem_team.id,
                'status': problem_team.status,
                'name': problem_team.problem.name,
                'score': problem_team.score,
                'auction_cost': problem_team.auction_cost,
                'subject': problem_team.problem.subject,
            })
        return get_response("سوالات مزایده با موفقیت دریافت شد!", format(json.dumps(result)))
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def request_problem(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        subject = int(request.POST.get('subject'))

        if len(ProblemTeam.objects.filter(team__id=team_id, status=1)) >= 3:
            return get_response("نمی‌توانید هم‌زمان بیش از ۳ سوال داشته باشید!", {}, 400)

        if len(ProblemTeam.objects.filter(team__id=team_id, problem__subject=subject)) >= 4:
            return get_response("شما ۴ سوال خود را از این مبحث گرفته‌اید!", {}, 400)

        problems = Problem.objects.filter(subject=subject)
        probable_problems = []
        for problem in problems:
            if len(ProblemTeam.objects.filter(problem=problem, team__id=team_id)) == 0:
                probable_problems.append(problem)

        if len(probable_problems) == 0:
            return get_response("شما تمام سوالات این مبحث را گرفته‌اید!", {}, 400)

        team = get_object_or_404(Team, id=team_id)
        team.score = team.score - get_problem_cost(subject)
        team.save()
        problem = random.choice(probable_problems)
        problem_team = ProblemTeam(problem=problem, team=team, status=1, )
        problem_team.save()

        return get_response("سوال {} از مبحث {} با موفقیت گرفته شد!".format(problem.name, PROBLEM_SUBJECTS[subject][1]),
                            {})
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_problem(request):
    if request.method == "POST":
        id = request.POST.get('id')
        problem_team = get_object_or_404(ProblemTeam, id=id)
        data = '{{"name": "{}", "text": "{}", "answer": "{}", "status": "{}"}}' \
            .format(problem_team.problem.name, problem_team.problem.text, problem_team.answer, problem_team.status)
        return get_response("سوال با موفقیت دریافت شد!", data)
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def put_problem_in_auction(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        id = request.POST.get('id')
        cost = request.POST.get('cost')

        problem_team = ProblemTeam.objects.get(team__id=team_id, id=id)

        if not problem_team:
            return get_response("شما این سوال را نگرفته‌اید!", {}, 400)

        if problem_team.status != 3 or problem_team.score > 2:
            print(problem_team.status, problem_team.score)
            return get_response("شما نمی‌توانید این سوال را به مزایده بگذارید!", {}, 400)

        problem_team.status = 4
        problem_team.auction_cost = cost
        problem_team.save()

        return get_response("سوال با موفقیت به مزایده گذاشته شد!", {})
    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_problem_from_auction(request):
    if request.method == "POST":
        team_id = request.POST.get('team_id')
        id = request.POST.get('id')

        problem_team = ProblemTeam.objects.get(id=id)
        putter_team = problem_team.team
        getter_team = get_object_or_404(Team, id=team_id)

        if len(ProblemTeam.objects.filter(team__id=team_id, status=1)) >= 3:
            return get_response("نمی‌توانید هم‌زمان بیش از ۳ سوال داشته باشید!", {}, 400)

        if len(ProblemTeam.objects.filter(team__id=team_id, problem=problem_team.problem)) >= 1:
            return get_response("شما قبلاً این سوال را گرفته‌اید!", {}, 400)

        putter_team.score = putter_team.score + problem_team.auction_cost
        putter_team.save()

        getter_team.score = getter_team.score - problem_team.auction_cost
        getter_team.save()

        problem_team.status = 5
        problem_team.auction_cost = 0
        problem_team.save()

        new_problem_team = ProblemTeam(team=getter_team, problem=problem_team.problem, status=1)
        new_problem_team.save()

        return get_response("سوال با موفقیت از مزایده گرفته شد!", {})
    return get_response('این متد غیرمجاز است!', None, 405)
