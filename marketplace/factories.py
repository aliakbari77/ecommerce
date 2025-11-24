# factories.py

import random
from faker import Faker
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from marketplace.models import (
    Category, Product, Order, OrderItem,
    Review, Discount
)

fake = Faker()
User = get_user_model()


# ------------------------
# User Factories
# ------------------------
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    is_customer = False
    is_vendor = False


class CustomerFactory(UserFactory):
    is_customer = True


class VendorFactory(UserFactory):
    is_vendor = True


# ------------------------
# Category Factories (Hierarchical)
# ------------------------
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    parent = None  # Level 1


class SubCategoryFactory(CategoryFactory):
    parent = factory.SubFactory(CategoryFactory)  # Level 2


class SubSubCategoryFactory(CategoryFactory):
    parent = factory.SubFactory(SubCategoryFactory)  # Level 3


# ------------------------
# Product Factory
# ------------------------
class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    vendor = factory.SubFactory(VendorFactory)
    stock = factory.Faker("pyint", min_value=0, max_value=500)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            # Random categories if none provided
            all_categories = list(Category.objects.all())
            if all_categories:
                self.categories.add(random.choice(all_categories))


# ------------------------
# Order & OrderItem Factories
# ------------------------
class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    status = factory.Iterator(["pending", "paid", "shipped", "cancelled"])
    total_price = 0  # Will update after adding items


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=5)
    price = factory.LazyAttribute(lambda obj: obj.product.price)


# ------------------------
# Review Factory
# ------------------------
class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    customer = factory.SubFactory(CustomerFactory)
    rating = factory.Faker("pyint", min_value=1, max_value=5)
    comment = factory.Faker("sentence")
    created_at = factory.Faker("date_time_this_year")


# ------------------------
# Discount Factory
# ------------------------
class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    name = factory.Faker("word")
    code = factory.Faker("bothify", text="DISCOUNT-####")
    amount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    active = True
    start_date = factory.Faker("past_datetime", start_date="-30d")
    end_date = factory.Faker("future_datetime", end_date="+30d")

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for product in extracted:
                self.products.add(product)
        else:
            all_products = list(Product.objects.all())
            if all_products:
                self.products.add(random.choice(all_products))
