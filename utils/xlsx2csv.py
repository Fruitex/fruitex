#!/usr/bin/python
import sys
from openpyxl.reader.excel import load_workbook
import csv

def load(fname):
    wb=load_workbook(filename=fname)
    sheet = wb.worksheets[0]
    csv_file='%s.csv' % fname.split('.')[0]
    print 'Creating %s' % csv_file
    out = csv.writer(file(csv_file, 'wb'))
    for row in sheet.rows:
        values=[]
        for cell in row:
            value=cell.value
            if value is None:
                value=''
            if not isinstance(value, unicode):
                value=unicode(value)
            value=value.encode('utf8')
            values.append(value)
        out.writerow(values)

import os
def rload(path):
  for fname in os.listdir(path): 
    if fname.endswith('.xlsx'):
      load(path + fname)
    else:
      if os.path.isdir(path + fname):
        rload(path + fname + os.path.sep)

if __name__=='__main__':
  path = sys.argv[1]
  if path[-1] != os.path.sep:
    path += os.path.sep
  load(path)
