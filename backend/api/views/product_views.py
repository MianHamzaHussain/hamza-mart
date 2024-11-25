from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from api.models import Product, Review
from api.serializers import ProductSerializer

from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def getProducts(request):
    try:
        query = request.query_params.get('keyword', '')
        products = Product.objects.filter(
            name__icontains=query
        ).order_by('-createdAt')
        
        page = request.query_params.get('page', 1)
        paginator = Paginator(products, 5)
        
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            message = {'detail': 'Page number out of range'}
            return Response(
                message,
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ProductSerializer(products, many=True)
        return Response({
            'products': serializer.data,
            'page': int(page),
            'pages': paginator.num_pages
        })
    
    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getTopProducts(request):
    try:
        products = Product.objects.filter(rating__gte=4).order_by('-rating')
        serializer = ProductSerializer(products[:5], many=True)
        if not serializer.data:
            return Response(
                {
                    "detail": "Products exist, but none have been reviewed yet.",
                    "products": []
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )




@api_view(['GET'])
def getProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(
            {"detail": f"Product with ID '{pk}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError:
        return Response(
            {"detail": "Invalid product ID format."},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    data = request.data
    required_fields = ['name', 'price', 'brand', 'countInStock', 'category', 'description']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return Response(
            {"detail": f"Missing required fields: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        product = Product.objects.create(
            user=request.user,
            name=data['name'],
            price=data['price'],
            brand=data['brand'],
            countInStock=data['countInStock'],
            category=data['category'],
            description=data['description']
        )

        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    required_fields = ['name', 'price', 'brand', 'countInStock', 'category', 'description']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return Response(
            {"detail": f"Missing required fields: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        product = Product.objects.get(id=pk)
        product.name = data['name']
        product.price = data['price']
        product.brand = data['brand']
        product.countInStock = data['countInStock']
        product.category = data['category']
        product.description = data['description']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            print("Image updated successfully.")
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response(
            {"detail": f"Product with ID '{pk}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError:
        return Response(
            {"detail": "Invalid product ID format."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"detail":str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return Response({"detail": "Product Deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(
            {"detail": f"Product with ID '{pk}' not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError:
        return Response(
            {"detail": "Invalid product ID format."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"detail":str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Product, Review
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    try:
        user = request.user
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(
                {"detail": f"Product with ID '{pk}' not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data

        alreadyExists = product.review_set.filter(user=user).exists()
        if alreadyExists:
            return Response(
                {"detail": "Product already reviewed by this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        if 'rating' not in data or data['rating'] == 0:
            return Response(
                {"detail": "Please provide a valid rating. Rating cannot be zero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'comment' in data and len(data['comment']) > 1000:
            return Response(
                {"detail": "Comment is too long. Please limit it to 1000 characters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data.get('comment', ''),
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = sum(review.rating for review in reviews)
        product.rating = total / len(reviews)
        product.save()

        return Response(
            {"detail": "Review added successfully."},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        message = {'detail': str(e)}
        return Response(
            message,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

