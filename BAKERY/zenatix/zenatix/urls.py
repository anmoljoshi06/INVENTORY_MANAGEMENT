"""zenatix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from bakery import views 
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(title="BAKERY APP",
        default_version='v1',
        description="Welcome to the world of Jaseci",
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'), 


    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),                    #used to login into the system and generating token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path("add/ingredient",views.ADD_INGREDIENT_VIEW.as_view()),                                 # api to add ingredients and their details
    path("put/edititem/<str:it>/<int:quant>/<int:price>",views.MANAGE_INVENTORY.as_view()),     # api to edit item details (for admin only)
    path("delete/edititem/<str:it>",views.DELETE_INGREDIENT.as_view()),                         # api to delete an ingredient from bakery
    path("add/bakeryitem",views.BAKERYITEM_ADD_VIEW.as_view()),                                 # api to add bakery items and their details
    path("create/recipe",views.BAKERYITEM_CREATE_VIEW.as_view()),                               # api to create the bakery items from raw ingredients
    path("get/itemdetail/<str:b_item>",views.BAKERYITEM_DETAILS_VIEW.as_view()),                # Get all the details of a particular bakery item 
    path("getall/itemdetails",views.ALL_BAKERYITEM_DETAILS_VIEW.as_view()),                     # Get details of all the Bakery Items
    path("register",views.create_user_view.as_view()),                                          # api to register a new user 
    path("get/menu",views.get_user_menu.as_view()),                                             # get all the items available in bakery as menu for customers
    path("post/order",views.user_order_view.as_view()),                                         # api to post the order for customers
    path("get/orderhistory",views.order_history.as_view()),                                     # api to get the order details history of a particular user 
    path("get/bestsellinitem",views.most_sellling_item.as_view()),                              # api to find best selling item so far from all the orders placed
    path("put/discount/<str:item_name>/<int:dis>",views.ADD_DISCOUNT.as_view())                 # api to add discount to a particular bakery item. 
]
