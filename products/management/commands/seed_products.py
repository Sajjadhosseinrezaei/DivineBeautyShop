from django.core.management.base import BaseCommand
from faker import Faker
import random
from uuid import uuid4
from products.models import Category, Product


class Command(BaseCommand):
    help = "Generate test data for categories, subcategories, and products"

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Number of main categories to create'
        )
        parser.add_argument(
            '--subcategories',
            type=int,
            default=3,
            help='Number of subcategories per category'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=10,
            help='Number of products per subcategory'
        )

    def handle(self, *args, **options):
        fake = Faker('fa_IR')
        categories_count = options['categories']
        subcategories_count = options['subcategories']
        products_count = options['products']

        self.stdout.write(self.style.NOTICE("Starting test data generation..."))

        try:
            for cat_index in range(categories_count):
                # Unique name to avoid duplicate slugs
                base_name = fake.word()
                unique_name = f"{base_name}-{uuid4().hex[:6]}"

                parent_category = Category.objects.create(
                    name=unique_name,
                    is_active=True,
                    display_order=cat_index
                )
                self.stdout.write(self.style.NOTICE(f"Created category: {parent_category.name}"))

                for sub_index in range(subcategories_count):
                    base_sub = fake.word()
                    unique_sub_name = f"{base_sub}-{uuid4().hex[:6]}"

                    sub_category = Category.objects.create(
                        name=unique_sub_name,
                        parent=parent_category,
                        is_active=True,
                        display_order=sub_index
                    )
                    self.stdout.write(self.style.NOTICE(f"  Created subcategory: {sub_category.name} (parent: {parent_category.name})"))

                    for prod_index in range(products_count):
                        prod_name = f"{fake.word()}-{uuid4().hex[:6]}"

                        Product.objects.create(
                            name=prod_name,
                            description=fake.text(max_nb_chars=200),
                            price=random.randint(10000, 500000),
                            stock=random.randint(0, 100),
                            is_available=random.choice([True, False]),
                            is_featured=random.choice([True, False]),
                            category=sub_category
                        )
                    self.stdout.write(self.style.SUCCESS(f"    {products_count} products created for subcategory '{sub_category.name}'"))

            self.stdout.write(self.style.SUCCESS("✅ Test categories, subcategories, and products created successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR("❌ Error while generating test data:"))
            self.stderr.write(self.style.ERROR(str(e)))
            raise
