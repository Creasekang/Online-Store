from django.shortcuts import render,redirect,reverse 
from django.http import HttpResponse,request
from .models import User_info,Food_info,Raw_material, Order
from django.utils.datastructures import MultiValueDictKeyError
from django.db import connection
import os
# Create your views here.

def execute_sql(sql_statement,para_list):
    with connections.cursor() as cursor:
        cursor.execute(sql_statement,para_list)
        return cursor


def index(request):
    user_list = User_info.objects.all()
    sql_statement="select * from polls_user_info"
    para_list=[]
    execute_sql(sql_statement,para_list)
    context = {
        'user_list': user_list,
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method=='GET':
      return render(request, 'register.html')
    if request.method=='POST':
       name=request.POST['uname']
       password=request.POST['upassword'] 
       u=0
       try:
           sql_statement="insert into polls_order(user_name,user_password) VALUES (%s, %s)"
           para_list=[name,password]
           u=execute_sql(sql_statement,para_list)
       except:
            u=User_info(user_name=name,user_password=password)
            u.save()
       path=os.path.join(BASE_DIR,"static","media","img",str(u.user_id))
       if not os.path.exists(path):
                os.mkdir(path)
       return HttpResponse("Succeed!")

def login(request):
    if request.method=='GET':
      return render(request, 'login.html')
    if request.method=='POST':
       name=request.POST['uname']
       password=request.POST['upassword']
       u=0
       try:
            sql_statement="select * from polls_user_info where user_name = %s and user_password =%s"
            para_list=[name, password]
            u=execute_sql(sql_statement,para_list)
       except:
           u=User_info.objects.filter(user_name=name, user_password=password)
       if u.count()==0:
           return HttpResponse("Login Failed!")
       elif u.count()==1:
           del request.session['user_name']
           request.session['user_name']=name
       context = {
        'u': name
       }
       return redirect(reverse('detail'))
    
def add(request):
    if request.method=='GET':
        return render(request, 'add.html')
    if request.method=='POST':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user=0
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name'])
            path=os.path.join(BASE_DIR,"static","media","img",str(user.user_id),"food")
            if not os.path.exists(path):
                os.mkdir(path)
            food_name=request.POST['food_name']
            food_price=request.POST['food_price']
            food_quantity=request.POST['food_quantity']
            food_intro_text=request.POST['food_intro_text']
            f=Food_info(upload_user=user,food_name=food_name,food_price=food_price,food_quantity=food_quantity,
            food_intro_text=food_intro_text)
            ls = os.listdir(path)
            for p in ls:
                if p==str(f.food_id)+"pic.jpg":
                    os.remove(os.path.join(path, p))
            f.save()
            f.food_img=request.FILES.get('picture')
            f.food_img.name=str(f.food_id)+"pic.jpg"
            f.save()
            return redirect(reverse('food_detail', args=[f.food_id]))

def food_modify(request,food_id):
    if request.method=='GET':
        food = 0
        try:
            sql_statement="select * from polls_food_info where food_id = %s"
            para_list=[food_id]
            food=execute_sql(sql_statement,para_list)
        except:
            food = Food_info.objects.get(food_id=food_id)
        context={
            'food':food
        }
        return render(request, 'food_modify.html',context)
    elif request.method=='POST':
        f = Food_info.objects.get(food_id=food_id)
        try:
            sql_statement="select * from polls_food_info where food_id = %s"
            para_list=[food_id]
            execute_sql(sql_statement,para_list)
        except:
            f = Food_info.objects.get(food_id=food_id)
        user=f.upload_user
        path=os.path.join(BASE_DIR,"static","media","img",str(user.user_id),"food")
        if not os.path.exists(path):
            os.mkdir(path)
        ls = os.listdir(path)
        for p in ls:
            if p==str(f.food_id)+"pic.jpg":
               os.remove(os.path.join(path, p))
        f.food_img=request.FILES.get('picture')
        f.food_img.name=str(f.food_id)+"pic.jpg"
        f.save()
        f.food_name=request.POST['food_name']
        f.food_price=request.POST['food_price']
        f.food_quantity=request.POST['food_quantity']
        f.food_intro_text=request.POST['food_intro_text']
        f.save() 
        return redirect(reverse('food_detail', args=[f.food_id]))

def food_detail(request,food_id):
    if request.method=='GET':
        food = 0
        try:
            sql_statement="select * from polls_food_info where food_id = %s"
            para_list=[food_id]
            food=execute_sql(sql_statement,para_list)
        except:
            food = Food_info.objects.get(food_id=food_id)
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            context={
                'food':food,
                'user':food.upload_user,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'food_detail.html',context)


def detail(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            u = User_info.objects.get(user_name=user_name)  
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[user_name]
                execute_sql(sql_statement,para_list)
            except:
                u = User_info.objects.get(user_name=user_name)
            food_list=u.food_info_set.all()
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            context={
                'food_list':food_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'detail.html',context)

def food_delete(request,food_id):
    if request.method=='GET':
        Food_info.objects.filter(food_id=food_id).delete()
        return redirect(reverse('detail'))

def food_index(request):
    if request.method=='GET':
        food_list = Food_info.objects.all()  
        try:
            sql_statement="select * from polls_food_info"
            para_list=[]
            execute_sql(sql_statement,para_list)
        except:
            food_list = Food_info.objects.all()  
        user_name = request.session.get('user_name', '')
        if not user_name:
            login=False
            u_name=""
        else:
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
        context = {
            'food_list': food_list,
             'login':login,
             'u_name':u_name
        }
        return render(request, 'food_index.html', context)

def buy(request,food_id):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user=0
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name'])
            food = 0
            try:
                sql_statement="select * from polls_food_info where food_id = %s"
                para_list=[food_id]
                food=execute_sql(sql_statement,para_list)
            except:
                 food = Food_info.objects.get(food_id=food_id)
            u = Order.objects.filter(buyer=user, seller=food.upload_user, food_id=food.food_id, has_pay=False, has_complete=False) 
            try:
                sql_statement="select * from polls_order where buyer = %s and seller = %s and food_id = %s and has_pay = %d and has_complete = %d"
                para_list=[buyer, seller, food_id, has_pay, has_complete]
                execute_sql(sql_statement,para_list)
            except:
                 u = Order.objects.filter(buyer=user, seller=food.upload_user, food_id=food.food_id, has_pay=False, has_complete=False) 
            if u.count()==0:
                
                try:
                    sql_statement="insert into order(buyer, seller, food_id, has_pay, has_complete) VALUES (%s, %s, %s, %d, %d)"
                    para_list=[buyer, seller, food_id, has_pay, has_complete]
                    execute_sql(sql_statement,para_list)
                except:
                    order=Order(buyer=user,seller=food.upload_user,food_id=food_id,food_price=food.food_price,food_name=food.food_name,food_num=1,cost=food.food_price,
                    has_pay=False, has_complete=False) 
                    order.save()
            elif u.count()==1:
                u=Order.objects.get(buyer=user,seller=food.upload_user,food_id=food.food_id,has_pay=False,has_complete=False)
                u.food_num=u.food_num+1
                u.cost=u.cost+food.food_price
                u.save()
            return HttpResponse("购买成功，已添加到购物车")

def pre_order(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name

            user = 0 
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name']) 

            order_list=0
            try:
                order_list=sql_statement="select * from polls_order where buyer = %s and has_pay = %d"
                order_list=para_list=[user, False]
                order_list=execute_sql(sql_statement,para_list)
            except:
                order_list = Order.objects.filter(buyer=user, has_pay=False) 

            context={
                'user':user_name,
                'order_list':order_list,
                 'login':login,
                  'u_name':u_name
            }
            return render(request, 'pre_order.html',context)

def pay(request,food_id):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = 0
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name']) 

            order = 0
            try:
                sql_statement="select * from polls_order where buyer = %s and food_id = %s and has_pay = %d"
                para_list=[user, food_id, False]
                order=execute_sql(sql_statement,para_list)
            except:
                order = Order.objects.get(buyer=user, food_id=food_id, has_pay=False)  

            food=0
            try:
                sql_statement="select * from polls_food_info where food_id = %s"
                para_list=[order.food_id]
                food=execute_sql(sql_statement,para_list)
            except:
                food = Food_info.objects.get(food_id=order.food_id) 
                
            if food.food_quantity>=order.food_num:
                food.food_quantity=food.food_quantity-order.food_num
                food.save()
                order.has_pay=True
                order.save()
                return redirect(reverse('pre_order'))
            else:
                context={
                    'food':food,
                    'order':order
                }
                return render(request, 'pay.html',context)

def plus(request,food_id):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = 0  
            try:
                sql_statement="select * from polls_user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name'])  

            food = 0
            try:
                sql_statement="select * from polls_food_info where food_id = %s"
                para_list=[food_id]
                food=execute_sql(sql_statement,para_list)
            except:
                food = Food_info.objects.get(food_id=food_id)

            u=Order.objects.get(buyer=user,seller=food.upload_user,food_id=food.food_id,has_pay=False,has_complete=False)     
            u.food_num=u.food_num+1
            u.cost=u.cost+food.food_price
            u.save()
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            
            order_list = 0
            try:
                sql_statement="select * from polls_order where buyer = %s and has_pay = %d"
                para_list=[user, False]
                execute_sql(sql_statement,para_list)
            except:
                order_list = Order.objects.filter(buyer=user, has_pay=False)  
            context={
                'user':user_name,
                'order_list':order_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'pre_order.html',context)

def minus(request,food_id):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = 0 
            try:
                sql_statement="select * from polls_user_info where user_name = %s "
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user=User_info.objects.get(user_name=request.session['user_name'])

            food = 0
            try:
                sql_statement="select * from polls_food_info where food_id = %s "
                para_list=[food_id]
                food=execute_sql(sql_statement,para_list)
            except:
                food = Food_info.objects.get(food_id=food_id) 

            u=Order.objects.get(buyer=user,seller=food.upload_user,food_id=food.food_id,has_pay=False,has_complete=False)
            if u.food_num==1:
                u.delete()
            elif u.food_num>1:
                u.food_num=u.food_num-1
                u.cost=u.cost-food.food_price
                u.save()
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            order_list=Order.objects.filter(buyer=user,has_pay=False)
            context={
                'user':user_name,
                'order_list':order_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'pre_order.html',context)

def order(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user =0  
            try:
                sql_statement="select * from polls_user_info where user_name = %s "
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name']) 

            order_list =0
            try:
                sql_statement="select * from order where buyer=%s and has_pay=%d"
                para_list=[user, True]
                order_list =execute_sql(sql_statement,para_list)
            except:
                order_list = Order.objects.filter(buyer=user, has_pay=True)

            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            context={
                'user':user_name,
                'address':user.address,
                'order_list':order_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'order.html',context)

def complete(request,food_id):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = User_info.objects.get(user_name=request.session['user_name']) 
            try:
              sql_statement="select * from user_info where user_name = %s"
              para_list=[request.session['user_name']]
              user = execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name']) 
            order=Order.objects.get(buyer=user,food_id=food_id,has_pay=True,has_complete=False)
            order.has_complete=True
            order.save()
            order_list=Order.objects.filter(buyer=user,has_pay=True)
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            context={
                'user':user_name,
                'order_list':order_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'order.html',context)

def sell_order(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = User_info.objects.get(user_name=request.session['user_name'])  
            try:
                sql_statement="select * from user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user =execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name'])  

            order_list=Order.objects.filter(seller=user,has_pay=True)
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            context={
                'user':user_name,
                'order_list':order_list,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'sell_order.html',context)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def user_detail(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = 0
            try:
                sql_statement="select * from user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user=User_info.objects.get(user_name=request.session['user_name'])
            path=os.path.join(BASE_DIR,"static","media","img",str(user.user_id))
            ls = os.listdir(path)
            img_path=os.path.join(path)
            login=True
            u_name=User_info.objects.get(user_name=request.session['user_name']).user_name
            for p in ls:
                if str(p)==str(user.user_id)+"pic.jpg":
                     img_path=os.path.join(path,p)
                     break
            context={
                'user':user,
                'img_path':img_path,
                'login':login,
                'u_name':u_name
            }
            return render(request, 'user_detail.html',context)



def user_modify(request):
    if request.method=='GET':
        user_name = request.session.get('user_name', '')
        if not user_name:
            return render(request, 'login.html')
        else:
            user = 0
            try:
                sql_statement="select * from user_info where user_name = %s"
                para_list=[request.session['user_name']]
                user=execute_sql(sql_statement,para_list)
            except:
                user = User_info.objects.get(user_name=request.session['user_name'])  

            context={
                'user':user
            }
            return render(request, 'user_modify.html',context)
    elif request.method=='POST':
        user = 0 
        try:
            sql_statement="select * from user_info where user_name = %s"
            para_list=[request.session['user_name']]
            user =execute_sql(sql_statement,para_list)
        except:
            user = User_info.objects.get(user_name=request.session['user_name']) 

        user.phone_num=request.POST['phone_num']
        user.address=request.POST['address']
        path=os.path.join(BASE_DIR,"static","media","img",str(user.user_id))
        ls = os.listdir(path)
        for p in ls:
            if p==str(user.user_id)+"pic.jpg":
               os.remove(os.path.join(path, p))
        user.img=request.FILES.get('picture')
        user.img.name=str(user.user_id)+"pic.jpg"
        user.save() 
        return redirect(reverse('user_detail'))

