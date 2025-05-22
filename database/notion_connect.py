import datetime
from typing import List, Dict, Optional

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

def get_bookings_ending_on(end_on: str,
                           payment_methods: List[str] = None,
                           status: List[str] = None) -> list[dict]:
    """
    Вернёт упрощённые строки, у которых End Date == end_on (YYYY-MM-DD).
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    body = {
        "filter": {
            "property": "End Date",
            "date": {
                "equals": end_on
            }
        }
    }
    resp = requests.post(url, headers=NOTION_HEADERS, json=body)
    resp.raise_for_status()
    raw = resp.json().get("results", [])

    simplified = []
    for page in raw:
        props = page["properties"]
        item = {
            "id": props["User ID"]["title"][0]["text"]["content"] if props["User ID"]["title"] else "",
            "cost": props["Cost"]["number"],
            "kids": props["Kids"]["checkbox"],
            "pets": props["Pets"]["checkbox"],
            "koupel": props["Kupel"]["checkbox"],
            "phone": props["Phone"]["phone_number"],
            "contact": props["Contact"]["rich_text"][0]["text"]["content"]
            if props["Contact"]["rich_text"] else "",
            "note": props["Note"]["rich_text"][0]["text"]["content"]
            if props["Note"]["rich_text"] else "",
            "start_date": props["Start Date"]["date"]["start"],
            "end_date": props["End Date"]["date"]["start"],
            "payment": props["Payment method"]["select"]["name"]
                if props["Payment method"]["select"] else None,
            "status": props["Booking status"]["select"]["name"]
                if props["Booking status"]["select"] else None,
            "num_quests": props["Num quests"]["select"]["name"]
                if props["Num quests"]["select"] else None,
            "uniq_id": props['ID']["unique_id"]["number"]
        }
        simplified.append(item)

        if payment_methods:
            simplified = [r for r in simplified if r["payment"] in payment_methods]
        if status:
            simplified = [r for r in simplified if r["status"] in status]

    return simplified


def get_bookings_start_on(start_on: str,
                          payment_methods: List[str] = None,
                          status: List[str] = None) -> list[dict]:
    """
    Вернёт упрощённые строки, у которых End Date == end_on (YYYY-MM-DD).
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    body = {
        "filter": {
            "property": "Start Date",
            "date": {
                "equals": start_on
            }
        }
    }
    resp = requests.post(url, headers=NOTION_HEADERS, json=body)
    resp.raise_for_status()
    raw = resp.json().get("results", [])

    simplified = []
    for page in raw:
        props = page["properties"]
        item = {
            "id": props["User ID"]["title"][0]["text"]["content"] if props["User ID"]["title"] else "",
            "cost": props["Cost"]["number"],
            "kids": props["Kids"]["checkbox"],
            "pets": props["Pets"]["checkbox"],
            "koupel": props["Kupel"]["checkbox"],
            "phone": props["Phone"]["phone_number"],
            "contact": props["Contact"]["rich_text"][0]["text"]["content"]
            if props["Contact"]["rich_text"] else "",
            "note": props["Note"]["rich_text"][0]["text"]["content"]
            if props["Note"]["rich_text"] else "",
            "start_date": props["Start Date"]["date"]["start"],
            "end_date": props["End Date"]["date"]["start"],
            "payment": props["Payment method"]["select"]["name"]
                        if props["Payment method"]["select"] else None,
            "status": props["Booking status"]["select"]["name"]
                        if props["Booking status"]["select"] else None,
            "num_quests": props["Num quests"]["select"]["name"]
                if props["Num quests"]["select"] else None,
            "uniq_id": props['ID']["unique_id"]["number"],

        }
        simplified.append(item)

        if payment_methods:
            simplified = [r for r in simplified if r["payment"] in payment_methods]
        if status:
            simplified = [r for r in simplified if r["status"] in status]


    return simplified

# Получить все записи из таблицы
def get_clean_rows(start_from: str = None,
                   end_to: str = None,
                   match_id: str = None,
                   payment_methods: List[str] = None,
                   status: List[str] = None,) -> List[Dict]:
    """
    Получает упрощённые записи из Notion и фильтрует по дате, ID и списку способов оплаты.

    :param start_from: (str, формат 'YYYY-MM-DD') — фильтр: дата начала >=
    :param end_to: (str, формат 'YYYY-MM-DD') — фильтр: дата конца <=
    :param match_id: (str) — точный поиск по ID (например, 'BRN-0012')
    :payment_methods (list) - фильтрация по методу оплаты
    :return: List[dict]
    """

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    resp = requests.post(url, headers=NOTION_HEADERS)
    resp.raise_for_status()
    raw = resp.json().get("results", [])

    simplified = []
    for page in raw:
        props = page["properties"]
        item = {
            "id": props["User ID"]["title"][0]["text"]["content"] if props["User ID"]["title"] else "",
            "cost": props["Cost"]["number"],
            "kids": props["Kids"]["checkbox"],
            "pets": props["Pets"]["checkbox"],
            "koupel": props["Kupel"]["checkbox"],
            "phone": props["Phone"]["phone_number"],
            "contact": props["Contact"]["rich_text"][0]["text"]["content"]
                       if props["Contact"]["rich_text"] else "",
            "note": props["Note"]["rich_text"][0]["text"]["content"]
                    if props["Note"]["rich_text"] else "",
            "start_date": props["Start Date"]["date"]["start"],
            "end_date": props["End Date"]["date"]["start"],
            "payment": props["Payment method"]["select"]["name"]
                       if props["Payment method"]["select"] else None,
            "status": props["Booking status"]["select"]["name"]
                        if props["Booking status"]["select"] else None,
            "num_quests": props["Num quests"]["select"]["name"]
                       if props["Num quests"]["select"] else None,
            "uniq_id": props['ID']["unique_id"]["number"],
        }
        simplified.append(item)

    if start_from:
        simplified = [r for r in simplified if r["start_date"] >= start_from]
    if end_to:
        simplified = [r for r in simplified if r["end_date"] <= end_to]
    if match_id:
        simplified = [r for r in simplified if r["id"] == match_id]
    if payment_methods:
        simplified = [r for r in simplified if r["payment"] in payment_methods]
    if status:
        simplified = [r for r in simplified if r["status"] in status]

    return simplified

def check_payment_status(notion_page_id: str) -> bool:
    """
    Возвращает False, если в свойстве Payment method:
      - нет значения,
      - или стоит "Waiting" / "Payment failed".
    В остальных случаях — True.
    """
    url = f"https://api.notion.com/v1/pages/{notion_page_id}"
    resp = requests.get(url, headers=NOTION_HEADERS)
    resp.raise_for_status()

    props = resp.json().get("properties", {})
    pm_select = props.get("Payment method", {}).get("select")

    # Нет select или в чёрном списке — False
    if pm_select is None or pm_select.get("name") in ("Waiting", "Payment failed"):
        return False
    return True

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
            "Kids": {"checkbox": bool(data.get("kids", False))},
            "Pets": {"checkbox": bool(data.get("pet", False))},
            "Kupel": {"checkbox": bool(data.get("koupel", False))},
            "Contact": {
                "rich_text": [{
                    "text": {"content": data.get("contact", "unknown")}
                }]
            },

            "Num quests": {
                "select": {"name": str(data.get("num_quests"))}  # По умолчанию "1"
            }
        }
    }
    if data.get("cost"):
        payload['properties']['Cost'] = {"number": data.get("cost", 0)}
    if data.get("payment"):
        payload['properties']['Payment method'] = {"select": {"name": data.get("payment", "Waiting")}}
    if data.get("verify"):
        payload['properties']['Booking status'] = {"select": {"name": data.get("verify")}}


    # Отправка данных
    response = requests.post(url, headers=NOTION_HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


# Обновить поле "Payment method" по ID (User ID)
def update_payment_method_by_user_id(user_id: str, new_method: str) -> bool:
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


def update_status_by_uniq_id(uniq_id: str, new_status: str) -> bool:
    """
    Обновляет поле 'Payment method' для записи, где свойство ID (Unique ID) равно uniq_id.

    :param uniq_id: значение поля 'ID' (тип Unique ID в базе)
    :param new_status: новое значение для поля 'Payment method' (select)
    :return: True если запись найдена и обновлена, False если не найдена
    """
    # 1. Ищем страницу по полю ID (Unique ID)
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    query_payload = {
        "filter": {
            "property": "ID",
            "unique_id": {
                "equals": uniq_id
            }
        }
    }
    response = requests.post(query_url, headers=NOTION_HEADERS, json=query_payload)
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        print(f"❌ Строка с ID = {uniq_id} не найдена.")
        return False

    page_id = results[0]["id"]

    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    update_payload = {
        "properties": {
            "Booking status": {
                "select": {"name": new_status}
            }
        }
    }
    update_resp = requests.patch(update_url, headers=NOTION_HEADERS, json=update_payload)
    update_resp.raise_for_status()

    print(f"✅ Строка с ID = {uniq_id} успешно обновлена: способ оплаты → {new_status}")
    return True


def update_verification_by_page_id(page_id: str, new_status: str) -> bool:
    """
    Обновляет поле 'Verification' (select) для записи с указанным Notion page ID.

    :param page_id: внутренний ID страницы в Notion, например "1cbfa05a-c45f-818c-8051-cf434ddf5996"
    :param new_status: Новое значение для поля 'Verification' (имя опции в select)
    :return: True, если запрос прошел успешно; иначе — False
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Booking status": {
                "select": { "name": new_status }
            }
        }
    }

    try:
        response = requests.patch(url, headers=NOTION_HEADERS, json=payload)
        response.raise_for_status()
        print(f"✅ Поле Verification на странице {page_id} установлено в '{new_status}'")
        return True
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error: {http_err}")
        print("→ Ответ API:", response.text)
    except Exception as err:
        print(f"❌ Другая ошибка: {err}")

    return False

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
            "payment": props["Payment method"]["select"]["name"] if props["Payment method"]["select"] else None,
            "created_time": process_created_time(page["created_time"]),
            "uniq_id": props['ID']["unique_id"]["number"]
        }

        simplified.append(item)

    simplified.sort(key=lambda x: x["start_date"])

    return simplified


def get_pages_by_user_id(
    user_id: str,
    allowed_status: Optional[List[str]] = None
):
    """
    Получает все страницы с указанным User ID, опционально фильтрует
    их по списку способов оплаты и сортирует по Start Date от нового к старому.

    :param user_id: ID пользователя (значение поля 'User ID', а не Notion internal id)
    :param allowed_status: Список названий вариантов в поле 'Payment method'.
                            Если не указано — фильтрация по оплате не выполняется.
    :return: Список обработанных данных страниц или None, если ничего не найдено.
    """
    # 1. Получаем все страницы из базы данных
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=NOTION_HEADERS)
    response.raise_for_status()
    results = response.json().get("results", [])

    # 2. Фильтруем по User ID
    filtered = []
    for page in results:
        titles = page["properties"].get("User ID", {}).get("title", [])
        if titles and titles[0]["text"]["content"] == user_id:
            filtered.append(page)

    # 3. Фильтруем по способу оплаты, если передан список
    if allowed_status:
        filtered = [
            page for page in filtered
            if (pm := page["properties"]
                         .get("Booking status", {})
                         .get("select"))
               and pm.get("name") in allowed_status
        ]

    if not filtered:
        print(
            "❌ Строки с таким User ID"
            + (f" и статусом {allowed_status}" if allowed_status else "")
            + " не найдены."
        )
        return None

    # 4. Сортируем по Start Date от нового к старому
    def _start_date(page):
        return page["properties"] \
                   .get("Start Date", {}) \
                   .get("date", {}) \
                   .get("start", "")

    filtered.sort(key=_start_date, reverse=True)

    # 5. Преобразуем и возвращаем
    return to_clean_rows(filtered)

