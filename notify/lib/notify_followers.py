from customer.models import FavoriteCustomer
from project.models import FavoriteProject
from threading import Thread


def notify_project_followers(project, message):
    project_followers = FavoriteProject.objects.filter(project=project)
    [Thread(target=user.user.send_line_notify, args=(message,)).start() for i, user in enumerate(project_followers)]


def notify_customer_followers(customer, message):
    customer_followers = FavoriteCustomer.objects.filter(customer=customer)
    [Thread(target=user.user.send_line_notify, args=(message,)).start() for i, user in enumerate(customer_followers)]
