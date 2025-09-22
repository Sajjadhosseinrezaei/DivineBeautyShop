from django.core.management.base import BaseCommand
from faker import Faker
import random
from products.models import Category, Product


class Command(BaseCommand):
    help = "ایجاد داده تستی برای دسته‌بندی‌ها، زیر دسته‌بندی‌ها و محصولات"

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='تعداد دسته‌بندی‌های اصلی برای ایجاد'
        )
        parser.add_argument(
            '--subcategories',
            type=int,
            default=3,
            help='تعداد زیر دسته‌بندی برای هر دسته‌بندی'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=10,
            help='تعداد محصولات برای هر زیر دسته‌بندی'
        )

    def handle(self, *args, **options):
        fake = Faker('fa_IR')
        categories_count = options['categories']
        subcategories_count = options['subcategories']
        products_count = options['products']

        self.stdout.write(self.style.NOTICE("در حال ایجاد دسته‌بندی‌ها و زیر دسته‌بندی‌ها..."))

        for _ in range(categories_count):
            # دسته‌بندی اصلی
            parent_category = Category.objects.create(
                name=fake.word(),
                is_active=True
            )

            for _ in range(subcategories_count):
                # زیر دسته‌بندی
                sub_category = Category.objects.create(
                    name=fake.word(),
                    parent=parent_category,
                    is_active=True
                )

                # محصولات مربوط به زیر دسته‌بندی
                for _ in range(products_count):
                    Product.objects.create(
                        name=fake.word(),
                        description=fake.text(max_nb_chars=200),
                        price=random.randint(10000, 500000),
                        stock=random.randint(0, 100),
                        is_available=random.choice([True, False]),
                        is_featured=random.choice([True, False]),
                        category=sub_category
                    )

        self.stdout.write(self.style.SUCCESS("✅ دسته‌بندی‌ها، زیر دسته‌بندی‌ها و محصولات تستی ساخته شدند."))
