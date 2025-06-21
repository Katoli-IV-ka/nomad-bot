from database.notion_connect import check_prepayment_status, update_payment_method_by_page_id, \
    update_verification_by_page_id


def check_prepayment(notion_page_id):
    if not check_prepayment_status(notion_page_id):
        update_verification_by_page_id(page_id=notion_page_id, new_status="Payment overdue")


def check_full_payment(notion_page_id):
    if not check_prepayment_status(notion_page_id):
        update_verification_by_page_id(page_id=notion_page_id, new_status="Payment overdue")