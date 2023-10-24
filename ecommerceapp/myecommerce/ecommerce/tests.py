from django.test import TestCase
from .models import Product, Category, Store

class ProductTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Electronics", description="Electronic products")
        store = Store.objects.create(name="Gadget Store", description="A store for gadgets")
        self.product = Product.objects.create(
            name="Smartphone",
            description="A high-end smartphone",
            price=999.99,
            store=store,
            category=category,
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Smartphone")
        self.assertEqual(product.name, "Smartphone")
        self.assertEqual(product.description, "A high-end smartphone")
        self.assertEqual(product.price, 999.99)
        self.assertEqual(product.store.name, "Gadget Store")
        self.assertEqual(product.category.name, "Electronics")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Smartphone")

    def test_product_price(self):
        self.assertTrue(self.product.price > 0)

    def test_product_category(self):
        self.assertEqual(self.product.category.name, "Electronics")

    def test_product_store(self):
        self.assertEqual(self.product.store.name, "Gadget Store")
