gitimport re
import time
import scipy.sparse as sparse
import numpy as np

num = 0
stringtoint = {}
inttostring = {}
order = {}
keydict = {}
row = []
col = []
data = []
v = np.array((0))

process_data_time = 0
graph_link_time = 0
iter_time = 0

pattern1 = re.compile('(\s)*<title>(.*)</title>')
pattern2 = re.compile('(\s)*<redirect title=\"[^\"]*\"\s?/>')
pattern3 = re.compile('\[\[(.*?)\]\]')
pattern4 = re.compile('(.*)\|(.*)')

def process_data():
    global num
    global stringtoint, inttostring
    global order, keydict
    file = open('./test.xml', 'r')
    flag = 0
    count = 0
    key = 0
    link = []
    while True:
        line = file.readline()
        if not line:
            break
        
        match = re.match(pattern1, line)
        if match:
            if flag == 1:
                order[title] = count
                keydict[title] = link
                count += 1
                if count % 10000 == 0:
                    print(count)
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

    num = len(keydict)

def graph_link():
    global num
    global inttostring
    global keydict
    global row, col, data
    for key in keydict:
        tmplink = keydict[key]
        colnum = order[key]
        linknum = 0
        for ref in tmplink:
            if inttostring[ref] in keydict.keys():
                col.append(colnum)
                row.append(order[inttostring[ref]])
                linknum += 1
        if linknum == 0:
            linknum = num
            for i in range(linknum):
                col.append(colnum)
                row.append(i)
        avgp = 1 / linknum
        for i in range(linknum):
            data.append(avgp)

def iterlist():
    global row, col, data
    global v
    alpha = 0.85
    matrix = sparse.coo_matrix((data, (row, col)), shape = (num, num))
    v = np.array([1 / num for i in range(num)])
    relink = np.array([1 / num for i in range(num)])

    while (sum(abs(v - (alpha * matrix * v + (1 - alpha) * relink))) > 0.0001):
        v = alpha * matrix * v + (1 - alpha) * relink

def write_file():
    global process_data_time, graph_link_time, iter_time
    global keydict
    global v
    time_start = time.time()

    f = open('./out.txt', 'w')
    for key, pr in zip(keydict, v):
        f.write('Title: ' + key + ' * PageRank: ' + str(pr) + '\n') 

    time_end = time.time()
    write_file_time = time_end - time_start

    f.write('\n')
    f.write('process data takes %ds\n' % process_data_time)
    f.write('graph link takes %ds\n' % graph_link_time)
    f.write('iter takes %ds\n' % iter_time)
    f.write('write file takes %ds\n' % write_file_time)
    f.close()

if __name__ == '__main__':
    time_start = time.time()
    process_data()
    time_end = time.time()
    process_data_time = time_end - time_start

    time_start = time.time()
    graph_link()
    time_end = time.time()
    graph_link_time = time_end - time_start

    time_start = time.time()
    iterlist()
    time_end = time.time()
    iter_time = time_end - time_start

    write_file()





        

