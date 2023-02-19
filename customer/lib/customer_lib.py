from lib.translate_table import translate_field_name
from notify.lib.notify_followers import notify_customer_followers


def send_change_message_to_followers(request, updated_form):
    if not updated_form.changed_data:
        return

    updated_customer = updated_form.instance
    ch_change_field = translate_field_name(updated_form.changed_data)

    s = f"{request.user.nickname} 更新了 \n" \
        f"[客戶]{updated_customer.name}({updated_customer.status})\n" \
        f"更新欄位：{ch_change_field}"
    notify_customer_followers(updated_customer, s)


def get_page(request):
    try:
        return int(request.GET['page'])
    except Exception:
        return 1


def get_num_of_page(request):
    try:
        return int(request.GET['data_num'])
    except Exception:
        return 50


def get_cel(request):
    try:
        return request.GET['cel']
    except Exception:
        return None

