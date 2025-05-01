import json
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Cliente

@csrf_exempt
def registar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cliente = Cliente(
                nome_completo=data.get('nome_completo'),
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
def remover_cliente(request, cliente_id):
    if request.method == 'DELETE':
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente.delete()
            return JsonResponse({'mensagem': 'Cliente removido com sucesso'}, status=200)
        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
