#!/usr/bin/python
import sys,os

def _getAllCsvFiles(folder):
  res = []
  for f in os.listdir(folder):
    if f.endswith('.csv'):
      res.append(folder + f)
    elif os.path.isdir(folder + f):
      res.extend(_getAllCsvFiles(folder + f + os.path.sep))
  return res

if __name__=='__main__':
  for f in _getAllCsvFiles(sys.argv[1]):
    s=file(f).read().replace('\r\n', '\n').replace('\r', '\n')
    out=file(f, 'wb')
    out.write(s)
    out.close()
