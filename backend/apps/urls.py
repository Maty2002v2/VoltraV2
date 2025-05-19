from django.urls import path

from .division.views import DivisionDetailView, DivisionListView, DivisionBuyingGroupLinkView
from .files.views import FileDetailView, FileDownloadView, FileListView, UserDocumentsView, DownloadDocumentView
from .users.views import (
    ChangePasswordView, ResetPasswordView,
    ValidatePasswordView, ChangeHistoryViewSet,
    PointViewSet, DivisionViewSet, ContactDataViewSet)
from .points.views import PointDetailView, PointListView, TagListView, ExportUserCosts, PPESearchViewSet

urlpatterns = [
    path('divisions/<int:pk>/', DivisionDetailView.as_view()),
    path('divisions/', DivisionListView.as_view()),
    path('divisions/link/', DivisionBuyingGroupLinkView.as_view()),

    #do ogólnych dokumentów
    path('files/<int:pk>/', FileDetailView.as_view()),
    path('files/', FileListView.as_view()),
    path('files/download/<str:directory>/<str:filename>/', FileDownloadView.as_view(), name='file_download'),

    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password/validate/', ValidatePasswordView.as_view(), name='validate_hash'),
    path('reset_password/<str:user_hash>/', ChangePasswordView.as_view(), name='change_password'),

    path('points/<int:pk>/', PointDetailView.as_view()),
    path('points/', PointListView.as_view(), name='point'),
    path('points/report/', ExportUserCosts.as_view(), name='export_usercosts'),

    path('tags/', TagListView.as_view(), name='tag'),

    # do prywatnych dokumentów usera
    path('documents/', UserDocumentsView.as_view(), name='user_documents'),
    path('documents/<int:document_id>/download/', DownloadDocumentView.as_view(), name='download_document'),

    ###### V2  tu dodam nowe endpointy
    path('user/change-history/', ChangeHistoryViewSet.as_view({'get': 'list'}),
         name='change-history-list'), # historia zmian danych użytkownika
    path('user/change-history/<int:pk>/',
         ChangeHistoryViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='change-history-detail'),

    path("user/points/", PointViewSet.as_view({"get": "list"})), # pobieranie danych o liście punktów, pojedynczym punkcie, update danych
    path("user/point/<int:pk>/", PointViewSet.as_view({"get": "retrieve", "patch": "update"})),

    path("points/search/", PPESearchViewSet.as_view({"post": "create"})), # Wyszukiwarka punktów
    path("points/search/export_excel/", PPESearchViewSet.as_view({"post": "export_excel"})), # export do excela

    path("user/divisions/", DivisionViewSet.as_view({"get": "list"})), # pobieranie danych o liście division, pojedynczym division, update
    path("user/division/<int:pk>/", DivisionViewSet.as_view({"get": "retrieve", "patch": "update"})),

    path('user/contact-data/', ContactDataViewSet.as_view({'get': 'list'}), name='contact-data-list'), # pobieranie danych usera i ich update
    path('user/contact-data/<int:pk>/',
         ContactDataViewSet.as_view({'patch': 'update'}),
         name='contact-data-detail'),



]

#OKEYCRM APIKEY TEST: 9ebd0453a8aba6d8d2f73a084a94f4a87477c306
