import requests
import allure
from helpers import register_new_courier_and_return_login_password
from urls import LOGIN_COURIER_URL, DELETE_COURIER_URL


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self):
        login_pass = register_new_courier_and_return_login_password()

        payload = {
            "login": login_pass[0],
            "password": login_pass[1]
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 200
        assert "id" in response.json()

        courier_id = response.json()["id"]
        requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")

    @allure.title("Нельзя авторизоваться без логина")
    def test_login_courier_without_login(self):
        payload = {
            "password": "test_password"
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}

    @allure.title("Нельзя авторизоваться без пароля")
    def test_login_courier_without_password(self):
        payload = {
            "login": "test_login"
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 400

    @allure.title("Нельзя авторизоваться с неправильным логином")
    def test_login_courier_with_wrong_login(self):
        payload = {
            "login": "nonexistent_login_123456789",
            "password": "test_password"
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}

    @allure.title("Нельзя авторизоваться с неправильным паролем")
    def test_login_courier_with_wrong_password(self):
        login_pass = register_new_courier_and_return_login_password()

        payload = {
            "login": login_pass[0],
            "password": "wrong_password"
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}

        login_response = requests.post(LOGIN_COURIER_URL, data={"login": login_pass[0], "password": login_pass[1]})
        courier_id = login_response.json()["id"]
        requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")

    @allure.title("Нельзя авторизоваться под несуществующим курьером")
    def test_login_nonexistent_courier(self):
        payload = {
            "login": "nonexistent_courier_987654321",
            "password": "nonexistent_password"
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}