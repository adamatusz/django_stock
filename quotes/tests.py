from django.test import TestCase
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Stock


User = get_user_model() # importujemy model uzytkownika

# Create your tests here.


@pytest.fixture
def user():
    user_a =User.objects.create_user(
        username='adam',
        email='adam@gmail.com',
        password='coderslab'
    )
    return user_a


@pytest.fixture
def stock():
    user = User.objects.create_user(
        username='adam',
        email='adam@gmail.com',
        password='coderslab'
    )
    Stock.objects.create(user=user, ticker='amzn')


def test_home_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    response = client.get(reverse('home'))
    # print(response.content)
    assert response.status_code == 200


def test_about_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    response = client.get(reverse('about'))
    print(response.content)
    assert response.status_code == 200


def test_login_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    response = client.get(reverse('login'))
    print(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    client.login(username='adam',
                 password='coderslab')
    response = client.get(reverse('home'))
    assert response.status_code == 200


def test_signup_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    response = client.get(reverse('signup'))
    print(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_signup_view(client):  # klient przeglądarka podawany domyślnie przez pytest
    client.login(username='adam',
                 password='coderslab')
    response = client.get(reverse('home'))
    assert response.status_code == 200


def test_add_stock_view_with_not_logged_user(client):
    response = client.get(reverse('add_stock'))
    assert response.status_code == 302  # oczekujemy przekierowania na @loginrequire


@pytest.mark.django_db
def test_add_stock_view_with_logged_user(client, user):
    client.login(username='adam',
                 password='coderslab')
    response = client.get(reverse('add_stock'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_stock(stock):
    stocks = Stock.objects.all()
    assert len(stocks) == 1
    assert stocks.first().ticker == 'amzn'  # bardziej testujemy Django


@pytest.mark.django_db
def test_add_stock_with_not_logged_user(client, user):
    payload = {"ticker": 'twtr'}
    post_response = client.post(reverse('add_stock'), payload, follow=True)
    assert post_response.status_code == 200
    assert b'input type="submit" value="Log In"' in post_response.content


@pytest.mark.django_db
def test_add_stock_with_logged_user(client, user):
    client.login(username='adam',
                 password='coderslab')
    payload = {"ticker": 'twtr'}
    post_response = client.post(reverse('add_stock'), payload, follow=True)
    print(dir(post_response))
    assert post_response.status_code == 200


def test_delete_stock_view_with_not_logged_user(client):
    response = client.get(reverse('delete_stock'))
    assert response.status_code == 302  # oczekujemy przekierowania na @loginrequire


@pytest.mark.django_db
def test_delete_stock_view_with_logged_user(client, user):
    client.login(username='adam',
                 password='coderslab')
    response = client.get(reverse('delete_stock'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_stock(stock):
    stocks = Stock.objects.all()
    assert len(stocks) == 1
    assert stocks.first().ticker == 'amzn'  # bardziej testujemy Django

