import random
from django.core.management.base import BaseCommand
from marketplace.factories import (
    CategoryFactory, SubCategoryFactory, SubSubCategoryFactory,
    VendorFactory, CustomerFactory, ProductFactory,
    OrderFactory, OrderItemFactory, ReviewFactory, DiscountFactory
)

class Command(BaseCommand):
    help = "Seed the database with realistic e-commerce data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # ------------------------
        # Categories
        # ------------------------
        top_cats = CategoryFactory.create_batch(10)
        sub_cats = SubCategoryFactory.create_batch(30)
        sub_sub_cats = SubSubCategoryFactory.create_batch(100)

        # ------------------------
        # Vendors & Customers
        # ------------------------
        vendors = VendorFactory.create_batch(50)
        customers = CustomerFactory.create_batch(200)

        # ------------------------
        # Products
        # ------------------------
        products = ProductFactory.create_batch(500)

        # ------------------------
        # Orders & OrderItems
        # ------------------------
        for _ in range(1000):
            order = OrderFactory(customer=random.choice(customers))
            items_count = random.randint(1, 5)
            for _ in range(items_count):
                OrderItemFactory(order=order, product=random.choice(products))

            # Update total price
            total = sum(item.price * item.quantity for item in order.items.all())
            order.total_price = total
            order.save()

        # ------------------------
        # Reviews
        # ------------------------
        ReviewFactory.create_batch(1000)

        # ------------------------
        # Discounts
        # ------------------------
        DiscountFactory.create_batch(50)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
