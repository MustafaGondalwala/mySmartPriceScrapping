from django.http import HttpResponse,JsonResponse
import requests
from bs4 import BeautifulSoup
import json
from .models import AutoSuggestion,Product,ProductDescription,ProductLinks
from django.db.models import Q
import datetime


	
def store_product(link):
	try:
		req = requests.get(search)
	except:
		return JsonResponse({"error":"Error Occured"},safe=False)
	soup = BeautifulSoup(req.text)
	all_images_container = soup.findAll("img",attrs={"class":"prdct-dtl__thmbnl-img"})
	all_images = []
	for i in all_images_container:
	  all_images.append({'image':i['data-image']})
	price_container = soup.findAll("div",attrs={"class":"prc-tbl__btn"})
	store = []
	for i in price_container:
		temp = i.a['href']
		store_name = temp.split("store=")[1].split(">")[0]
		price = temp.split("sprice=")[1].split("&")[0]
		store.append({"store_name":store_name,"price":price})
	bullets_container = soup.findAll("li",attrs={"class":"prdct-dtl__spfctn"})
	bullets = []
	for i in bullets_container:
	  bullets.append(i.text)

	try:
		description = soup.find("div",attrs={"class":"main-wrpr__cols3"})
	except:
		description = ""
	try:
		title = soup.find("h1",attrs={"class":"prdct-dtl__ttl"}).text
	except:
		title = ""
	try:
		rating = soup.find("span",attrs={"itemprop":"ratingValue"}).text
	except:
		rating = 0
	ProductDescription(link=search,store=json.dumps(store),all_images=json.dumps(all_images),bullets=json.dumps(bullets),description=str(description),title=title,rating=rating).save()


def specific_product(request):
	keyword = request.GET['keyword']
	main = []
	check_in_db = Product.objects.filter(keyword = keyword)[:10]
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
		return JsonResponse(main,safe=False);
	else:
		return JsonResponse([],safe=False);
	pass
def product_search(request):
	search = request.GET['search']
	try:
		page = request.GET['page']
	except:
		page = 1
	main = []
	check_in_db = Product.objects.filter(keyword = search,page=page)
	print(check_in_db)
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
		return JsonResponse(main,safe=False);

	req = requests.get("https://www.mysmartprice.com/msp/search/msp_search_new.php?subcategory=undefined&s="+search+"&page="+str(page))
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
	        "price":price,
	    })
	    try:
	    	Product(keyword=search,image=image,title=title,link=link,rating=rating,price=price,page=page).save()
	    except:
	    	pass
	return JsonResponse(main,safe=False);


def autosuggestion(request):
	keyword = request.GET['search']
	check_in_db = AutoSuggestion.objects.filter(keyword = keyword)
	main = []
	if(check_in_db):
		for i in check_in_db:
			main.append({"title":i.suggesstion})
	else:
		req = requests.get("https://completion.amazon.co.uk/api/2017/suggestions?session-id=258-2024396-2105469&customer-id=&request-id=A8EXFYP8T04RPZTGMM8Q&page-type=Gateway&lop=en_IN&site-variant=desktop&client-info=amazon-search-ui&mid=A21TJRUUN4KGV&alias=aps&b2b=0&fresh=0&ks=8&prefix="+keyword+"&event=onKeyPress&limit=11&fb=1&suggestion-type=KEYWORD&suggestion-type=WIDGET&_=1587382658381")
		for i in req.json()['suggestions']:
		    AutoSuggestion(keyword=keyword,suggesstion=i['value']).save()
		    main.append({"title":i['value']})
	return JsonResponse(main,safe=False);



def validity_check(check_in_db):
	future_date = check_in_db.created_at + datetime.timedelta(days=5)
	current_day = datetime.datetime.now().date()
	if(current_day >= future_date):
		check_in_db.delete()
		return False
	return True

def get_product(request):
	search = request.GET['search']
	if(search.isdigit() == True):
		check_in_db = ProductDescription.objects.filter(id=search).first()
	else:
		check_in_db = ProductDescription.objects.filter(link=search).first()
	if(check_in_db):
		if(validity_check(check_in_db)):
			main = {
				"store":json.loads(check_in_db.store),
				"all_images":json.loads(check_in_db.all_images),
				"bullets":json.loads(check_in_db.bullets),
				"title": check_in_db.title,
				"description": check_in_db.description,
				"link":check_in_db.link,
				"rating":check_in_db.rating,
				"id":check_in_db.id,
			}
			return JsonResponse(main,safe=False)
	try:
		req = requests.get(search)
	except:
		return JsonResponse({"error":"Error Occured"},safe=False)
	soup = BeautifulSoup(req.text)
	all_images_container = soup.findAll("img",attrs={"class":"prdct-dtl__thmbnl-img"})
	all_images = []
	for i in all_images_container:
	  all_images.append({'image':i['data-image']})
	
	price_container = soup.findAll("div",attrs={"class":"prc-tbl__btn"})
	store = []
	for i in price_container:
		try:
			temp = i.a['href']
			store_name = temp.split("store=")[1].split(">")[0]
			price = temp.split("sprice=")[1].split("&")[0]
			store.append({"store_name":store_name,"price":price})
		except:
			pass
	bullets_container = soup.findAll("li",attrs={"class":"prdct-dtl__spfctn"})
	bullets = []
	for i in bullets_container:
	  bullets.append(i.text)
	try:
		description = soup.find("div",attrs={"class":"main-wrpr__cols3"})
	except:
		description = ""
	try:
		title = soup.find("h1",attrs={"class":"prdct-dtl__ttl"}).text
	except:
		title = ""
	try:
		rating = soup.find("span",attrs={"itemprop":"ratingValue"}).text
	except:
		rating = 0
	ProductDescription(link=search,store=json.dumps(store),all_images=json.dumps(all_images),bullets=json.dumps(bullets),description=str(description),title=title,rating=rating).save()
	main = {
		"store":store,
		"all_images":all_images,
		"bullets":bullets,
		"title":title,
		"description":str(description),
		"rating":rating,
		"link":search
	}
	return JsonResponse(main,safe=False);



def get_links(request):
	search = request.GET['search']
	if(search.isdigit() == True):
		check_in_db = ProductDescription.objects.filter(id=search).first()
	else:
		check_in_db = ProductDescription.objects.filter(link=search).first()
	if(check_in_db):
		if(check_in_db.product_link_json != ""):
			if(validity_check(check_in_db)):
				main = {
					"product_links" : json.loads(check_in_db.product_link_json),
					"id" : check_in_db.id
				}
				return JsonResponse(main,safe=False)
	try:
		main_page = requests.get(search)
	except:
		return JsonResponse({"error":"Error Occured"},safe=False)
	soup = BeautifulSoup(main_page.text)
	price_container = soup.findAll("div",attrs={"class":"prc-tbl__btn"})
	store = []
	for i in price_container:
		temp = i.a['href']
		store_name = temp.split("store=")[1].split(">")[0]
		get_product_link = requests.get(temp)
		soup = BeautifulSoup(get_product_link.text)
		meta = soup.find("meta",attrs={"http-equiv":"Refresh"})
		actual_link = meta['content'].split("url=")[1]
		store.append({"store_name":store_name,"actual_link":actual_link})
	if(search.isdigit() == True):
		ProductDescription.objects.filter(id=search).update(product_link_json=json.dumps(store))
	else:
		ProductDescription.objects.filter(link=search).update(product_link_json=json.dumps(store))
	main = {
		"product_links" : store
	}
	return JsonResponse(main,safe=False)

	pass
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")