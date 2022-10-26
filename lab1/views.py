import json

from django.shortcuts import render, redirect
import psycopg2
from rest_framework.decorators import api_view
import requests
from lab1.database_management import DB
from lab1.models import Films
from rest_framework.response import Response

"""
id
name 
score
"""

db = DB()
db_name = 'lab1_films'


# db.create('Films', Name='VARCHAR(50) NOT NULL', Score='INTEGER DEFAULT 0')

@api_view(['GET'])
def index(request):
    data = db.select(db_name)
    table = []
    for el in data:
        table.append({
            'id': el[0],
            'name': el[1],
            'score': el[2]}
        )

    context = {
        'table': table
    }
    return render(request, 'lab1/index.html', context=context)


@api_view(['GET'])
def delete(request, id_films):
    db.delete(db_name, id_film=id_films)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@api_view(['POST'])
def push(request):
    data = request.data
    db.push(
        table_name=db_name,
        id_films=data['id'],
        name=data['name'],
        score=data['score']
    )
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@api_view(['POST'])
def insert(request):
    data = request.data
    db.insert(db_name, data['name'], data['score'])
    return redirect('home')


@api_view(['GET'])
def orm_read(request):
    films = Films.objects.all()
    context = {
        'table': films
    }
    return render(request, 'lab1/index.html', context=context)


@api_view(['GET'])
def orm_delete(request, id_films):
    if Films.objects.filter(id=id_films).exists():
        Films.objects.get(id=id_films).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@api_view(['POST'])
def orm_insert(request):
    data = request.data
    Films(
        name=data['name'],
        score=data['score']
    ).save()
    return redirect('home')


@api_view(['POST'])
def orm_update(request):
    data = request.data
    if Films.objects.filter(id=data['id']).exists():
        films = Films.objects.get(id=data['id'])
        if data['name'] != '':
            films.name = data['name']
        if data['score'] != '':
            films.score = data['score']
        films.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@api_view(['GET'])
def get_api(request):
    res = requests.get('https://cdn.cur.su/api/latest.json')
    with open('currency.json', 'w') as f:
        json.dump(res.json(), f, sort_keys=True, indent=2)
    return Response(data=res.json(), status=200)
