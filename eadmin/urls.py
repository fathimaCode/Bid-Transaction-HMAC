from django.urls import path
from .import views

urlpatterns = [
    path("",views.index, name="index"),
    path("login/",views.login, name="login"),
    path("register/",views.register, name="register"),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("bid_details/",views.bid_details, name="bid_details"),
    path("viewBidDetails/<int:tender_id>/",views.getBidDetails, name="viewBidDetails"),
    path("newCotation/",views.newCotation, name="newCotation"),
]