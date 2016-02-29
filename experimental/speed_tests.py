import csv
import timeit

def not_join(size = (40,40)):
    blank_dict = {}
    output = ''
    for y in range(size[1]):
        if y>0:
            output += '\n'
        for x in range(size[0]):
            output += blank_dict.get((x,y), '.')
    return output

def using_join_poorly(size = (40,40)):
    blank_dict = {}
    output = ''
    for y in range(size[1]):
        if y>0:
            output += '\n'
        line = ''.join([blank_dict.get((x, y), '.') for x in range(size[0])])
        output += line
    return output

def join_all_at_once(size = (40,40)):
    blank_dict = {}
    output_list = []
    for y in range(size[1]):
        if y > 0:
            output_list.append('\n')
        output_list.extend([blank_dict.get((x, y), '.') for x in range(size[0])])
    return ''.join(output_list)

if not_join() == using_join_poorly() == join_all_at_once():
    print('They Match')
else:
    print(not_join(size=(10,10)))
    print(using_join_poorly(size=(10,10)))
    print(join_all_at_once(size=(10,10)))

data_point_1 = timeit.timeit('not_join()', number=10000, globals=globals())
print(data_point_1)
data_point_2 = timeit.timeit('using_join_poorly()', number=10000, globals=globals())
print(data_point_2)
data_point_3 = timeit.timeit('join_all_at_once()', number=10000, globals=globals())
print(data_point_3)

with open('speed_test_log.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([data_point_1, data_point_2, data_point_3])
    print('run times logged')