import re
import time


file = open('../../enwiki-20180920-pages-articles-multistream.xml', 'r')
f = open('./out.txt', 'w')
flag = 0
count = 0
key = 0
link = []
stringtoint = {}
inttostring = {}
keydict = {}
numcount = {}

pattern1 = re.compile('(\s)*<title>(.*)</title>')
pattern2 = re.compile('(\s)*<redirect title=\"[^\"]*\"\s?/>')
pattern3 = re.compile('\[\[(.*?)\]\]')
pattern4 = re.compile('(.*)\|(.*)')

time_start = time.time()

while True:
    line = file.readline()
    if not line:
        break
    
    match = re.match(pattern1, line)
    if match:
        if flag == 1:
            count += 1
            if count % 10000 == 0:
                print(count)
            keydict[title] = link
            numcount[title] = 0
        title = match.group(2)
        flag = 1
        link = []
    
    if count == 1000000:
        break
    
    match = re.match(pattern2, line)
    if match:
        flag = 0
    
    if flag == 1:
        match = re.findall(pattern3, line)
        for item in match:
            if item.startswith('File:'):
                continue
            tmp = re.match(pattern4, item)
            if tmp:
                item = tmp.group(1)
            if item not in stringtoint.keys():
                stringtoint[item] = key
                inttostring[key] = item
                tmp = key
                key += 1
            else:
                tmp = stringtoint[item]
            link.append(tmp)

time_end = time.time()
print(time_end - time_start)

time_start = time.time()

for key in keydict:
    tmplink = keydict[key]
    for ref in tmplink:
        if ref in numcount.keys():
            numcount[ref] += 1

time_end = time.time()
print(time_end - time_start)

time_start = time.time()
for name in numcount:
    f.write(name + ' ' + str(numcount[name]) + '\n')

time_end = time.time()
print(time_end - time_start)



        

