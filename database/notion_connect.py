import datetime

import requests

from utils.process_created_time import process_created_time

# Конфигурация для подключения к Notion API
NOTION_TOKEN='secret_AbbSZWbyZO8zLqWHAL6WCK2nYRihGYD5kOCZMvUUAT5'
DATABASE_ID="1c8fa05ac45f80c499ecfef705bb0282"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


# Получить все записи из таблицы
def get_clean_rows(start_from: str = None, end_to: str = None, match_id: str = None):
    """
    Получает упрощённые записи из Notion и фильтрует по дате и ID.

    :param start_from: (str, формат 'YYYY-MM-DD') — фильтр: дата начала >=
    :param end_to: (str, формат 'YYYY-MM-DD') — фильтр: дата конца <=
    :param match_id: (str) — точный поиск по ID (например, 'BRN-0012')
    :return: List[dict]
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS)
    response.raise_for_status()
    raw_results = response.json().get("results", [])

    simplified = []
    for page in raw_results:
        props = page["properties"]
        item = {
            "id": props["User ID"]["title"][0]["text"]["content"] if props["User ID"]["title"] else "",
            "cost": props["Cost"]["number"],
            "kids": props["Kids"]["checkbox"],
            "pets": props["Pets"]["checkbox"],
            "kupel": props["Kupel"]["checkbox"],
            "shooting": props["Shooting"]["checkbox"],  # Новое поле Shooting
            "phone": props["Phone"]["phone_number"],
            "contact": props["Contact"]["rich_text"][0]["text"]["content"] if props["Contact"]["rich_text"] else "",
            "note": props["Note"]["rich_text"][0]["text"]["content"] if props["Note"]["rich_text"] else "",  # Новое поле Note
            "start_date": props["Start Date"]["date"]["start"],
            "end_date": props["End Date"]["date"]["start"],
            "payment_method": props["Payment method"]["select"]["name"] if props["Payment method"]["select"] else None
        }

        simplified.append(item)

    # 📅 Фильтрация по датам
    if start_from:
        simplified = [row for row in simplified if row["start_date"] >= start_from]
    if end_to:
        simplified = [row for row in simplified if row["end_date"] <= end_to]

    # 🔍 Фильтрация по ID
    if match_id:
        simplified = [row for row in simplified if row["id"] == match_id]

    return simplified


def add_row(data: dict):
    """
    Добавляет запись в таблицу Notion с обязательными полями и дефолтными значениями для необязательных полей.

    :param data: Данные для добавления в таблицу.
    :return: Ответ от API Notion.
    """
    # Обязательные поля
    required_fields = ["id", "phone", "start_date", "end_date"]

    # Проверка на наличие обязательных полей
    for field in required_fields:
        if field not in data:
            print(f"❌ Отсутствует обязательное поле: {field}")
            return None



    # Заполнение обязательных полей
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "User ID": {
                "title": [{
                    "text": {"content": data["id"]}
                }]
            },
            "Phone": {"phone_number": data["phone"]},
            "Start Date": {"date": {"start": data["start_date"]}},
            "End Date": {"date": {"start": data["end_date"]}},
            # Дополнительные поля (с дефолтными значениями)
            "Cost": {"number": data.get("cost", 0)},
            "Kids": {"checkbox": bool(data.get("kids", False))},
            "Pets": {"checkbox": bool(data.get("pet", False))},
            "Kupel": {"checkbox": bool(data.get("koupel", False))},
            "Shooting": {"checkbox": bool(data.get("shooting", False))},
            "Contact": {
                "rich_text": [{
                    "text": {"content": data.get("contact", "unknown")}
                }]
            },
            "Payment method": {
                "select": {"name": data.get("payment_method", "Waiting")}
            },
            "Num quests": {
                "select": {"name": str(data.get("num_quests", "1"))}  # По умолчанию "1"
            }
        }
    }

    # Отправка данных
    response = requests.post(url, headers=NOTION_HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# Обновить поле "Payment method" по ID (User ID)
def update_payment_method_by_id(user_id: str, new_method: str) -> bool:
    """
    Обновляет поле 'Payment method' для записи с указанным User ID.

    :param user_id: ID пользователя (значение поля 'User ID', а не Notion internal id)
    :param new_method: Новое значение для поля 'Payment method' (select)
    :return: True если успешно, False если запись не найдена
    """
    # 1. Найдём нужную страницу по User ID
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS)
    response.raise_for_status()
    results = response.json().get("results", [])

    page_id_to_update = None
    for page in results:
        title_data = page["properties"]["User ID"]["title"]
        title_text = title_data[0]["text"]["content"] if title_data else ""
        if title_text == user_id:
            page_id_to_update = page["id"]
            break

    if not page_id_to_update:
        print("❌ Строка с таким User ID не найдена.")
        return False

    # 2. Обновим поле 'Payment method'
    update_url = f"https://api.notion.com/v1/pages/{page_id_to_update}"
    payload = {
        "properties": {
            "Payment method": {
                "select": {"name": new_method}
            }
        }
    }

    update_response = requests.patch(update_url, headers=NOTION_HEADERS, json=payload)
    update_response.raise_for_status()

    print(f"✅ Строка с User ID '{user_id}' успешно обновлена: способ оплаты → {new_method}")
    return True

def update_payment_method_by_page_id(page_id: str, new_method: str) -> bool:
    """
    Обновляет поле 'Payment method' для записи с указанным Notion page ID.

    :param page_id: ID страницы Notion (внутренний ID страницы, например, "1cbfa05a-c45f-818c-8051-cf434ddf5996")
    :param new_method: Новое значение для поля 'Payment method' (select)
    :return: True если успешно, False если запись не найдена
    """
    # Структура запроса для обновления страницы
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Payment method": {
                "select": {"name": new_method}
            }
        }
    }

    try:
        # Отправляем запрос на обновление
        response = requests.patch(update_url, headers=NOTION_HEADERS, json=payload)
        response.raise_for_status()  # Проверка на ошибки HTTP

        print(f"✅ Строка с page_id '{page_id}' успешно обновлена: способ оплаты → {new_method}")
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        print("Ошибка в запросе:", response.text)  # Ответ от API с ошибкой
    except Exception as err:
        print(f"❌ Other error occurred: {err}")

    return False


def to_clean_rows(results):
    """
    Обрабатывает и упрощает данные для отображения, сортируя их по start_date.

    :param results: Ответ от Notion с данными.
    :return: Список упрощенных данных, отсортированных по start_date.
    """
    simplified = []
    for page in results:
        props = page["properties"]
        print(page["created_time"])
        item = {
            "id": props["User ID"]["title"][0]["text"]["content"] if props["User ID"]["title"] else "",
            "cost": props["Cost"]["number"],
            "kids": props["Kids"]["checkbox"],
            "pets": props["Pets"]["checkbox"],
            "kupel": props["Kupel"]["checkbox"],
            "phone": props["Phone"]["phone_number"],
            "contact": props["Contact"]["rich_text"][0]["text"]["content"] if props["Contact"]["rich_text"] else "",
            "note": props["Note"]["rich_text"][0]["text"]["content"] if props["Note"]["rich_text"] else "",
            "start_date": datetime.datetime.strptime(props["Start Date"]["date"]["start"], "%Y-%m-%d").date(),
            "end_date": datetime.datetime.strptime(props["End Date"]["date"]["start"], "%Y-%m-%d").date(),
            "payment_method": props["Payment method"]["select"]["name"] if props["Payment method"]["select"] else None,
            "created_time": process_created_time(page["created_time"])  # Преобразование времени создания
        }
        simplified.append(item)

    simplified.sort(key=lambda x: x["start_date"])

    return simplified


def get_pages_by_user_id(user_id: str):
    """
    Получает все страницы с указанным User ID.

    :param user_id: ID пользователя (значение поля 'User ID', а не Notion internal id)
    :return: Список обработанных данных страниц.
    """
    # 1. Получаем все страницы из базы данных
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS)
    response.raise_for_status()

    results = response.json().get("results", [])

    for i in results:
        print(i)

    # 2. Фильтруем страницы по User ID
    filtered_pages = [page for page in results if
                      page["properties"]["User ID"]["title"][0]["text"]["content"] == user_id]

    if not filtered_pages:
        print("❌ Строки с таким User ID не найдены.")
        return None

    # 3. Возвращаем обработанные данные
    return to_clean_rows(filtered_pages)
