import datetime as dt


with open('trail_info.txt', 'r') as file:
    info_list = []
    tm = []
    file_list = file.readlines()
    for i in range(1, len(file_list)):
        info_list.append(file_list[i].split(','))
        info_list[-1].pop()
        info_list[-1][1] = dt.datetime.fromtimestamp(int(info_list[-1][1]))
        info_list[-1][2] = round(float(info_list[-1][2]))
        info_list[-1][3] = round(float(info_list[-1][3]))
        info_list[-1][4] = float(info_list[-1][4])
        info_list[-1][5] = int(info_list[-1][5])
        tm.append(info_list[-1][1])
for i in info_list:
    print i

# with open('time_stamp.txt', 'w') as f:
#     for i in info_list:
#         f.write(i)

# last_day = 4
# day_tm = [[]]
# for i in tm:
#     if i.day == last_day:
#         day_tm[-1].append(str(i))
#     else:
#         last_day = i.day
#         day_tm.append([])
#         day_tm[-1].append(str(i))
# day_min = []
# day_max = []
# for i in day_tm:
#     day_min.append(min(i))
#     day_max.append(max(i))
# for i in day_min:
#     print i
# print '---------------------------------------'
# for i in day_max:
#     print i
