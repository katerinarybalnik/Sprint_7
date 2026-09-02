import requests
import random
import string
import allure
from urls import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        payload = {
            "login": login,
            "password": "test_password",
            "firstName": "test_name"
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        try:
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        finally:
            login_response = requests.post(LOGIN_COURIER_URL, data={"login": login, "password": "test_password"})
            courier_id = login_response.json()["id"]
            requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_two_identical_couriers(self):
        login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))

        payload = {
            "login": login,
            "password": "test_password",
            "firstName": "test_name"
        }

        first_response = requests.post(CREATE_COURIER_URL, data=payload)
        second_response = requests.post(CREATE_COURIER_URL, data=payload)

        try:
            assert first_response.status_code == 201
            assert second_response.status_code == 409
            assert second_response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
        finally:
            login_response = requests.post(LOGIN_COURIER_URL, data={"login": login, "password": "test_password"})
            courier_id = login_response.json()["id"]
            requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")

    @allure.title("Нельзя создать курьера без логина")
    def test_create_courier_without_login(self):
        payload = {
            "password": "test_password",
            "firstName": "test_name"
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Нельзя создать курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {
            "login": "test_login_without_password",
            "firstName": "test_name"
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}