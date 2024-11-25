from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.models import Product, Order, OrderItem, ShippingAddress
from api.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    try:
        orderItems = data.get('orderItems', [])

        if not orderItems or len(orderItems) == 0:
            return Response({'detail': 'No Order Items provided.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  
            order = Order.objects.create(
                user=user,
                paymentMethod=data.get('paymentMethod', ''),
                taxPrice=data.get('taxPrice', 0),
                shippingPrice=data.get('shippingPrice', 0),
                totalPrice=data.get('totalPrice', 0),
            )

            shipping_data = data.get('shippingAddress', {})
            if not all(k in shipping_data for k in ['address', 'city', 'postalCode', 'country']):
                return Response({'detail': 'Incomplete shipping address.'}, status=status.HTTP_400_BAD_REQUEST)

            ShippingAddress.objects.create(
                order=order,
                address=shipping_data['address'],
                city=shipping_data['city'],
                postalCode=shipping_data['postalCode'],
                country=shipping_data['country'],
            )

            for item_data in orderItems:
                try:
                    product = Product.objects.get(id=item_data['product'])
                except Product.DoesNotExist:
                    return Response({'detail': f"Product with ID {item_data['product']} not found."},
                                    status=status.HTTP_404_NOT_FOUND)

                if product.countInStock < item_data['qty']:
                    return Response({'detail': f"Not enough stock for product: {product.name}."},
                                    status=status.HTTP_400_BAD_REQUEST)

                OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    qty=item_data['qty'],
                    price=item_data['price'],
                    image=product.image.url,
                )

                product.countInStock -= item_data['qty']
                product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except KeyError as e:
        return Response({'detail': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    try:
        user = request.user
        orders = user.order_set.all()
        if not orders.exists():
            return Response(
                {'detail': 'No orders found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
           str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    try:
        orders = Order.objects.all()
        if not orders.exists():
            return Response(
                {'detail': 'No orders found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Not authorized to view this order'},
                status=status.HTTP_403_FORBIDDEN
            )

    except Order.DoesNotExist:
        return Response(
            {'detail': 'Order does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        return Response(
            str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    try:
        order = Order.objects.get(id=pk)
        if request.user.is_staff or order.user == request.user:
            order.isPaid = True
            order.paidAt = datetime.now()
            order.save()
            return Response(
                {'detail': 'Order marked as paid'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'detail': 'Not authorized to update this order'},
                status=status.HTTP_403_FORBIDDEN
            )

    except Order.DoesNotExist:
        return Response(
            {'detail': 'Order does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    try:
        order = Order.objects.get(_id=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response(
            {'detail': 'Order marked as delivered'},
            status=status.HTTP_200_OK
        )
    except Order.DoesNotExist:
        return Response(
            {'detail': 'Order does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
         str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
