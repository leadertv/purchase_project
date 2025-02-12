
# Purchase Project - розничные сети

**Purchase Project** – это backend-приложение для автоматизации закупок в розничной сети. Проект реализован на Python с использованием Django и Django REST Framework.

## О дипломном проекте

Данный проект предоставляет REST API для следующих функций:
- **Авторизация и регистрация** пользователей (как покупателей, так и поставщиков).
- **Получение списка товаров** и **спецификации по отдельному товару**.
- **Работа с корзиной**: добавление и удаление товаров.
- **Добавление/удаление адреса доставки** (через управление контактами пользователя).
- **Подтверждение заказа** с отправкой email уведомлений клиенту и администратору.
- **Получение списка заказов** и **деталей заказа**.
- **Редактирование статуса заказа** – в базовой версии статусы описаны в модели, но нужна доработка API.
- **Импорт товаров** из YAML-файлов.
- *(Гипотетически)* API для поставщиков: обновление прайсов, переключение приёма заказов и получение заказов по прайсу.

## Требования
- VDS сервер на базе Ubuntu 24.
- Python версии 3.12 а таже установленный pip и venv для создания виртуального окружения.

## Клонирование репозитория

Зайдите по пути (опционально):
```bash
cd /home
mkdir purchasedir
cd purchasedir
```

Клонируйте проект с GitHub:

```bash
git clone git@github.com:leadertv/purchase_project.git
```

Создайте виртуальное окружение VENV перейдя в папку purchase_project:

```bash
cd purchase_project
python -m venv venv
source venv/bin/activate
```
Можно это сделать внутри screen, тут по желанию...


## Установка зависимостей

В корневой директории проекта установите зависимости:

```bash
pip install -r requirements.txt
```

*Пример файла `requirements.txt`:*

```
Django>=3.2,<4.0
djangorestframework>=3.12.4
python-dotenv>=0.15.0
PyYAML>=5.3.1
```

## Настройка окружения (.env)

Создайте файл `.env` в корневой директории проекта (рядом с файлом `manage.py`) и настройте его. Пример содержимого:

```env
DEBUG=True
ALLOWED_HOSTS=<IP Вашего сервера> localhost 127.0.0.1
DEFAULT_FROM_EMAIL=noreply@example.com
ADMIN_EMAIL=admin@example.com
SERVER_DOMAIN=<IP Вашего сервера>
```

Эти переменные используются для:
- Определения режима отладки (DEBUG)
- Настройки списка разрешённых хостов (ALLOWED_HOSTS)
- Конфигурации email отправителя (DEFAULT_FROM_EMAIL) и адреса администратора (ADMIN_EMAIL)
- Задания доменного имени сервера (SERVER_DOMAIN), по которому будет доступен API

## Применение миграций

Выполните миграции для создания базы данных:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Импорт образца с товарами

Можно импортировать YAML файл находясь в корне проекта, для проверки и тестов товаров

```bash
python manage.py import_products data/price01.yaml
```

## Создание суперпользователя

Для доступа к административной панели и выполнения административных задач создайте суперпользователя:

```bash
python manage.py createsuperuser
```

## Запуск сервера

Чтобы запустить сервер и сделать его доступным извне (на 0.0.0.0:8000), выполните:

```bash
python manage.py runserver 0.0.0.0:8000
```

Сервер будет доступен по адресу:  
`http://<IP ВАШЕГО VDS>:8000/`

## Тестирование API

Для тестирования API можно использовать инструменты вроде VS Code REST Client. Примеры запросов для тестирования доступны в файле `api-tests.http`.

## Дальнейшая доработка

Проект разработан как базовый прототип. Возможны следующие доработки:
- Реализация полноценного API для поставщиков (обновление прайсов, переключение приёма заказов, получение заказов по прайсу).
- Расширение функционала управления заказами, в том числе редактирование статусов заказа.
- Улучшение валидации входных данных и обработка ошибок.
- Улучшение работы с задачами и т.д. используя Celery.
- Настройка продакшн-среды (использование WSGI/ASGI серверов, настройка HTTPS и т.д.).
- Докеризация проекта.

## Контакты

Почта: leadertv@mail.ru

---

Это руководство поможет развернуть проект, протестировать API и заложить основу для дальнейшей доработки.
