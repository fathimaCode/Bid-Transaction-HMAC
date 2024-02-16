from django.urls import path
from .import views

urlpatterns = [
    path("",views.index, name="index"),
    
    path("login/",views.login, name="login"),
    path("register/",views.register, name="register"),
    path("authority_newTender/",views.authority_newTender, name="authority_newTender"),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("bid_details/",views.bid_details, name="bid_details"),
    path("viewBidDetails/<int:tender_id>/",views.getBidDetails, name="viewBidDetails"),
    path("newCotation/",views.newCotation, name="newCotation"),
    path("viewTenderList/",views.viewTenderList, name="viewTenderList"),
    path("deleteTender/<int:tender_id>/",views.deleteTender, name="deleteTender"),
    path("adminGetBidInfo/<int:tender_id>/",views.adminGetBidInfo, name="adminGetBidInfo"),
    path("closeTender/<int:tender_id>/",views.closeTender, name="closeTender"),
    path("announceWinner/<int:blockid>/",views.announceWinner, name="announceWinner"),
]