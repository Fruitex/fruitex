from custom_manage import *

def execute_from_command_line(argv):
  def _arg(i):
    if len(argv) > i:
      return argv[i]
    return ''

  if _arg(1) == 'clear':
    clearItems(_arg(2))
  elif _arg(1) == 'load':
    loadItem(_arg(2), _arg(3))
  elif _arg(1) == 'add':
    addItems(_arg(2), _arg(3))
  elif _arg(1) == 'check_item':
    addItems(_arg(2), _arg(3), check_only=True)
  elif _arg(1) == 'cate':
    fetchCategory(_arg(2))
  elif _arg(1) == 'order':
    showOrders()
  elif _arg(1) == 'tax':
    showTax()
  elif _arg(1) == 'fix':
    fixTypo()
  elif _arg(1) == 'init_sold_num':
    initItemSoldNumber()
  elif _arg(1) == 'v':
    showVersion()
  elif _arg(1) == 'clear_pending_orders':
    clearOrder()
  elif _arg(1) == 'test_mail':
    testMail()
  elif _arg(1) == 'check_img':
    checkImg(_arg(2))
  elif _arg(1) == 'on_sale':
    onSale(_arg(2), _arg(3), True)
  elif _arg(1) == 'off_sale':
    onSale(_arg(2), _arg(3), False)
  elif _arg(1) == 'add_coupon':
    addCoupon(int(_arg(2)), float(_arg(3)))
  elif _arg(1) == 'clear_used_coupon':
    clearUserCoupon()
  elif _arg(1) == 'create_store':
    createStore(_arg(2), _arg(3))
  else:
    return False
  return True
