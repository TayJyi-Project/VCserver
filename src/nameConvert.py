import os
import re
items = os.listdir()
for item in items:
  if re.search('.*\d+.*\.wav', item):
    num = int(re.findall('\d+', item)[0])
    os.rename(item, 'chunk{0}.wav'.format(str(num).zfill(3)))
