import re
import argparse
import time
import numpy as np

num = 0
stringtoint = {}
inttostring = {}
order = {}
reorder = {}
keydict = {}
reflink = {}
refnum = []
final = {}
v = []

pattern1 = re.compile('(\s)*<title>(.*)</title>')
pattern2 = re.compile('(\s)*<redirect title=\"[^\"]*\"\s?/>')
pattern3 = re.compile('\[\[(.*?)\]\]')
pattern4 = re.compile('(.*)\|(.*)')

def process_data(root):
    global stringtoint, inttostring, order, reorder, keydict

    file = open(root, 'r')
    flag = False
    count = 0
    key = 0
    link = []
    
    while True:
        line = file.readline()
        if not line:
            break
        
        match = re.match(pattern1, line)
        if match:
            if flag == True:
                order[title] = count
                reorder[count] = title
                keydict[title] = link
                reflink[title] = []
                count += 1
                if count % 10000 == 0:
                    print(count)
            title = match.group(2)
            flag = True
            link = []
        
        if count == num:
            break
        
        match = re.match(pattern2, line)
        if match:
            flag = False
        
        if flag == True:
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

def graph_link():
    global inttostring, keydict, order, reflink, refnum

    print('start linking')
    for key in keydict:
        number = order[key]
        refnum[number] = 0
        tmplink = keydict[key]
        for ref in tmplink:
            name = inttostring[ref]
            if name in keydict.keys():
                refnum[number] += 1
                reflink[name].append(number)
    print('end linking')

def save_data():
    global inttostring, reflink, refnum, reorder
    
    file = open('./data/i2s.txt', 'w')
    for key in inttostring:
        file.write(str(key) + '\n' + inttostring[key] + '\n')
    file.close()

    file = open('./data/ref.txt', 'w')
    for key in reflink:
        link = reflink[key]
        file.write(key + '\n' + str(len(link)) + '\n')
        for ref in link:
            file.write(str(ref) + '\n')
    file.close()

    file = open('./data/refnum.txt', 'w')
    for key in refnum:
        file.write(str(key) + '\n' + str(refnum[key]) + '\n')
    file.close()

    file = open('./data/ro.txt', 'w')
    for key in reorder:
        file.write(str(key) + '\n' + reorder[key] + '\n')
    file.close()

def load_data():
    global inttostring, reflink, refnum, reorder, num

    file = open('./data/i2s.txt', 'r')
    while True:
        linenum = file.readline()
        if not linenum:
            break
        number = int(linenum)
        linestr = file.readline()
        inttostring[number] = linestr
    file.close()
    print('load i2s done')

    file = open('./data/ref.txt', 'r')
    while True:
        linename = file.readline()
        if not linename:
            break
        reflink[linename] = []
        linenum = file.readline()
        number = int(linenum)
        for i in range(number):
            refnum = int(file.readline())
            reflink[linename].append(refnum)
    file.close()
    print('load reflink done')
 
    refnum = [0 for i in range (num)]
    file = open('./data/refnum.txt', 'r')
    while True:
        lineord = file.readline()
        if not lineord:
            break
        index = int(lineord)
        linenum = file.readline()
        number = int(linenum)
        refnum[index] = number
    file.close()
    print('load refnum done')

    file = open('./data/ro.txt', 'r')
    while True:
        linenum = file.readline()
        if not linenum:
            break
        number = int(linenum)
        linestr = file.readline()
        reorder[number] = linestr
    file.close() 
    print('load reorder done')
    
def iterlist():
    global v, num, final, inttostring, reflink, reorder

    print('start iter')
    iternum = 100
    repage = 0.15 / num
    v = [1 / num for i in range(num)]
    for i in range(iternum):
        for j in range(num):
            rank = 0
            name = reorder[j]
            for ref in reflink[name]:
                rank += 0.85 * v[ref] / refnum[ref]
            rank += repage
            v[j] = rank
        print('iteration' + str(i) + ' done')
    print('end iter')
    
    print('start sorting')
    for key, pr in zip(reorder, v):
        final[reorder[key]] = pr
    final = sorted(final.items(), key = lambda x : x[1], reverse = True)
    print('end sorting')

def write_file():
    global final

    f = open('./out.txt', 'w')
    for pr in final:
        f.write('Title: ' + pr[0] + ' * PageRank: ' + str(pr[1]) + '\n') 
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--root', help ='data root')
    parser.add_argument('-l', '--load', action = 'store_true', required = True, help = 'load or not')
    parser.add_argument('-n', '--num', default = '1000000', help = 'title num')

    args = parser.parse_args()
    root = args.root
    load = args.load
    num = int(args.num)

    if load:
        time_start = time.time()
        load_data()
        time_end = time.time()
        load_data_time = time_end - time_start
        print('load data takes %ds' % load_data_time)
    else:
        time_start = time.time()
        process_data(root)
        time_end = time.time()
        process_data_time = time_end - time_start
        print('process data takes %ds' % process_data_time)

        time_start = time.time()
        graph_link()
        time_end = time.time()
        graph_link_time = time_end - time_start
        print('graph link takes %ds' % graph_link_time)

        time_start = time.time()
        save_data()
        time_end = time.time()
        save_data_time = time_end - time_start
        print('save data takes %ds' % save_data_time)
    
    time_start = time.time()
    iterlist()
    time_end = time.time()
    iter_time = time_end - time_start
    print('iteration takes %ds' % iter_time)

    time_start = time.time()
    write_file()
    time_end = time.time()
    write_file_time = time_end - time_start
    print('write file takes %ds' % write_file_time)
    
    




        

