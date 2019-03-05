from django.urls import path

from . import views

urlpatterns = [
    path('', views.food_index, name='food_index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('detail', views.detail, name='detail'),
    path('add', views.add, name='add'),
    path('buy/<int:food_id>', views.buy, name='buy'),
    path('minus/<int:food_id>', views.minus, name='minus'),
    path('food_detail/<int:food_id>',views.food_detail,name="food_detail"),
    path('food_modify/<int:food_id>',views.food_modify,name="food_modify"),
    path('food_delete/<int:food_id>',views.food_delete,name="food_delete"),
    path('pre_order',views.pre_order,name="pre_order"),
    path('pay/<int:food_id>', views.pay, name='pay'),
    path('plus/<int:food_id>', views.plus, name='plus'),
    path('order',views.order,name="order"),
    path('complete/<int:food_id>',views.complete,name="complete"),
    path('sell_order',views.sell_order,name="sell_order"),
    path('user_detail', views.user_detail, name='user_detail'),
    path('user_modify', views.user_modify, name='user_modify')

]