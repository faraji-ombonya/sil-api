from rest_framework import serializers

from shop.models import Category, Product, Order, Customer, OrderItem
from user.serializers import UserSerializer
from utils.helpers import get_category_tree


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["category"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["categories"] = CategorySerializer(
            get_category_tree(instance.category), many=True
        ).data
        return representation


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        exclude = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order_items"] = OrderItemSerializer(
            instance.orderitem_set.all(), many=True
        ).data
        return representation


class ProductOrderSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist")
        return value


class CreateOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        exclude = ["total_price"]

    def create(self, validated_data):
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)

        # Create order items, and calculate total price. Creating order
        # items helps us freeze the price of the product at the time
        # of order
        total_price = 0
        for product in products:
            product_instance = Product.objects.get(id=product["product_id"])
            order_item = OrderItem.objects.create(
                product=product_instance,
                quantity=product["quantity"],
                price=product_instance.price,
                order=order,
            )
            total_price += order_item.price * order_item.quantity

        order.total_price = total_price
        order.save()
        return order


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = UserSerializer(instance.user).data
        return representation


class CreateCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"
