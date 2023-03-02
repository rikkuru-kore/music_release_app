from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('search',views.search,name='search'),
    path('tab_maintenance/',views.tab_maintenance,name='tab_maintenance'),
    path('music_maintenance/',views.music_maintenance,name='music_maintenance'),
    path('item_create/<int:division>/',views.item_create,name='item_create'),
    path('item_edit/<int:id>/<int:division>/',views.item_edit,name='item_edit'),
    path('item_delete/<int:id>/',views.item_delete,name='item_delete'),
    path('detail_item/<int:id>/',views.detail_item,name='detail_item'),
    path('<int:id>/input_email/',views.input_email,name='input_email'),
    path('pay/success/',views.pay_success,name='pay_success'),
    path('pay/cancel/',views.pay_cancel,name='pay_cancel'),
    path('create_checkout_session/<int:order_id>/',views.create_checkout_session,name='create_checkout_session'),
]
