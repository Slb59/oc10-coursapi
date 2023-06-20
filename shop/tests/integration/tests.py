from unittest import mock

from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product
from shop.mocks import mock_openfoodfact_success, ECOSCORE_GRADE


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

    def get_article_list_data(self, articles):
        return [
            {
                'id': article.pk,                
                'date_created': self.format_datetime(article.date_created),
                'date_updated': self.format_datetime(article.date_updated),
                'name': article.name,
                'product': article.product_id,
                'price': article.price
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'description': product.description,
                'category': product.category_id,
                'ecoscore': ECOSCORE_GRADE
            } for product in products
        ]

    def get_product_detail_data(self, product):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id,
                'articles': self.get_article_list_data(
                    product.articles.filter(active=True))
            }
        ]

    def get_category_list_data(self, categories):
        return [
            {
                'id': category.id,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
                'description': ''
                # 'products': self.get_product_list_data(
                #     category.products.filter(active=True))
            } for category in categories
        ]


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
        self.assertEqual(
            response.json()['results'],
            self.get_category_list_data([self.category, self.category_2])
            )

    def test_detail(self):

        url_detail = reverse(
            'shop:category-detail', kwargs={'pk': self.category.pk}
            )
        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, 200)
        excepted = {
            'id': self.category.pk,
            'name': self.category.name,
            'date_created': self.format_datetime(self.category.date_created),
            'date_updated': self.format_datetime(self.category.date_updated),
            'products': self.get_product_list_data(
                self.category.products.filter(active=True)),
        }
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

    def test_detail(self):
        response = self.client.get(
            reverse('shop:product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_product_detail_data(self.product)
            )

    @mock.patch(
        'shop.models.Product.call_external_api',
        mock_openfoodfact_success
        )
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_product_list_data([self.product, self.product_2])
            )

    @mock.patch(
        'shop.models.Product.call_external_api',
        mock_openfoodfact_success
        )
    def test_list_filter(self):
        response = self.client.get(
            self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_product_list_data([self.product]))

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
