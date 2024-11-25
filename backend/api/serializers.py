from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, ShippingAddress, Review

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    def get_isAdmin(self, obj):
        try:
            return obj.is_staff
        except AttributeError:
            return False

    def get_name(self, obj):
        try:
            name = obj.first_name if obj.first_name else obj.email
        except AttributeError:
            name = ''
        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        try:
            token = RefreshToken.for_user(obj)
            return str(token.access_token)
        except Exception:
            return None

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        try:
            reviews = obj.review_set.all()
            serializer = ReviewSerializer(reviews, many=True)
            return serializer.data
        except Exception:
            return []

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        try:
            items = obj.orderitem_set.all()
            serializer = OrderItemSerializer(items, many=True)
            return serializer.data
        except Exception:
            return []

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except AttributeError:
            address = None
        return address

    def get_user(self, obj):
        try:
            user = obj.user
            serializer = UserSerializer(user, many=False)
            return serializer.data
        except AttributeError:
            return None
