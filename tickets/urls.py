from rest_framework import routers
from .views import TicketsViewsSet


router = routers.SimpleRouter()
router.register(r'', TicketsViewsSet)
urlpatterns = router.urls
