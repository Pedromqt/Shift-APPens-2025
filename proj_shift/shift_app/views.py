import json
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Cliente

@csrf_exempt
def registar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cliente = Cliente(
                nome_completo=data.get('nome_completo'),
                password=make_password(data.get('password')),
                email=data.get('email'),
                idade=data.get('idade'),
                morada=data.get('morada'),
                observacoes=data.get('observacoes')
            )

            cliente.full_clean()
            cliente.save()

            return JsonResponse({
                'id': cliente.id,
                'nome_completo': cliente.nome_completo,
                'email': cliente.email,
                'idade': cliente.idade,
                'morada': cliente.morada,
                'observacoes': cliente.observacoes
            }, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def remover_cliente(request, id):
    if request.method == 'DELETE':
        try:
            cliente = Cliente.objects.get(pk=id)
            cliente.delete()
            return JsonResponse({'mensagem': 'Cliente removido com sucesso'}, status=200)
        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)


@csrf_exempt
def atualizar_cliente(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(pk=id)
            cliente.nome_completo = data.get('nome_completo', cliente.nome_completo)
            cliente.email = data.get('email', cliente.email)
            cliente.idade = data.get('idade', cliente.idade)
            cliente.morada = data.get('morada', cliente.morada)
            cliente.observacoes = data.get('observacoes', cliente.observacoes)

            if 'password' in data:
                cliente.password = make_password(data['password'])

            cliente.full_clean()
            cliente.save()

            return JsonResponse({
                'id': cliente.id,
                'nome_completo': cliente.nome_completo,
                'email': cliente.email,
                'idade': cliente.idade,
                'morada': cliente.morada,
                'observacoes': cliente.observacoes
            }, status=200)

        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
        except ValidationError as e:
            return JsonResponse({'erro': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)


@csrf_exempt
def login_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            cliente = Cliente.objects.get(email=email)

            if check_password(password, cliente.password):
                return JsonResponse({
                    'id': cliente.id,
                    'nome_completo': cliente.nome_completo,
                    'email': cliente.email
                }, status=200)
            else:
                return JsonResponse({'erro': 'Senha incorreta'}, status=401)

        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def morada_cliente(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
            return JsonResponse({'morada': cliente.morada})
        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def obs_cliente(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
            return JsonResponse({'observasoes': cliente.observacoes})
        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)         