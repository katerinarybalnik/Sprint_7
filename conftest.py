import pytest
import requests
import random
import string
import allure

from urls import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL


@allure.step("Создать курьера")
def create_courier(payload):
    return requests.post(CREATE_COURIER_URL, data=payload)


@allure.step("Авторизовать курьера")
def login_courier(payload):
    return requests.post(LOGIN_COURIER_URL, data=payload)


@allure.step("Удалить курьера")
def delete_courier(courier_id):
    return requests.delete(f"{DELETE_COURIER_URL}/{courier_id}")


@pytest.fixture
def create_and_delete_courier():
    login = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    payload = {"login": login, "password": "test_password", "firstName": "test_name"}

    response = create_courier(payload)

    yield login, response

    login_response = login_courier({"login": login, "password": "test_password"})
    courier_id = login_response.json()["id"]
    delete_courier(courier_id)