from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Ingredient, Inventory, Transaction, Box, Store
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def get_store_id_from_username(username):
    if username.startswith('LittleBytes'):
        store_id = username[11:]
        if store_id.isdigit():
            return '{:02d}'.format(int(store_id))
    return None

@login_required
def inventory(request):
    store_id = get_store_id_from_username(request.user.username)
    if store_id:
        query_results = Inventory.objects.filter(store__id=store_id)
    else:
        query_results = Inventory.objects.all()
        
    low_stock = request.GET.get('stock', 'all')=='low'
    if low_stock:
        query_results = query_results.filter(stock__lt=5)

    order_by = request.GET.get('sort', 'item')
    map_to_field = {'item': 'name', 'store': 'store', 'expiration': 'date_exp'}
    order_by = map_to_field.get(order_by, 'name')
    query_results = query_results.order_by(order_by)
    
    return render(request, 'littlebytes/inventory.html', {'query_results': query_results})

@login_required
def sales(request):
    store_id = get_store_id_from_username(request.user.username)
    if store_id:
        query_results = Transaction.objects.filter(store__id=store_id)
    else:
        query_results = Transaction.objects.all()

    order_by = request.GET.get('sort', 'store')
    map_to_field = {'store': 'store', 'date': 'date'}
    order_by = map_to_field.get(order_by, 'store')
    query_results = query_results.order_by(order_by)

    # Get all ingredients and cost
    from django.db.models import Sum, F, DecimalField
    cost_per_unit = 'box__boxcontents__sandwich__ingredients__inventory__cost_per_unit'
    ingredient_amount = 'box__boxcontents__sandwich__ingredients__sandwichrecipe__ingredient_amount'
    query_results = query_results.annotate(cost=Sum(F(cost_per_unit)*F(ingredient_amount),
                                                    output_field=DecimalField(decimal_places=2)))

    return render(request, 'littlebytes/sales.html', {'query_results': query_results})

@login_required
def add_sale(request):
    from django.db.models import Min, Sum, F, DecimalField, Count
    authorized_store_id = get_store_id_from_username(request.user.username)
    confirm = 'confirm' in request.POST
    context = {'error': ''}
    if not confirm:
        context['stores'] = (Store.objects.filter(id=authorized_store_id)
                             if authorized_store_id else Store.objects.all())
        context['boxes'] = Box.objects.all()
    else:
        store_id = request.POST.get('store', None)
        if authorized_store_id and (authorized_store_id!=store_id):
            context['error'] = 'Store ID {} is invalid'.format(store_id)
        else:
            barcode = request.POST.get('barcode', None)
            box = Box.objects.filter(barcode=barcode)
            if len(box)!=1:
                context['error'] = 'Barcode {} is invalid'.format(barcode)
            else:
                inventory_index = 'contents__ingredients__inventory'
                inventory_store = 'contents__ingredients__inventory__store'
                ingredient = 'boxcontents__sandwich__ingredients__sandwichrecipe__ingredient'
                ingredient_amount = 'boxcontents__sandwich__ingredients__sandwichrecipe__ingredient_amount'
                ingredients = box.values(index=F(inventory_index),name=F(ingredient),store=F(inventory_store)) \
                                 .annotate(amount=Sum(F(ingredient_amount)))
                sandwich_count = box.aggregate(sandwich_count=Count('contents'))['sandwich_count']
                transaction = Transaction(box=box[0],
                                          store=Store.objects.get(id=store_id),
                                          transaction_type=request.POST.get('type', 'w'),
                                          gross=sandwich_count*3.25)
                items = Inventory.objects.all()
                updatedItems = []
                for i in ingredients:
                    if i['store'] and i['store']!=transaction.store.id:
                        continue
                    if i['index']==None:
                        context['error'] = 'Cannot find "{}" in the store inventory.'.format(i['name'])
                        break
                    item = items[i['index']-1]
                    amount = i['amount']
                    if item.stock<amount:
                        context['error'] = 'Not enough "{}" in  in Store "{}".'.format(i['name'], transaction.store)
                        break
                    item.stock -= amount
                    updatedItems.append(item)
                if context['error']=='':
                    for item in updatedItems:
                        item.save()
                    transaction.save()
                    context['error'] = 'Transaction "{}" added.' \
                                       .format(transaction.id)
                    context['transaction'] = transaction
    return render(request, 'littlebytes/add_sale.html', context)

@login_required
def reports(request):
    import itertools
    import datetime
    from django.db.models.functions import TruncDate
    from django.db.models import Avg, Count, F, Sum, DecimalField

    start_date = request.GET.get('start', None)
    end_date = request.GET.get('end', None)
    context = {}
    if start_date==None:
        days = [x['tdate'] for x in Transaction.objects.annotate(tdate=TruncDate('date')).values('tdate').distinct()]
        weeks = []
        for week,wd in itertools.groupby(days, key=lambda x: x.isocalendar()[1]):
            start = datetime.datetime.strptime('{} {} 1'.format(next(wd).year, week), '%Y %W %w')
            end = start + datetime.timedelta(days=7)
            weeks.append((start,end))
        context = {'daily': days, 'weekly': weeks}
    else:
        authorized_store_id = get_store_id_from_username(request.user.username)
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end = (datetime.datetime.strptime(end_date, '%Y-%m-%d')
               if end_date else start + datetime.timedelta(days=1))

        inventory_store = 'box__contents__ingredients__inventory__store'
        ingredient = 'box__boxcontents__sandwich__ingredients__sandwichrecipe__ingredient'
        ingredient_amount = 'box__boxcontents__sandwich__ingredients__sandwichrecipe__ingredient_amount'
        cost_per_unit = 'box__boxcontents__sandwich__ingredients__inventory__cost_per_unit'

        all_sales = Transaction.objects.filter(date__gte=start, date__lt=end)
        units = dict(Ingredient.objects.all().values_list('name', 'unit'))
        stores = (Store.objects.all() if authorized_store_id==None
                  else Store.objects.filter(id=authorized_store_id))
        storeReports = []
        for s in stores:
            sales = all_sales.filter(store__id=s.id)
            ingredients = sales.filter(store=F(inventory_store)) \
                               .values('store', name=F(ingredient)) \
                               .annotate(amount=Sum(F(ingredient_amount),
                                                    output_field=DecimalField(decimal_places=2)))
            ingredients = [(item['name'],units[item['name']],item['amount'])
                           for item in ingredients]
            box_stats = sales.values('box') \
                             .annotate(avg_gross=Avg('gross'),
                                       cost=Sum(F(cost_per_unit)*F(ingredient_amount),
                                                output_field=DecimalField(decimal_places=2)))
            boxes_count = dict(sales.values_list('box') \
                                    .annotate(count=Count('box')))
            for b in box_stats:
                b['count'] = boxes_count[b['box']]
            total_gross = sales.aggregate(total_gross=Sum('gross'))
            store = {'store': s,
                     'ingredients': ingredients,
                     'box_stats': box_stats,
                     'total_gross': total_gross['total_gross'],
                     'total_tax': total_gross['total_gross']*s.tax/100,
                     }
            storeReports.append(store)
        context['reports'] = storeReports
        context['start_date'] = start
        context['end_date'] = end

    return render(request, 'littlebytes/reports.html', context)

@permission_required('entity.can_add_user', login_url='/')
def register(request):
    if request.method == 'POST':

        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = UserCreationForm()

    return render(request, 'littlebytes/register.html', {'form': f})


