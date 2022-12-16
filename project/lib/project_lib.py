from django.utils import timezone

from lib.translate_table import translate_field_name
from notify.lib.notify_followers import notify_customer_followers, notify_project_followers
from ..forms import ProjectForm
from ..models import DailyReportPhoto, FavoriteProject


def save_new_project_or_none(request, customer):
    form = ProjectForm(data=request.POST)
    if form.is_valid():
        new_project = form.save(commit=False)
        new_project.customer = customer
        new_project.creator = request.user
        new_project.editor = request.user
        new_project.save()
        customer.editor = request.user
        customer.update_time = timezone.now()
        customer.save()
        return new_project
    return None


def send_owner_notify(request, updated_project):
    if request.user == updated_project.owner:
        return
    project_title = f'[專案]{updated_project.title}/{updated_project.type}'
    s = f'你已被{request.user}設定為 \n{project_title}\n 的負責人員。\n' \
        f'自動加入追蹤清單。' \
        f'連結：{updated_project.create_detail_link(request)}'
    FavoriteProject.objects.get_or_create(user=updated_project.owner, project=updated_project)
    updated_project.owner.send_line_notify(s)


def send_add_project_msg_to_followers(request, new_project):
    s = f"{request.user.nickname}建立新專案：\n" \
        f"({new_project.customer.name})[專案]{new_project.title}/{new_project.type}\n"
    notify_customer_followers(new_project.customer, s)


def send_change_message_to_followers(request, updated_form):
    updated_project = updated_form.instance
    ch_change_field = translate_field_name(updated_form.changed_data)

    s = f"{request.user.nickname} 更新了 \n" \
        f"[專案]{updated_project.title}/{updated_project.type}({updated_project.customer.name})\n" \
        f"更新欄位：{ch_change_field}"
    notify_project_followers(updated_project, s)

    if 'owner' in updated_form.changed_data:
        send_owner_notify(request, updated_project)


def send_add_report_message_to_followers(request, report):
    s = f"{request.user.nickname} 建立了紀錄: \n " \
        f"[{report.project.customer.name}]{report.project.title}/{report.project.type}\n" \
        f"---\n" \
        f"{report.note}\n" \
        f"---\n" \
        f"{report.project.create_detail_link(request)}"
    notify_project_followers(report.project, s)


def count_photos(report_id):
    photo_sets = DailyReportPhoto.objects.filter(report=report_id)
    if not len(photo_sets):
        return 0

    counter = 0
    for photo_set in photo_sets:
        for k in photo_set.__dict__.keys():
            if 'photo' in k and getattr(photo_set, k):
                counter += 1
    return counter


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
