#! /usr/bin/env python3
# coding: utf-8
from unittest.mock import patch
from django.test import TestCase
from ..management.commands.dbinit import DBInit
from django.contrib.auth.models import User
from..models import Product, Category, Profile

class TestCommandDBInit(TestCase):
    """
    This class groups the unit tests linked to the public methods from
    the DBInit class (command to initialize the database for the beta app [< 10k rows])
    """

    maxDiff= None

    @classmethod
    def setUpTestData(cls):
        """
        The objective is to integrate some categories and products with their relations
        in order to tests the query analysis' methods on a similar environment than the production
        """

        categories = [
            {
                "products": 32107,
                "name": "Aliments et boissons à base de végétaux",
                "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
                "id": "en:plant-based-foods-and-beverages"
            },
            {
                "id": "en:plant-based-foods",
                "url": "https://fr.openfoodfacts.org/categorie/aliments-d-origine-vegetale",
                "products": 27435,
                "name": "Aliments d'origine végétale"
            },
            {
                "products": 21875,
                "name": "Boissons",
                "url": "https://fr.openfoodfacts.org/categorie/boissons",
                "sameAs": [
                    "https://www.wikidata.org/wiki/Q40050"
                ],
                "id": "en:beverages"
            },
            {
                "url": "https://fr.openfoodfacts.org/categorie/boissons-non-sucrees",
                "name": "Boissons non sucrées",
                "products": 9153,
                "id": "en:non-sugared-beverages"
            },
            {
                "products": 8006,
                "name": "Produits fermentés",
                "url": "https://fr.openfoodfacts.org/categorie/produits-fermentes",
                "id": "en:fermented-foods"
            },
            {
                "id": "en:fermented-milk-products",
                "sameAs": [
                    "https://www.wikidata.org/wiki/Q3506176"
                ],
                "products": 8002,
                "name": "Produits laitiers fermentés",
                "url": "https://fr.openfoodfacts.org/categorie/produits-laitiers-fermentes"
            },
            {
                "id": "en:non-alcoholic-beverages",
                "url": "https://fr.openfoodfacts.org/categorie/boissons-sans-alcool",
                "products": 7646,
                "name": "Boissons sans alcool"
            },
            {
                "url": "https://fr.openfoodfacts.org/categorie/biscuits-et-gateaux",
                "products": 7294,
                "name": "Biscuits et gâteaux",
                "id": "en:biscuits-and-cakes"
            },
            {
                "id": "en:meats",
                "products": 7191,
                "name": "Viandes",
                "url": "https://fr.openfoodfacts.org/categorie/viandes"
            },
            {
                "id": "en:spreads",
                "url": "https://fr.openfoodfacts.org/categorie/produits-a-tartiner",
                "products": 6724,
                "name": "Produits à tartiner"
            },
        ]

        products = [
            {
                "product_name_fr": "Le jus de raisin 100% jus de fruits",
                "code": "123456789",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr" : "jus de fruit naturel sans sucre ajouté",
                "categories_hierarchy": [
                    "en:plant-based-foods-and-beverages",
                    "en:beverages",
                ],
            },
            {
                "product_name_fr": "Le haricot 100% naturellement bleue",
                "code": "987654321",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "nutrition_grade_fr": "b",
                "generic_name_fr" : "",
                "categories_hierarchy": [
                    "en:plant-based-foods",
                ],
            },
            {
                "product_name_fr": "cola à la mousse de bière",
                "code": "456789123",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "d",
                "generic_name_fr" : "du coca et de la bière, ca mousse pas mal",
                "categories_hierarchy": [
                    "en:beverages",
                    "en:plant-based-foods-and-beverages",
                ],
            },
            {
                "product_name_fr": "Banane à la feuille de coca",
                "code": "12345787459",
                "image_url":"https://static.openfoodfacts.org/images/products/609/109/100/0301/front_fr.13.100.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "",
                "categories_hierarchy": [
                    "en:plant-based-foods-and-beverages",
                    "en:beverages",
                    "en:biscuits-and-cakes"
                ],
            },
            {
                "product_name_fr": "steack charal",
                "code": "987695121",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "generic_name_fr":"mmmmmmhhhh Charal!!",
                "nutrition_grade_fr": "a",
                "categories_hierarchy": [
                    "en:meats",
                ],
            },
            {
                "product_name_fr": "nutella plein d'huiles de palme",
                "code": "456789123",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "pas bon pour les singes et les artères",
                "categories_hierarchy": [
                    "en:spreads",
                ],
            },
            {
                "product_name_fr": "steack de fausses viandes",
                "code": "987751251",
                "image_url": "https://static.openfoodfacts.org/images/products/152/haricot.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "ca a le gout de viande, mais c'est pas de la viande",
                "categories_hierarchy": [
                    "en:meats",
                ],
            },
            {
                "product_name_fr": "lait demi-écrémé pour une meilleure digestion",
                "code": "474369523",
                "image_url": "https://static.openfoodfacts.org/images/products/152/on-en-reve-tous.jpg",
                "nutrition_grade_fr": "a",
                "generic_name_fr": "lait de vache frais",
                "categories_hierarchy": [
                    "en:non-alcoholic-beverages",
                    "en:fermented-milk-products"
                ],
            },
        ]

        for category in categories:
            Category.objects.create(name=category["name"].lower(),
                                    api_id=category["id"].lower(),
                                    total_products=category["products"],
                                    enough_good_nutriscore=True)

        for product in products:
            new_product = Product.objects.create(name=product["product_name_fr"].lower(),
                                   ref=product["code"],
                                   nutriscore=product["nutrition_grade_fr"],
                                   picture=product["image_url"],
                                   description=product["generic_name_fr"])
            
            for category in product["categories_hierarchy"]:
                try:
                    cat_in_db = Category.objects.get(api_id=category) 
                    new_product.categories.add(cat_in_db)
                except:
                    pass

        # We create some users
        
        #First one
        username = 'test-ref'
        mail = 'test-ref@register.com'
        password = 'ref-test-view'
        password_check = 'ref-test-view'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="123456789")
        user_profile.products.add(product.id)
        product = Product.objects.get(ref="987654321")
        user_profile.products.add(product.id)

        #Second one
        username = 'test-update'
        mail = 'test-update@dbinit.com'
        password = 'ref-update'
        password_check = 'ref-update'
        user = User.objects.create_user(username, mail, password)
        user_profile = Profile(user=user)
        user_profile.save()
        product = Product.objects.get(ref="123456789")
        user_profile.products.add(product.id)
        product = Product.objects.get(ref="474369523")
        user_profile.products.add(product.id)

    def setUp(self):
        self.db_init = DBInit()

    def test_clean_db_without_data(self):
        """
        This method tests if the method deletes all the data from the database
        """

        self.db_init.clean_db()

        query = Category.objects.all().exists()
        self.assertEqual(query, False)

        query = Product.objects.all().exists()
        self.assertEqual(query, False)

        query = User.objects.all().exists()
        self.assertEqual(query, False)

        query = Profile.objects.all().exists()
        self.assertEqual(query, False)
    
    @patch('search.management.commands.dbinit.DBInit._get_categories_from_api')
    def test_db_update(self, mock_get_categories_from_api):
        """
        The objective is to test if the update works when there are some datas in the database
        """
        pass

    @patch('search.management.commands.dbinit.DBInit._get_from_api_products_info_from_page_category')
    @patch('search.management.commands.dbinit.DBInit._get_categories_from_api')
    def test_db_create(self, mock_get_categories_from_api, mock_api_product):
        """
        The idea is to test if the database is cleaned with news datas when we want to recreate the database
        """

        products_return = {
            "skip" : 0,
            "page" : 1,
            "page_size" : 1000,
            "count" : 9,
            "products" : [
                {
                    "product_name_fr": "potion magique de santé",
                    "code": "951753",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/sante.jpg",
                    "generic_name_fr":"ca requinque la life",
                    "nutrition_grade_fr": "a",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de bave de crapaud",
                    "code": "49123",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/degueu.jpg",
                    "nutrition_grade_fr": "d",
                    "generic_name_fr": "degueu",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de nutella",
                    "code": "9877",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/nutella-degueu.jpg",
                    "nutrition_grade_fr": "e",
                    "generic_name_fr": "encore plus mauvais que l'original",
                    "categories_hierarchy": [
                        "en:meats",
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion musclor",
                    "code": "47",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/musclor.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ahouuuuuuuuuu",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                        "em:meat-ultra",
                    ],
                },
                                {
                    "product_name_fr": "potion de bouse",
                    "code": "7",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/bouse.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "hhhmmmmm c'est delicieux",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "potion de grand mère",
                    "code": "52894631",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/old.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "périmé",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "jus de chaussettes",
                    "code": "4749763",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/shoes.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "pas fou en gout mais ca requinque",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "liquide inconnu",
                    "code": "9523",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/unknown.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ca se teste",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
                {
                    "product_name_fr": "jus de prune",
                    "code": "47433",
                    "image_url": "https://static.openfoodfacts.org/images/products/152/prune.jpg",
                    "nutrition_grade_fr": "a",
                    "generic_name_fr": "ca lave",
                    "categories_hierarchy": [
                        "en:magic-beverages",
                    ],
                },
            ]
        }
        mock_get_categories_from_api.return_value = {
            "count" : 13936,           
            "tags" : [
                {
                    "products": 30000,
                    "name": "Aliments et boissons à base de végétaux",
                    "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
                    "id": "en:plant-based-foods-and-beverages"
                },
                {
                    "id": "en:magic-beverages",
                    "url": "https://fr.openfoodfacts.org/categorie/boissons-magiques",
                    "products": 850,
                    "name": "Boissons magiques"
                },
                {
                    "products": 50,
                    "name": "Biscuits de druides",
                    "url": "https://fr.openfoodfacts.org/categorie/biscuits-de-druides",
                    "sameAs": [
                        "https://www.wikidata.org/wiki/Q40050"
                    ],
                    "id": "en:druids-cookies"
                },
            ]
        }

        mock_api_product.return_value = products_return

        # operation from dbinit --create commands
        self.db_init.clean_db()
        self.db_init.set_categories()
        self.db_init.set_products()

        # tests
        category_number = Category.objects.all().count()
        self.assertEqual(category_number, 1)

        product_number = Product.objects.all().count()
        self.assertEqual(product_number, 8)

        users = User.objects.all().exists()
        self.assertEqual(users, False)

        profiles = Profile.objects.all().exists()
        self.assertEqual(profiles, False)

        categories = Category.objects.all()
        categories_result = [
            "<Category: boissons magiques>",
        ]
        self.assertQuerysetEqual(categories, categories_result, ordered=False)

        products = Product.objects.all()
        products_result = [
            "<Product: potion magique de sante>",
            "<Product: potion de bave de crapaud>",
            "<Product: potion de nutella>",
            "<Product: potion musclor>",
            "<Product: potion de bouse>",
            "<Product: potion de grand mere>",
            "<Product: jus de chaussettes>",
            "<Product: liquide inconnu>",
        ]
        self.assertQuerysetEqual(products, products_result, ordered=False)