from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Count,Sum
from django.core import serializers

# Create your views here.



class ADD_INGREDIENT_VIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):   #to get lis of all ingredients
        snippets = ingredients.objects.all()
        serializer = ingredients_serializer(snippets, many=True)
        print("HERE",list(serializer.data))
        return Response(serializer.data)

    def post(self, request, format=None):     # to add a new ingredient
        serializer = ingredients_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MANAGE_INVENTORY(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,it,quant,price):
        if request.user.is_superuser:
            try:
                ingredients.objects.filter(item=it).update(price_per_unit=price)
                q = ingredients.objects.get(item=it).quantity_added
                ingredients.objects.filter(item=it).update(quantity_added=q+quant)
                return(Response({"Status":"edited details for "+str(it)},status=status.HTTP_200_OK))
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))
        else:
            return(Response({"Alert":"Not Allowed"},status=status.HTTP_401_UNAUTHORIZED))       
    
class DELETE_INGREDIENT(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,it):
        if request.user.is_superuser:
            try:
                ingredients.objects.filter(item=it).delete()
                return(Response({"status":"Item "+str(it)+" deleted"},status=status.HTTP_200_OK))
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        else:            
            return(Response({"Alert":"Not Allowed"},status=status.HTTP_401_UNAUTHORIZED))

class BAKERYITEM_ADD_VIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):   #to get lis of all Bakery items
        snippets = Bakery_Item_Names.objects.all()
        serializer = Bakery_Item_Names_serializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):     # to add a new Bakery items
        serializer = Bakery_Item_Names_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BAKERYITEM_CREATE_VIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):   #to get lis of all Bakery items
        snippets = Bakery_item_recipe.objects.distinct()
        serializer = Bakery_item_recipe_serializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request,format=None):     # to add a new Bakery items
        serializer = Bakery_item_recipe_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BAKERYITEM_DETAILS_VIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,b_item ,format=None):
        if request.user.is_superuser:  
            final = {}
            sn = Bakery_Item_Names.objects.get(bakery_item=b_item)
            snippets = Bakery_item_recipe.objects.filter(bakery_item=sn)
            serializer = Bakery_item_detail_serializer(snippets, many=True)
            final[b_item] = [dict(s) for s in list(serializer.data)]
            final["selling_price"]=sn.price
            final["cost_price"]=sn.cost_price
            return Response(final)
        else:
            return(Response({"Alert":"Not Allowed"},status=status.HTTP_401_UNAUTHORIZED))


class ALL_BAKERYITEM_DETAILS_VIEW(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,format=None):  
        all_items = Bakery_Item_Names.objects.all()
        final = {}
        for i in all_items:
            snippets = Bakery_item_recipe.objects.filter(bakery_item=i.id)
            serializer = Bakery_item_detail_serializer(snippets, many=True)
            final[i.bakery_item] = [[dict(s) for s in list(serializer.data)]]
            final[i.bakery_item].append([{"selling_price":i.price,"cost_price":i.cost_price}])
        return Response(final,status=status.HTTP_200_OK)


class create_user_view(APIView):
    def post(self,request):
        if request.method=="POST":
            try:
                name = request.data["username"]
                pwd = request.data["password"]
                email = request.data["email"]
            except Exception as e:
                return(Response({"status":"Malformed Request, "+str(e)},status=status.HTTP_400_BAD_REQUEST))    
            try:                            
                user = User.objects.create_superuser(username=name,email=email,password=pwd)
                user.is_staff = True 
                user.is_superuser=False
                user.save()
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))    
            return(Response({"status":"created non-admin user"},status=status.HTTP_200_OK))   



class get_user_menu(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        items = Bakery_Item_Names.objects.all()
        data = user_menu_serializer(items,many=True)
        return(Response(data.data,status=status.HTTP_200_OK))



class user_order_view(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        uid = request.user.id
        try:
            ods_name  = dict(request.data)
            s = 0
            bill={}
            for i in ods_name:
                cost = int(Bakery_Item_Names.objects.get(bakery_item = str(i)).price)
                cost = cost  * ( 1 - (int(Bakery_Item_Names.objects.get(bakery_item = str(i)).discount) /100))            # selling price - discount
                bill[i] = int(ods_name[i])*cost
                s+=int(ods_name[i])*cost   
                history = orders(user=User(id=uid),
                       bakery_item = Bakery_Item_Names.objects.get(bakery_item=i),
                       quantity = int(ods_name[i]),
                       cost=bill[i])
                history.save()       
            bill["Total"] = s 
            bill["Status"] = "Order Placed"    
            return(Response(bill,status=status.HTTP_200_OK))
        except Exception as e:
            return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))     



class order_history(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        uid = request.user.id
        try:
            ods = orders.objects.filter(user = uid)
            history = orders_serializer(ods,many=True)
            return(Response(history.data,status=status.HTTP_200_OK))
        except Exception as e:
            return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))


class most_sellling_item(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        items = Bakery_Item_Names.objects.all()
        final = {}
        for i in items:
            q = orders.objects.filter(bakery_item=i.id).aggregate(s = Sum('quantity'))
            final[i.bakery_item] = int(q["s"])*int(i.price)
        result = max(final, key=final.get)    
        return(Response({"Best Selling Item":result}))    



    

class ADD_DISCOUNT(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,item_name,dis):
        if request.user.is_superuser:
            try:
                Bakery_Item_Names.objects.filter(bakery_item=str(item_name).update(discount=dis))
                return(Response({"status":"Added a discount of "+str(dis)+" for "+item_name},status=status.HTTP_200_OK))
            except Exception as e:
                return(Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST))   
        else:
            return(Response({"Alert":"Not Allowed"},status=status.HTTP_401_UNAUTHORIZED))         
