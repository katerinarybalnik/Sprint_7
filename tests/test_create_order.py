import pytest
import requests
import allure
from urls import CREATE_ORDER_URL
from data import ORDER_DATA, ORDER_COLORS

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными цветами самоката")
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_create_order_with_different_colors(self, color):
        payload = ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(CREATE_ORDER_URL, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()


    @allure.title("Создание заказа без указания цвета")
    def test_create_order_without_color(self):
        payload = ORDER_DATA.copy()

        response = requests.post(CREATE_ORDER_URL, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()