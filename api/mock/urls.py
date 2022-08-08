# Django imports
from django.urls import path
# Overlord-API imports
from api.mock import views

MOCK_PRODUCT = lambda product_id: f"api/digital/v1/product/{product_id}"

URLS = [
  path(
      MOCK_PRODUCT("4148762"),
      views.product,
      name="List Mock Product Data"
  ),
]

"""
This is the real endpoint that we are mocking:
  https://www.bloomingdales.com/xapi/digital/v1/product/4148762?
  clientId=PROS&_regionCode=US&currencyCode=USD&_shoppingMode=SITE&size=small&_customerState=GUEST
"""
