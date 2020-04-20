from django.http import HttpResponse,JsonResponse
import requests
from bs4 import BeautifulSoup
from .models import AutoSuggestion,Product



def autosuggestion_search(keyword):
	check_in_db = AutoSuggestion.objects.filter(keyword = keyword)
	main = []
	if(check_in_db):
		for i in check_in_db:
			main.append({"title":i.suggesstion})
	return main
	req = requests.get("https://completion.amazon.co.uk/api/2017/suggestions?session-id=258-2024396-2105469&customer-id=&request-id=A8EXFYP8T04RPZTGMM8Q&page-type=Gateway&lop=en_IN&site-variant=desktop&client-info=amazon-search-ui&mid=A21TJRUUN4KGV&alias=aps&b2b=0&fresh=0&ks=8&prefix="+keyword+"&event=onKeyPress&limit=11&fb=1&suggestion-type=KEYWORD&suggestion-type=WIDGET&_=1587382658381")
	for i in req.json()['suggestions']:
	    AutoSuggestion(keyword=keyword,suggesstion=i['value']).save()
	    main.append({"title":i['value']})
	return main


def product_listing_search(product_search):
	main = []
	check_in_db = Product.objects.filter(keyword = product_search)
	if(check_in_db):
		for i in check_in_db:
			main.append({
					"image":i.image,
			        "title":i.title,
			        "link":i.link,
			        "rating":i.rating,
			        "price":i.price,
			        "id":i.id
				})
		return main
	req = requests.get("https://www.mysmartprice.com/msp/search/msp_search_new.php?subcategory=undefined&s="+product_search)
	soup = BeautifulSoup(req.text);
	for i in soup.findAll("div",attrs={"class":"prdct-item"}):
	    image = i.find("img")['data-lazy-src']
	    title = i.find('a',attrs={"class":"prdct-item__name"}).text.strip()
	    link = i.find("a",attrs={"class":"prdct-item__name"})['href']
	    try:
	        rating = i.find("div",attrs={"class":"rtng-star"})['data-tooltip'].split(' ')[1]
	    except:
	        rating = 0
	    price = i.find("span",attrs={"class":"prdct-item__prc-val"}).text.replace(",","")
	    main.append({
	        "image":image,
	        "title":title,
	        "link":link,
	        "rating":rating,
	        "price":price
	    })
	    Product(keyword=product_search,image=image,title=title,link=link,rating=rating,price=price).save()

	return main

def product_search_by_link(link):
	
	return link

def autosuggestion(request):
	search = request.GET['search']
	return JsonResponse(autosuggestion_search(search),safe=False);


def product_search(request):
	search = request.GET['search']
	return JsonResponse(product_listing_search(request.GET['search']),safe=False);


def get_search_by_link(request):

	return JsonResponse(product_search_by_link(request.GET['link']),safe=False);

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")