from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Context, loader
from items.models import Store, Item
import json

labels = {
  'Produce': 'cate_label_produce.png',
  'Home & Lifestyle': 'cate_label_home.png',
  'Groceries': 'cate_label_grocery.png', 
  'Snacks & Candies': 'cate_label_candy.png',
  'Beverage':'cate_label_beverage.png'
}


category = {
  'Produce' : {
    'Vegetables': [
      "Fresh Vegetables",
      "Root Vegetables",
      "Mushrooms",
      "Organic",
      "Squash",
      "Salad Mixes",
    ],
    'Fruits' : [
      "Berries & Grapes",
      "Citrus",
      "Apples & Pears",
      "Melons",
      "Organic",
      "Others",
      "Fruit Bowls",
    ],
    'Bakery' : [
      "Bread",
      "Bagel",
      "Wraps & Pitas",
      "Cake",
      "Store-baked",
    ],
    'Nuts & Seeds' : [
      "Peanuts",
      "Pistachios",
      "Almonds",
      "Trail Mixes",
      "Cashews",
      "Others",
    ],
  },
  'Groceries' : {
    "Coffee & Tea" : [
      "Ground Coffee",
      "Tea",
      "Instant Drink Mix",
    ],
    'Cereal & Breakfast' : [
      "Cereal",
      "Granola Bars",
      "Breakfast Tarts",
      "Oatmeal",
    ],
    'Pasta & Sauces' : [
      "Pasta",
      "Sauces",
    ],
    'Dairy Products' : [
      "Yogurt",
      "Cheese",
      "Butter & Margarine",
    ],
    'Oil, Spices & Seasonning' : [
      "Oil",
      "Salt & Sugar",
      "Spices",
      "Seasoning",
    ],
    'Condiments & Sauces' : [
      "Ketchup & Mustard",
      "Pickles & Olives",
      "Salad dressing",
      "Jam & Spreads",
      "Honey",
      "Meal Helpers",
      "Cooking Sauce",
      "Oriental Curry Sauce",
    ],
    'Soup & Cans' : [
      "Stock Soup",
      "Canned Soup",
      "Canned Meat",
      "Canned Fish",
      "Canned Pasta",
      "Canned Beans",
      "Canned Vegetables",
    ],
    'Frozen Food' : [
      "Fries & Onion rings",
      "Frozen Pizza",
      "Frozen Dinner Packs",
      "Frozen Appetizers",
      "Frozen Fruits",
      "Frozen Vegetable Packs",
      "Icecream Bars",
      "Icecream & Frozen Yogurt",
    ],
  },

  'Snacks & Candies' : {
    'Candy & Choccolates' : [
      "Chocolate Bars",
			"Chocolate Packs",
			"Gummy",
			"Candy Packs",
			"Bulk Packs",
			"Gum",
    ],
    'Chips' : [
      "Lays",
      "Doritos",
      "Organic & Baked",
      "Vegetable Chips",
      "Nacho Chips",
    ],
    'Cookies & Biscuits' : [
      "Cookies",
      "Biscuits",
      "Crackers",
    ],
    'Pudding & Jello' : [
      "Pudding",
      "Jello",
    ],
    'Dried & Fruit Snacks' : [
      "Fruit Snack Pack",
      "Dried Fruits",
    ],
  },

  'Beverage' : {
    'Water' : [
      "Bottled",
			"Enhanced Water",
			"Flavored Water",
			"Carbonated Water",
			"Distilled Water",
    ],
    'Fresh Juice' : [
      "Orange Juice",
			"Oasis",
			"Minute Maid",
    ],
    'Fruit Cocktail' : [
      "Oceanspray",
			"Welches",
			"mix cocktail",
			"lunch-pack",
    ],
    'Non-Dairy' : [	
      'Soy Drinks',
			"Almond Milk",
    ],
    'Energy & Sports' : [
      "Monster",
			"Red Bull",
			"Powerade",
			"Gatorade",
			"Cashews",
			"Others",
    ],
  },
  'Home & Lifestyle' : {
    'Hair Care' : [
      "Hair Enhancement",
      "Oral Care",
      "Female Hygene",
      "Bath & Body",
    ],
    'Home Supplies' : [		
      "Kitchen",
      "Air Refreshers",
      "Cleaning Supply",
      "Laundry",
      "Tissues & Paper Towel",
    ],
    'Pharmacy' :[
      "First Aid",
      "Cold & Cough",
      "Allergy Medication",
      "Vitamins & Supplements",
      "Allergies",
    ],
  },
}


def itemlist(request):
    template = loader.get_template('itemlist.html')
    context = Context({
      'category' : json.dumps(category),
      'labels' : json.dumps(labels)
      })
    return HttpResponse(template.render(context))

def getItemsFromBackend(startId, num):
  items = []
  for it in Item.objects.all()[startId : startId + num]:
    items.append({'id': it.id, 'name' : it.name, 'price' : it.price, 'category' : it.category})
  return items

@csrf_exempt
def getItems(request):
  if request.method == 'POST':
    startId = int(request.POST['startId'])
    num = int(request.POST['num'])
    return HttpResponse(json.dumps(getItemsFromBackend(startId, num)))
  else:
    return HttpResponse('error')


