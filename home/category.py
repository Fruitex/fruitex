from home.models import Item


def cateForSobeys():
    invalidData = ['Goceries']
    category = {}
    seen = set()
    for it in Item.objects.filter(store__name='sobeys'):
      c = it.category
      if c in seen:
        continue
      else:
        seen.add(c)
      c = c.split('->')
      assert len(c) >= 2, 'incalid category format: %s' % c
      if c[0] in invalidData:
        continue
      if c[0] not in category:
        category[c[0]]={}
      if c[1] not in category[c[0]]:
        category[c[0]][c[1]]=[]
      if len(c) == 3:
        category[c[0]][c[1]].append(c[2])
    return category


def getTextBookTopCate(c):
    if ord(c[0].upper()) <= ord('E'):
      return 'Department A-E'
    elif ord(c[0].upper()) <= ord('J'):
      return 'Department F-J'
    elif ord(c[0].upper()) <= ord('O'):
      return 'Department K-O'
    else:
      return 'Department P-Z'

def cateForBookStore():
    category = {}
    seen = set()
    for it in Item.objects.filter(store__name='bookstore'):
      c = it.category
      if c in seen:
        continue
      else:
        seen.add(c)
      c = c.split('->')
      assert len(c) >= 2, 'incalid category format: %s' % c
      if c[0] == 'Textbook':
        c[0] = getTextBookTopCate(c[1])
      if c[0] not in category:
        category[c[0]]={}
      if c[1] not in category[c[0]]:
        category[c[0]][c[1]]=[]
      if len(c) == 3:
        category[c[0]][c[1]].append(c[2])
    return category

category = {
    'sobeys' : cateForSobeys(),
    'bookstore' : cateForBookStore(),
}
