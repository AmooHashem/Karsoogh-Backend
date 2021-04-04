from django.shortcuts import render, get_object_or_404
import json
import uuid
from django.contrib.auth.hashers import make_password, check_password

from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Avg, Sum, Min, Max

from Api.decorators import check_token
from Api.forms import AnswerForm
from Formula0.utils import get_response
from Formula0.models import *


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            team_id = post_data.get('team_id')
            team = get_object_or_404(Team, id=team_id)
            return get_response('خوش آمدید!',
                                '{{"team_id": "{}", "voice_chat_link": "{}", "team_name": "{}"}}'
                                .format(team_id, team.voice_chat_link, team.name))
        except Exception as d:
            return get_response('تیمی با این شناسه وجود ندارد!', None, 404)

    return get_response('این متد غیرمجاز است!', None, 405)


@csrf_exempt
def get_problem_of_subject(request):
    # subject + id
    pass


@csrf_exempt
def submit_problem(request):
    # id
    pass
