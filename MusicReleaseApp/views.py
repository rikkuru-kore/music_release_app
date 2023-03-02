from django.shortcuts import render,redirect,get_object_or_404
from .models import Items,Orders
from .forms import ItemCreateForm,EmailForm
from .email_handler import send_mail
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.conf import settings

from datetime import datetime
from pytz import timezone
import stripe

# Create your views here.
def index(request):
    items = Items.objects.all()
    return render(request,'index.html',context={"items":items})

def search(request):
    query = request.GET.get('query') or ""
    if query:
        items = Items.objects.filter(Q(title__icontains=query)|Q(artist__icontains=query)).all()
    else:
        return redirect(index)
    return render(request,'index.html',context={"items":items,"query":query})

@login_required
def tab_maintenance(request):
    tabs = Items.objects.filter(division=0).all()
    division = 0
    return render(request,'item/item_maintenance.html',context={"items":tabs,'division':division})

@login_required
def music_maintenance(request):
    musics = Items.objects.filter(division=1).all()
    division = 1
    return render(request,'item/item_maintenance.html',context={"items":musics,'division':division})

@login_required
def item_create(request,division):
    if division:
        form = ItemCreateForm(request.POST or None,request.FILES or None,initial={'division':1})
    else:
        form = ItemCreateForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        if division:
            return redirect(music_maintenance)
        else:
            return redirect(tab_maintenance)
    return render(request,'item/item_create.html',context={'form':form,'division':division})

@login_required
def item_edit(request,id,division):
    item = get_object_or_404(Items, pk=id)
    form = ItemCreateForm(request.POST or None,request.FILES or None,instance=item)
    if form.is_valid():
        form.save()
        if division:
            return redirect(music_maintenance)
        else:
            return redirect(tab_maintenance)
    return render(request,'item/item_create.html',context={'form':form,'item':item,'division':division})

@login_required        
def item_delete(request,id):
    item = get_object_or_404(Items, pk=id)
    if item.division:
        item.delete()
        return redirect(music_maintenance)
    else:
        item.delete()
        return redirect(tab_maintenance)

def detail_item(request,id):
    item = get_object_or_404(Items, pk=id)
    if not item.publish:
        raise Http404
    return render(request,'item/detail_item.html',context={'item':item})

def input_email(request,id):
    form = EmailForm(request.POST or None)
    if form.is_valid():
        item = get_object_or_404(Items, pk=id)
        if not item.publish:
            raise Http404
        order = Orders.objects.create(item=item,email=form.cleaned_data.get('email'))
        return redirect('create_checkout_session',order_id=order.id)
    return render(request,'input_email.html',context={'form':form})

stripe.api_key = settings.STRIPE_API_KEY

def pay_success(request):
    order_id = request.GET.get('order_id')
    date = request.GET.get('date')
    order = Orders.objects.filter(id=int(order_id)).first()
    if not order.tentative_sale == date:
        raise Http404
    item = Items.objects.get(id=order.item.id)
    gmail = 'garidebu.max120@gmail.com'
    password = 'trpbktgodlmqidjc' # secretにする
    if item.division:
        division = '楽曲'
        file = item.music
    else:
        division = 'Tab譜'
        file = item.tab
    subject = f'{division}「{item.title}/{item.artist}」の送信'
    text = f"""
お客様

いつもお世話になっております。

この度はご購入頂きありがとうございます。
「{item.title}/{item.artist}」の{division}をお送りします。

良い音楽ライフを送れることを祈っております。

今後ともFlat Landをよろしくお願い致します。

Flat Land
        """
    send_mail(gmail=gmail, password=password, to=order.email, subject=subject,text=text,filename=file)
    item.sale += 1
    item.save()
    return render(request,'success.html')

def pay_cancel(request):
    order_id = request.GET.get('order_id')
    date = request.GET.get('date')
    order = Orders.objects.filter(id=int(order_id)).first()
    if not order.tentative_sale == date:
        raise Http404
    order.delete()
    return render(request,'cancel.html')

tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=0.1 * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)

def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': unit_amount,
            'product_data': {'name': name, }
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id]
    }

my_url = settings.MY_URL

def create_checkout_session(request,order_id):
    order = Orders.objects.filter(id=order_id).first()
    if order.tentative_sale:
        raise Http404
    line_items = []
    order.tentative_sale = date = datetime.now(timezone('Asia/Tokyo')).strftime('%Y%m%d%H%M%S%f')
    order.save()
    line_item = create_line_item(order.item.price, order.item.title, 1)
    line_items.append(line_item)
    
    checkout_session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url= my_url + f'/pay/success/?order_id={order.id}&date={date}',
        cancel_url= my_url + f'/pay/cancel/?order_id={order.id}&date={date}'
    )
    return redirect(checkout_session.url)

def show_error_page(request,exception):
    return render(request,'404.html')
