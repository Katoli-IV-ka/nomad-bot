from database.notion_connect import check_payment_status, update_payment_method_by_page_id, \
    update_verification_by_page_id


def check_payment(notion_page_id):
    if not check_payment_status(notion_page_id):
        update_verification_by_page_id(page_id=notion_page_id, new_status="Payment overdue")