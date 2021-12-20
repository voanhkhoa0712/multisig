
from django.shortcuts import render
from django.http import HttpResponse
from .party import Party
import json


party = Party(3, 5)


def response_json(data: dict):
    return HttpResponse(json.dumps(data), content_type = 'application/json')


def index(request):
    return render(request, 'index.html')


def remove_user(request):
    name = request.GET.get('user')
    result = {'user': party.remove_user(name)}
    return response_json(result)


def create_user(request):
    name = request.GET.get('user')
    data = party.create_user(name)
    if data == False:
        return response_json({'stat': False})
    pk, poly = data
    result = {}
    result['stat'] = True
    result['poly'] = [str(i) for i in poly]
    result['pk_x'] = str(pk.x)
    result['pk_y'] = str(pk.y)
    return response_json(result)


def set_status(request):
    stat = request.GET.get('stat')
    name = request.GET.get('user')
    stat = party.set_user_status(name, stat)
    result = {'stat': stat}
    return response_json(result)


def view_secret(request):
    name = request.GET.get('user')
    data = party.view_secret(name)
    if data == False:
        return response_json({'stat': False})
    x_key, share = data
    result = {'x_key': str(x_key), 'share': str(share)}
    return response_json(result)


def view_nonce(request):
    name = request.GET.get('user')
    data = party.view_nonce(name)
    if data == False:
        return response_json({'stat': False})
    p1, s1 = data
    result = {}
    result['stat'] = True
    result['p1_x'] = str(p1.x)
    result['p1_y'] = str(p1.y)
    result['s1_k'] = str(s1)
    return response_json(result)





def admin(request):
    return render(request, 'admin.html')


def list_member(request):
    result = {'user': party.list_member()}
    return response_json(result)


def reset_member(request):
    party.reset_member()
    return response_json({})


def setup_party(request):
    result = {'stat': party.setup_group()}
    return response_json(result)


def sign_message(request):
    data = request.GET.get('data')
    data = party.sign_message(data)
    if data == False:
        return response_json({'stat': False})
    p, r, s = data
    result = {}
    result['stat'] = True
    result['s'] = str(s)
    result['px'] = str(p.x)
    result['py'] = str(p.y)
    result['rx'] = str(r.x)
    result['ry'] = str(r.y)
    return response_json(result)