import os
import re
items = os.listdir()
for item in items:
  if re.search('.*\d+.*\.\w+', item):
    num = int(re.findall('\d+', item)[0])
    ext = re.findall('\.[a-zA-Z]+', item)[0]
    os.rename(item, 'chunk{0}{1}'.format(str(num).zfill(3), ext))
