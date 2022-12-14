from customer.models import FavoriteCustomer
from project.models import FavoriteProject


def notify_project_followers(project, message):
    project_followers = FavoriteProject.objects.filter(project=project)
    [user.user.send_line_notify(message)for user in project_followers]


def notify_customer_followers(customer, message):
    customer_followers = FavoriteCustomer.objects.filter(customer=customer)
    [user.user.send_line_notify(message)for user in customer_followers]
