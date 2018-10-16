# PageRank

PageRank is a popular method for measuring the popularity of websites. We get the PageRank of a website by counting how many websites refrence this page.

In this work we use the [enwiki dataset](https://dumps.wikimedia.org/backup-index.html), and we need to count the PageRank value of 100M pages. Due to the limit of equipment, many methods are inpracticable. I use iterative method at last. Code is available in PageRank.py and I show the first 1000 lines of result in out.txt. I use some txt files to store the intermediate results because I haven't solve the problem about the very slow speed of reading the original xml file. If you have better idea of how to read data, please contact me.