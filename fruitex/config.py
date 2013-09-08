import platform
if platform.uname()[1] == 'user-PC':
  BASE_DIR = r'C:\Users\user\Dropbox\fruitex\\'
elif platform.uname()[1] == 'XINYUANs-MacBook-Air.local':
  BASE_DIR = r'/Users/Sue/Documents/workspace/fruitex'
else:
  BASE_DIR = '/fruitex/'

DOMAIN = 'fruitex.ca' #'108.171.244.148'

#  Set this to false to switch to prod.
DEBUG = False
