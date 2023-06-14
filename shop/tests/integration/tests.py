from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Let's create two categories, only one of which is active
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(
            name='Légumes', active=False)

        # Let's create two products, only one of which is active
        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(
            name='Banane', active=False)

        # Let's create another category with a product active
        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(
            name='Tomate', active=True)

    def format_datetime(self, value):
        # This method is a helper to format a date
        # in string of characters in the same format as that of the api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestCategory(ShopAPITestCase):
    # We store the endpoint url in a class attribute
    # so we can use it more easily in each of our tests
    url = reverse_lazy('shop:category-list')

    def test_list(self):

        # The call is made in GET using the client of the test class
        response = self.client.get(self.url)
        # We check that the status code is 200
        # and that the values returned are those expected
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in [self.category, self.category_2]
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # We save the count of category
        category_count = Category.objects.count()
        response = self.client.post(
            self.url, data={'name': 'Nouvelle catégorie'})
        # Let's check that the status code is in error
        # and prevents us from creating a category
        self.assertEqual(response.status_code, 405)
        # Finally, let's check that the count is same
        # despite the status code 405
        self.assertEqual(Category.objects.count(), category_count)


class TestProduct(ShopAPITestCase):
    url = reverse_lazy('shop:product-list')

    def get_product_detail_data(self, products):
        # fields = ['id', 'name', 'date_created', 'date_updated', 'category']
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id
            } for product in products
        ]

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data(
            [self.product, self.product_2]), response.json())

    def test_list_filter(self):
        response = self.client.get(
            self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_product_detail_data([self.product]), response.json())

    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(
            self.url, data={'name': 'Nouveau produit'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    def test_delete(self):
        response = self.client.delete(
            reverse('shop:product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
