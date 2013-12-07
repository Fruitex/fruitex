from management.shop import item

def execute_from_command_line(argv):
  def _arg(i):
    if len(argv) > i:
      return argv[i]
    return ''

  if _arg(1) == 'shop_import_csv':
    item.import_from_csv(_arg(2),_arg(3))
  else:
    return False
  return True
