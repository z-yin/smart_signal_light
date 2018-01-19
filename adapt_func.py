import datetime as dt
import sys


# s = [[]]
phase_diff = [0, 0, 0, 0, 0, 0, 0]


p1 = [[0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
      [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
p2 = [[0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
      [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
      [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
p3 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
p4 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1]]
p5 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
p6 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
      [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
p7 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
      [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
      [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

p = [p1, p2, p3, p4, p5, p6, p7]


class SysStartEndTime:
    SYSTEMTIME = {}
    start_dic = {(5, 4): 1493852410,    # 2017-05-04 07:00:10
                 (5, 5): 1493938820,    # 2017-05-05 07:00:20
                 (5, 8): 1494198023,    # 2017-05-08 07:00:23
                 (5, 9): 1494284412,    # 2017-05-09 07:00:12
                 (5, 10): 1494370814,   # 2017-05-10 07:00:14
                 (5, 11): 1494457213,   # 2017-05-11 07:00:13
                 (5, 12): 1494543607,   # 2017-05-12 07:00:07
                 (5, 15): 1494802815,   # 2017-05-15 07:00:15
                 (5, 16): 1494889214,   # 2017-05-16 07:00:14
                 (5, 17): 1494975615}   # 2017-05-17 07:00:15

    def __init__(self):
        pass


# compute the start time of a phase
# @jit
def get_phase_start(current_time, h, i, t, T):
    phase_start = current_time - ((current_time - phase_diff[h]) % T)
    for x in range(i):
        phase_start += t[x]
    return phase_start


def get_phase_end(start_time, i, t):
    return start_time + t[i]


def get_p_num(a, day, current_time, h, j):
    standard_time = SysStartEndTime.start_dic[day] + current_time
    std_time1 = dt.datetime.fromtimestamp(standard_time - 1)
    std_time2 = dt.datetime.fromtimestamp(standard_time)
    std_time3 = dt.datetime.fromtimestamp(standard_time + 1)
    key1 = (std_time1, h, j)
    key2 = (std_time2, h, j)
    key3 = (std_time3, h, j)
    vehicle_num = 0
    if key1 in a.map_table:
        vehicle_num += a.get_vehicles_number(key1)
    if key2 in a.map_table:
        vehicle_num += a.get_vehicles_number(key2)
    if key3 in a.map_table:
        vehicle_num += a.get_vehicles_number(key3)
    return vehicle_num


def get_p_id_set(a, day, current_time, h, j):
    standard_time = SysStartEndTime.start_dic[day] + current_time
    std_time1 = dt.datetime.fromtimestamp(standard_time - 1)
    std_time2 = dt.datetime.fromtimestamp(standard_time)
    std_time3 = dt.datetime.fromtimestamp(standard_time + 1)
    key1 = (std_time1, h, j)
    key2 = (std_time2, h, j)
    key3 = (std_time3, h, j)
    vehicle_set = []
    if key1 in a.map_table:
        vehicle_set.extend(a.map_table[key1])
    if key2 in a.map_table:
        vehicle_set.extend(a.map_table[key2])
    if key3 in a.map_table:
        vehicle_set.extend(a.map_table[key3])
    return set(vehicle_set)


# compute q[]
def get_enter_dic(enter_dic, start_time, end_time, a, day, h):
    global tm_of_get_q
    begin_tm = dt.datetime.now()

    enter_dic[start_time] = set()
    for j in range(12):
        enter_dic[start_time] |= get_p_id_set(a, day, start_time, h, j)

    for tm in range(start_time + 3, end_time + 1, 3):
        enter_dic[tm] = set()
        for j in range(12):
            enter_dic[tm] |= get_p_id_set(a, day, tm, h, j)
        enter_dic[tm] |= enter_dic[tm - 3]

    end_tm = dt.datetime.now()

    tm_of_get_q += end_tm - begin_tm


# compute the number of retention vehicles before a phase
def retention(start_time, a, day, h, j):
    return get_p_num(a, day, start_time, h, j)


# compute number of vehicles entering into a intersection from the start of a phase to the current time
def num_entering(enter_dic, start_time, current_time):
    print(current_time)
    print(enter_dic)

    if current_time in enter_dic:
        return len(enter_dic[current_time] - enter_dic[start_time])
    elif current_time - 1 in enter_dic:
        return len(enter_dic[current_time - 1] - enter_dic[start_time])
    elif current_time - 2 in enter_dic:
        return len(enter_dic[current_time - 2] - enter_dic[start_time])
    else:
        sys.exit('error in num_entering')


# compute number of vehicles flowing out from a lane
def flow_out(h, j, i, t):
    # return s[h][j] * psom.p[h][i][j] * t[i]
    return 0.05 * p[h][i][j] * t[i]


# compute the delay in a second
# @jit
def delay_per_second(enter_dic, start_time, a, day, current_time, h, j, i, t):
    temp = retention(start_time, a, day, h, j) + \
           num_entering(enter_dic, start_time, current_time) + flow_out(h, j, i, t)
    if temp > 0:
        return temp
    else:
        return 0

tm_of_get_q = dt.datetime.now()


# compute the total delay in all intersections
# @jit
def delay(a, t):
    T = t[0] + t[1] + t[2] + t[3] + t[4]
    delay_sum = 0
    last_i = 0
    delay_phase = 0
    enter_dic = {}
    for day in SysStartEndTime.start_dic:
        for h in range(7):
            for j in range(12):
                st_tm = dt.datetime.now()
                global tm_of_get_q
                tm_of_get_q = dt.datetime.now() - dt.datetime.now()

                start_time = 0
                end_time = 0

                for current_time in range(1, 7200, 3):

                    rele_time = (current_time - phase_diff[h]) % T
                    if rele_time < t[0]:
                        i = 0
                    elif rele_time < (t[0] + t[1]):
                        i = 1
                    elif rele_time < (t[0] + t[1] + t[2]):
                        i = 2
                    elif rele_time < (t[0] + t[1] + t[2] + t[3]):
                        i = 3
                    else:
                        i = 4

                    if current_time == 1:
                        start_time = get_phase_start(current_time, h, i, t, T)
                        end_time = get_phase_end(start_time, i, t)
                        enter_dic.clear()
                        get_enter_dic(enter_dic, start_time, end_time, a, day, h)

                    if i != last_i:
                        qt = num_entering(enter_dic, start_time, current_time - 3) * t[last_i]
                        if qt > 0:
                            delay_phase /= qt
                        else:
                            delay_phase = 0
                        delay_sum += delay_phase
                        delay_phase = 0
                        last_i = i

                        start_time = get_phase_start(current_time, h, i, t, T)
                        end_time = get_phase_end(start_time, i, t)
                        enter_dic.clear()
                        get_enter_dic(enter_dic, start_time, end_time, a, day, h)

                    delay_phase += delay_per_second(start_time, end_time, a, day, current_time, h, j, i, t)

                end_tm = dt. datetime.now()

                spend_tm = end_tm - st_tm
                print(tm_of_get_q, spend_tm)
                print()
