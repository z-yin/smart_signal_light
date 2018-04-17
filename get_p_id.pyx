import datetime as dt
import adapt_func

cpdef get_p_id_set(a, day, int h, keys):
    # global tm3
    # global cntt
    # cntt += 1
    # st = dt.datetime.now()
    cdef int current_time = keys[0]
    cdef int j = keys[1]
    cdef int standard_time
    cdef int std_time1
    cdef int std_time2
    cdef int key1[3]
    cdef int key2[3]
    cdef int key3[3]

    standard_time = adapt_func.SysStartEndTime.start_dic[day] + current_time
    std_time1 = standard_time - 1
    std_time2 = standard_time + 1

    key1 = {std_time1, h, j}
    key2 = {standard_time, h, j}
    key3 = {std_time2, h, j}

    key1 = tuple(key1)
    key2 = tuple(key2)
    key3 = tuple(key3)

    vehicles = []
    if key1 in a.map_table:
        vehicles.extend(a.map_table[key1])
    if key2 in a.map_table:
        vehicles.extend(a.map_table[key2])
    if key3 in a.map_table:
        vehicles.extend(a.map_table[key3])

    # print(dt.datetime.now() - st)
    # tm3 += dt.datetime.now() - st

    if any(vehicles):
        return (current_time, j), set(vehicles)
    else:
        return None, None