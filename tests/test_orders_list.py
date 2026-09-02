import requests
import allure
from urls import ORDERS_LIST_URL


@allure.feature("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(ORDERS_LIST_URL)

        assert response.status_code == 200
        assert "orders" in response.json()