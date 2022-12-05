from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render
from django.db.models import Q
from .models import *
import threading, queue

my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def all_true(request):
    for i in Inventory.objects.all():
        i.download = False
        i.save()
    return HttpResponse('')

@storeInQueue
def Validated_Update(request, code):
	i = Inventory.objects.get(code = code)
	if i.vera == True and i.col == True and i.cali == True:
		i.update = False
		i.save()

@storeInQueue
def Validated_New(request, code):
	i = Inventory.objects.get(code = code)
	if i.vera == True and i.col == True and i.cali == True:
		i.new_product = False
		i.save()

@api_view(['POST'])
def Update_Product_Sede(request):
	data = request.data
	i = Inventory.objects.get(code = data['code'])
	if data['sede'] == 1:
		i.vera = data['campo']
	elif data['sede'] == 2:
		i.col = data['campo']
	elif data['sede'] == 3:
		i.cali = data['campo']
	i.save()
	u = threading.Thread(target=Validated_Update,args=(request,data['code']), name='PDF')
	u.start()
	return Response({'Message':True})

@api_view(['POST'])
def New_Product_Sede(request):
	data = request.data
	print(data)
	i = Inventory.objects.get(code = data['code'])
	if data['sede'] == 1:
		i.vera = data['campo']
	elif data['sede'] == 2:
		i.col = data['campo']
	elif data['sede'] == 3:
		i.cali = data['campo']
	i.save()
	u = threading.Thread(target=Validated_New,args=(request,data['code']), name='PDF')
	u.start()
	return Response({'Message':True})


@api_view(['POST'])
def GetInventory(request):
	data = request.data
	inventory = Inventory.objects.filter(Q(new_product = True) | Q(update=True)).order_by('pk')
	data = [
		{
            "code": i.code,
            "code_int": i.code_int,
            "name": i.name,
            'cost':i.cost,
            "price_1": i.price_1,
            "price_2": i.price_2,
            "price_3": i.price_3,
            "price_4": i.price_4,
            "price_5": i.price_5,
            "tax":i.tax,
            "category":i.category,
            "active" : i.active,
            'new':i.new_product,
            'update':i.update,
            'vera':i.vera,
            'col':i.col,
            'cali':i.cali
		}
		for i in inventory
	]

	return Response(data)


@api_view(['POST'])
def SetInventory(request):
	data = request.data
	message= False
	try:
		Inventory(
			code = data['code'],
			code_int = data['code_int'],
			name = data['name'],
			cost = data['cost'],
			price_1 = data['price_1'],
			price_2 = data['price_2'],
			price_3 = data['price_3'],
			price_4 = data['price_4'],
			price_5 = data['price_5'],
			tax = data['tax'],
			category = data['category'],
			active = True,
			new_product = True,
			vera = False,
			col = False,
			cali = False,
		).save()
		message = True
	except Exception as e:
		print(e)

	return Response({'Message':message})



@api_view(['POST'])
def Update_Product(request):
	data = None
	data = request.data
	try:
	    inv = Inventory.objects.get(code = data['code'])
	    inv.code_int = data['code_int']
	    inv.name = data['name']
	    inv.cost = data['cost']
	    inv.price_1 = data['price_1']
	    inv.price_2 = data['price_2']
	    inv.price_3 = data['price_3']
	    inv.price_4 = data['price_4']
	    inv.price_5 = data['price_5']
	    inv.tax = data['tax']
	    inv.cat = data['category']
	    inv.update = True
	    inv.vera = False
	    inv.col = False
	    inv.cali = False
	    inv.save()
	    message = True
	except Exception as e:
	    message = e
	return Response({'Message':message})

@api_view(['POST'])
def Delete_Product(request):
	data = request.data
	inv = Inventory.objects.get(code = data['code'])
	inv.active = False
	inv.update = True
	inv.vera = False
	inv.col = False
	inv.cali = False
	inv.save()
	return Response({'Message':True})

@api_view(['POST'])
def Delete_Record(request):
	data = request.data
	i = Inventory.objects.get(code = data['code'])
	if data['sede'] == 1:
		i.vera = data['campo']
	elif data['sede'] == 2:
		i.col = data['campo']
	elif data['sede'] == 3:
		i.cali = data['campo']
	i.save()
	if i.vera == True and i.col == True and i.cali == True and i.active == False:
	    i.delete()
	return Response({'Message':True})








