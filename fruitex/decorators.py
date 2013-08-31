from django.shortcuts import redirect

class admin(object):
  def __init__(self, f):
    self.f = f
  def __call__(self, *args):
    try:
      if args[0].user.is_authenticated():
        return apply(self.f, args)
    except Exception as e:
      print e
    return redirect('/admin/')
