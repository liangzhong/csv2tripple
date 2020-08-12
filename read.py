import csv

path = '/Users/liangzhong/projects/csv2tripple'
file = path + '/' + 'a.csv'


# with open(file) as f:
#     head_1 = f.readline()
#     # print(head_1)
#     h1 = head_1.split(",")
#     line_1 = f.readline()
#     l1 = line_1.split(",")


# for h1a in h1:
#     print(h1a)

# for l1a in l1:
#     print(l1a)


with open(file, mode='r',encoding='utf-8') as file_reader:
    # entries_list = [line.strip().split(',') for line in lines]
    lines = csv.reader(file_reader, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    # print(type(lines))
    # head_1 = lines.readline()
    # line_1 = lines.readline()
    # print(type(head_1))
    h1 = next(lines)
    l1 = next(lines)

    for x, y in zip(h1, l1):
        print(x + '\t||\t' + y)

print ("Done!")            