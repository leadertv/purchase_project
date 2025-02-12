from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import Shop, Category, Product, ProductPrice, Order, OrderItem, UserContact

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Сериализатор для регистрации
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'], 
            password=validated_data['password']
        )
        return user

# Сериализатор для магазина
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

# Сериализатор для категории
class CategorySerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'

# Сериализатор для цены товара
class ProductPriceSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(read_only=True)
    
    class Meta:
        model = ProductPrice
        fields = ['shop', 'price', 'quantity']

# Сериализатор для товара
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    prices = ProductPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

# Сериализатор для позиции заказа
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'shop', 'price', 'quantity']

# Сериализатор для заказа
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'delivery_address', 'items']

# Сериализатор для добавления позиции в корзину (используем id-шники)
class AddOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    shop_id = serializers.IntegerField()
    
    class Meta:
        model = OrderItem
        fields = ['product_id', 'shop_id', 'price', 'quantity']

# Сериализатор для контактов пользователя
class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

# Сериализаторы для восстановления пароля

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            uid = data.get('uid')
            token = data.get('token')
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            raise serializers.ValidationError("Неверные uid или token")
        
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Неверный token или срок действия токена истек")
        
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
