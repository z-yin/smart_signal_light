# -*- coding: utf-8 -*-


import datetime as dt
import itertools


# s = [[]]
phase_diff = [0, 0, 0, 0, 0, 0, 0]
T = [200, 200, 200, 200, 200, 200, 200]

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
cpdef get_phase_start(int current_time, int h, int i, t):
    # global tm1
    # st = dt.datetime.now()
    cdef int phase_start
    cdef int phase_end
    T_ = sum(t)
    phase_start = current_time - ((current_time - phase_diff[h]) % T_)
    for x in range(i):
        phase_start += t[x]

    # phase_start += np.sum(t[:i])
    phase_end = phase_start + t[i]

    # tm1 += dt.datetime.now() - st

    return phase_start, phase_end


cpdef get_p_num(a, day, int current_time, int h, int j):
    # global tm2
    # st = dt.datetime.now()
    cdef int standard_time
    cdef int std_time1
    cdef int std_time2

    standard_time = SysStartEndTime.start_dic[day] + current_time
    std_time1 = standard_time - 1
    std_time2 = standard_time + 1

    key1 = (std_time1, h, j)
    key2 = (standard_time, h, j)
    key3 = (std_time2, h, j)

    vehicle_num = 0
    if key1 in a.map_table:
        vehicle_num += a.get_vehicles_number(key1)
    if key2 in a.map_table:
        vehicle_num += a.get_vehicles_number(key2)
    if key3 in a.map_table:
        vehicle_num += a.get_vehicles_number(key3)

    # tm2 += dt.datetime.now() - st
    return vehicle_num


# compute the number of retention vehicles before a phase
cpdef int retention(int start_time, a, day, int h, int j):
    return get_p_num(a, day, start_time, h, j)


# compute number of vehicles entering into a intersection from the start of a phase to the current time
cpdef int num_entering(a, day, int start_time, int current_time, int h):
    # global tm5
    # global tm6
    # global cntt2
    # cntt2 += 1
    # st1 = dt.datetime.now()
    standard_time = SysStartEndTime.start_dic[day]
    start_time_1 = start_time + standard_time
    current_time_1 = current_time + standard_time

    key = [(x1, h, x2) for x1 in range(start_time_1, current_time_1) for x2 in range(12)]
    _1 = [a.map_table[x] for x in key if x in a.map_table]
    _1 = itertools.chain(*_1)

    key_ = [(st, h, j) for st in [start_time_1 - 1, start_time_1, start_time_1 + 1] for j in range(12)]
    _2 = [a.map_table[x] for x in key_ if x in a.map_table]
    _2 = itertools.chain(*_2)

    # tm5 += dt.datetime.now() - st1
    # st2 = dt.datetime.now()

    if any(_1):
        # print "_1_________"
        q_sum = len(set(_1))
    else:
        q_sum = 0

    if any(_2):
        # print "_2_________"
        start_sum = len(set(_2))
    else:
        start_sum = 0

    # tm6 += dt.datetime.now() - st2
    # print "q_sum - start_sum : " + str(q_sum - start_sum)
    return q_sum - start_sum


# compute number of vehicles flowing out from a lane
cpdef int flow_out(int h, int j, int i, t):
    # return s[h][j] * psom.p[h][i][j] * t[i]
    return 0.3 * p[h][i][j] * t[i]


# compute the delay in a second
# @jit
cpdef float delay_per_second(start_time, a, day, int current_time, int h, int j, int i, t):
    temp = retention(start_time, a, day, h, j) + \
           num_entering(a, day, start_time, current_time, h) - flow_out(h, j, i, t)
    return max(temp, 0)


# compute the total delay in all intersections
# @jit
def delay(a, t):
    T_sum = sum(t)
    cn1 = cn2 = 0
    delay_time = dt.datetime.now()
    delay_sum = 0
    last_i = 0
    delay_phase = 0
    for day in [(5, 4)]:  # SysStartEndTime.start_dic:
        for h in range(4, 5):
            for j in range(12):
                st_tm = dt.datetime.now()
                start_time = 0
                end_time = 0
                for current_time in range(1, 1000, 3):
                    rele_time = (current_time - phase_diff[h]) % T_sum

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

                    if current_time == 1 :
                        start_time, end_time = get_phase_start(current_time, h, i, t)

                    if i != last_i:
                        cn1 += 1
                        qt = num_entering(a, day, start_time, end_time, h) * t[last_i]
                        if qt > 0:
                            cn2 += 1
                            delay_phase /= qt
                        else:
                            delay_phase = 0
                        delay_sum += delay_phase
                        delay_phase = 0
                        last_i = i
                        start_time, end_time = get_phase_start(current_time, h, i, t)

                    delay_phase += delay_per_second(start_time, a, day, current_time, h, j, i, t)

    del_tm = (dt.datetime.now() - delay_time).total_seconds()

    return delay_sum
