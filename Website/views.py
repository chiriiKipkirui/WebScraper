from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
import requests
from PIL import Image
import bs4
import os
import re
import copy
from datetime import datetime
import matplotlib.pyplot as plt
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
#from easy_pdf.views import PDFTemplateView
from django.views.generic import View
from django.http import HttpResponse
#from ezraWeb.utils import render_to_pdf
from easy_pdf.rendering import render_to_pdf
from django.http import HttpResponse
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse


# Create your views here.
price = []
Labels = []
dict_= {}
date_today = datetime.now()
global_query = ''
productDetails = []


@login_required
def Home(request):
    td = datetime.now()
    date_today =td

    osName = ''
    if os.name =='nt':
            osName =osName.replace('','windows')
    else:
        pass
    context = {'today':td,'os_name':osName,'name':request.user.username}
    return render(request,'mainpage/home.html',context)
   
@login_required
def About(request):
    name = ' Shop adviser'
    version = ' Version V1.01'
    developer = ' Ezra Chirchir'
    contact = '@ezrachirii'
    email = 'kipkiruichirii@outlook.com'
    license_ = 'It\'s under the common BSD licence.All code can be downloaded on GitHub Repository'
    Thanks = 'Let me pass my Sincere gratitude to the University Supervisor Madam Lily Siele, and all the lecturers at the University of Eldoret.'
    
    
    context = {'name':name,'version':version,'developer':developer,'contact':contact,'email':email,'license':license_,'Thanks':Thanks}
    return render(request,'mainpage/about.html',context)
@login_required
def analytics(request):
    global global_query
    query = request.GET.get('q')
    if query == None:
        query = 'iphone 6'
        global_query=query
    else:
        query=query

        global_query = query
    query_modified = query.replace(' ','+')
    #defining the function that would scrape the various websites 
 
    def avechiScrapper(productUrl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        res = requests.get(productUrl, headers=headers)
        res.raise_for_status()


        soup = bs4.BeautifulSoup(res.text, 'lxml')
        #elms = soup.select('.woocommerce-Price-amount amount')
        ins = soup.find('span',attrs={'data-price-type':'finalPrice'})
    
        #for i in ins:print(float(i.text[3:].replace(',',''))/98)
        if ins==[]:
            #print("Product not found")
            price_none = 0
            #price.insert(0,price_none)
        else:
            price_ins= ins
            priceAvechi = float(price_ins.text[4:].replace(',',''))
            price.insert(0,priceAvechi)
   


    def killmallScraper(productUrl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        res = requests.get(productUrl, headers=headers)
        res.raise_for_status()


        soup = bs4.BeautifulSoup(res.text, 'lxml')
        elms = soup.select('.sale-price')
        price_ = elms[0].string
        price_ = price_[4:]
        price_ = price_.replace(',','')
        price_= float(price_)
        killMallprice=price_
        price.insert(1,killMallprice)
       
        

    def JumiaScraper(productUrl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        res = requests.get(productUrl, headers=headers)
        res.raise_for_status()


        soup = bs4.BeautifulSoup(res.text, 'lxml')
        #elms = soup.select('.price')
        price_container =  soup.find_all('span', attrs={'dir':'ltr','data-price':re.compile('\d+')})
        prices_jumia = []
        for i in range(4):
            prices_jumia.append(price_container[i].get_text('data-price'))
        price_jumia = max(prices_jumia) #getting the maximum price among the four prices due to adds
        jumiaPrice = float(price_jumia.replace(',',''))/98
        if jumiaPrice <0:
            jumiaPrice = str(jumiaPrice)[1:]
            jumiaPrice = float(jumiaPrice)
        else:
            jumiaPrice=jumiaPrice
        price.insert(2,jumiaPrice*98)
        #GETTING THE PRODUCT DETAILS 
        details_url = soup.find('a',{'class':'link'}).attrs['href']
        res_product_details = requests.get(details_url,headers = headers)
        soup_details = bs4.BeautifulSoup(res_product_details.text,'lxml')
        details = soup_details.find('div',{'class':'list -features -compact -no-float'})
        details_li = details.ul.contents
        for i in range(len(details_li)):
            productDetails.append(details_li[i].text)

    
  

    killmallScraper('https://www.kilimall.co.ke/?act=search&keyword='+query_modified)
    JumiaScraper('https://www.jumia.co.ke/catalog/?q='+query_modified)
   # ebayScraper('https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2050601.m570.l1313.TR0.TRC0.H0.X'+query_modified +'TRS0&_nkw='+query_modified+'&_sacat=0')
    avechiScrapper('https://avechi.co.ke/catalogsearch/result/?q='+query_modified)
    #the contexts
    def deleteimage():
         try:
            im = Image.open('/static/'+query_modified.replace('+','')+'.png')
            if im:
                os.remove(im)
            else:
                pass
         except:
            pass
    deleteimage()
         


    def plots():
        labels = ['Avechi.co.ke', 'Killmall.co.ke', 'Jumia.co.ke']
        Labels=labels
        sizes = [x for x in price]
        #if len(sizes)<len(labels):
           # sizes.append(0)
        colors = ['gold', 'yellowgreen', 'lightcoral', ]
        explode = (0.1, 0,0)  # explode 1st slice
         
        # Plot
        plt.pie(price, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
         
        plt.axis('equal')
        plt.savefig('ezraWeb/static/'+query_modified+'.png')
    plots()
    dictprice = {'avechi':"{0:.2f}".format(price[0]),'killmall':"{0:.2f}".format(price[1]),'jumia':"{0:.2f}".format(price[2])}
    global dict_ 
    dict_ =  copy.deepcopy(dictprice)
    context = {'query':query,'price':price,'dict':dictprice,'query_modified':query_modified,'productDetails':productDetails}
    return render(request,'mainpage/analytics.html',context)
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

        #"pdf generation function and class"
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {#'today': datetime.date.today(),
         'amount': 39.99,
        'customer_name': 'Cooper Mann',
        'order_id': 1233434,
        'base_url' :'file://' + settings.STATIC_URL + '/',
        'price_s':price,
        'dict':dict_,
        'date':date_today,
        'query':global_query,
    
        }
        pdf = render_to_pdf('pdf/contentpage.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


