import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Item, Customer
from .serializers import ItemSerializer, CustomerSerializer
from rest_framework import status



logger = logging.getLogger(__name__)



@api_view(['POST'])
def add_customer(request):
    
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        
        serializer.save()
    else:
        return Response(serializer.errors, status=400)
    return Response(serializer.data)

@api_view(['POST'])
def get_all_Customers(request):
    try:
        data = request.data 
        filter = data.get('filter', None)
        
        if filter == 'name':
            customers= Customer.objects.filter(name__icontains=data.get('data', ''))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        
        elif filter == 'email':    
            customers = Customer.objects.filter(details__email__icontains=data.get('data', ))
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)
      
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    except Exception as e:
        logger.error(f'Error at getAllCustomers {str(e)}', exc_info=True)

        return Response({"error": "No customers found"}, status=404)
    

@api_view(['DELETE'])
def deleteCustumer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response({'message': 'Cliente deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f'Error at deleteCustomer {str(e)}', exc_info=True)

        return Response({'error': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def update_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({'error': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    