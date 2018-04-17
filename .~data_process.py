# -*- coding: utf-8 -*-
"""
Created on 
"""
import numpy as np
import datetime as dt
import math
import time


class Position:
    EAST = 1
    WEST = -1
    NORTH = 2
    SOUTH = -2
    CENTER = 0
    POS_DIC = {EAST: np.array([1, 0]),
               WEST: np.array([-1, 0]),
               NORTH: np.array([0, 1]),
               SOUTH: np.array([0, -1]),
               CENTER: np.array([0, 0])}

    LANE_DIC = {(EAST, SOUTH): 0,
                (EAST, WEST): 1,
                (EAST, CENTER): 1,
                (EAST, EAST): 1,
                (EAST, NORTH): 2,

                (WEST, NORTH): 3,
                (WEST, EAST): 4,
                (WEST, CENTER): 4,
                (WEST, WEST): 4,
                (WEST, SOUTH): 5,

                (NORTH, EAST): 6,
                (NORTH, SOUTH): 7,
                (NORTH, CENTER): 7,
                (NORTH, NORTH): 7,
                (NORTH, WEST): 8,

                (SOUTH, WEST): 9,
                (SOUTH, NORTH): 10,
                (SOUTH, CENTER): 10,
                (SOUTH, SOUTH): 10,
                (SOUTH, EAST): 11,

                (CENTER, EAST): 12,
                (CENTER, WEST): 13,
                (CENTER, NORTH): 14,
                (CENTER, SOUTH): 15,
                (CENTER, CENTER): -1}

    def __init__(self):
        pass


# Single info of a vehicle at a certain time
class Info:
    id = ''
    time = 0
    x_coordinate = 0
    y_coordinate = 0
    speed = 0
    category = 0
    intr_sec = 0    # The intersection of this trail info
    pos = 0
    info_dir = 0

    def __init__(self, from_info):
        self.id = from_info[0]
        self.time = from_info[1]
        self.x_coordinate = from_info[2]
        self.y_coordinate = from_info[3]
        self.speed = from_info[4]
        self.category = from_info[5]
        self.intr_sec = InterSection().find_nearest_inter(self)
        self.pos = self.get_pos()

    def get_pos(self):
        self.info_dir = np.array([self.x_coordinate - InterSection.dict_location[self.intr_sec][0],
                                  self.y_coordinate - InterSection.dict_location[self.intr_sec][1]])
        if self.get_info_dir_length() < 5000:
            return Position.CENTER
        elif Direction.get_angle(self.info_dir, Position.POS_DIC[Position.EAST]) > math.cos(math.pi/4):
            return Position.EAST
        elif Direction.get_angle(self.info_dir, Position.POS_DIC[Position.WEST]) > math.cos(math.pi/4):
            return Position.WEST
        elif Direction.get_angle(self.info_dir, Position.POS_DIC[Position.NORTH]) > math.cos(math.pi/4):
            return Position.NORTH
        elif Direction.get_angle(self.info_dir, Position.POS_DIC[Position.SOUTH]) > math.cos(math.pi/4):
            return Position.SOUTH
        else:
            return Position.CENTER

    def get_info_dir_length(self):
        return self.info_dir.dot(self.info_dir)


# Vehicles info linked together by time sequence
class TimeSeries:
    InfoSeriesByTime = []

    def __init__(self, info):
        self.InfoSeriesByTime.append(info)

    def sort_by_time(self):
        sorted(self.InfoSeriesByTime, key=lambda info: info.time)


class Direction:
    def __init__(self):
        pass

    def get_direction(self, intr_sec, info):
        in_to_intrsec = np.array([InterSection().dict_location[intr_sec[0]][0] - intr_sec[1][0],
                                  InterSection().dict_location[intr_sec[0]][1] - intr_sec[1][1]])
        out_from_intrsec = np.array([info.x_coordinate - InterSection().dict_location[intr_sec[0]][0],
                                     info.y_coordinate - InterSection().dict_location[intr_sec[0]][1]])
        direction = np.cross(out_from_intrsec, in_to_intrsec)
        if math.cos(math.pi*0.86) < self.get_angle(in_to_intrsec, out_from_intrsec) < math.cos(math.pi*0.14):
            if direction > 0:
                return 1
            elif direction < 0:
                return -1
        else:
            return 0

    @staticmethod
    def get_angle(into_intersection, out_from_intersection):
        norm_of_into = math.sqrt(np.dot(into_intersection, into_intersection))
        norm_of_out = math.sqrt(np.dot(out_from_intersection, out_from_intersection))
        dot_of_two = np.dot(into_intersection, out_from_intersection)
        if norm_of_out == 0 or norm_of_into == 0:
            return 0
        else:
            angle = dot_of_two/(norm_of_into*norm_of_out)
            return angle


# Single vehicle info
class Vehicle:
    id = ''
    info = []  # Info of a vehicle at a certain time, every element is a 'Info' class
    trail_key = []
    tr_info = {}
    intersec_sequence = {}   # The intersections sequence that a vehicle passed through ordered by time
    lane = {}
    SYSERROR = 10

    def __init__(self, from_info):
        self.id = from_info.id
        self.info = []
        self.info.append(from_info)
        self.trail_key = []
        self.tr_info = {}
        self.intersec_sequence = {}
        self.lane = {}

    def add_info(self, from_info):
        self.info.append(from_info)

    def set_trail_key(self, idx):
        tm = time.mktime(self.info[idx].time.timetuple())
        tm_ex = time.mktime(self.info[idx - 1].time.timetuple())
        if abs(tm - tm_ex) < self.SYSERROR:
            self.trail_key[-1][1] = self.info[idx].time
            self.trail_key[-1][-1] = idx
        else:
            self.trail_key.append([self.info[idx].time, self.info[idx].time, idx, idx])

    def sort_info(self):
        self.info.sort(key=lambda x: x.time)
        self.trail_key.append([self.info[0].time, self.info[0].time, 0, 0])
        for idx in range(1, len(self.info)):
            self.set_trail_key(idx)

    def set_trail_info(self):
        self.sort_info()
        for k in self.trail_key:
            key = tuple(k)
            self.tr_info[key] = []
            self.intersec_sequence[key] = []
            self.lane[key] = {}
            for idx in range(key[2], key[3] + 1):
                self.tr_info[key].append(self.info[idx])

    def set_sequence(self):
        self.set_trail_info()
        pos_set = set()
        for trail in self.tr_info:
            self.intersec_sequence[trail].append(self.tr_info[trail][0])
            pos_set.add((self.tr_info[trail][0].intr_sec, self.tr_info[trail][0].pos))
            for x in self.tr_info[trail][1:-1]:
                if (x.intr_sec, x.pos) not in pos_set:
                    self.intersec_sequence[trail].append(x)
                    pos_set.add((x.intr_sec, x.pos))
            self.intersec_sequence[trail].append(self.tr_info[trail][-1])

    def set_lane(self):
        self.set_sequence()
        for trail in self.intersec_sequence:
            length = len(self.intersec_sequence[trail])
            cnt = 0
            while cnt < length:
                sec1 = self.intersec_sequence[trail][cnt].intr_sec
                tm1 = self.intersec_sequence[trail][cnt].time
                pos1 = self.intersec_sequence[trail][cnt].pos
                if (cnt + 1) < length and self.intersec_sequence[trail][cnt + 1].intr_sec == sec1:
                    tm2 = self.intersec_sequence[trail][cnt + 1].time
                    pos2 = self.intersec_sequence[trail][cnt + 1].pos
                    if (cnt + 2) < length and self.intersec_sequence[trail][cnt + 2].intr_sec == sec1:
                        tm3 = self.intersec_sequence[trail][cnt + 2].time
                        pos3 = self.intersec_sequence[trail][cnt + 2].pos
                        if (cnt + 3) < length and self.intersec_sequence[trail][cnt + 3].intr_sec == sec1:
                            tm4 = self.intersec_sequence[trail][cnt + 3].time
                            pos4 = self.intersec_sequence[trail][cnt + 3].pos
                            self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos3)]
                            self.lane[trail][(tm2, tm3, sec1)] = Position.LANE_DIC[(pos2, pos3)]
                            self.lane[trail][(tm3, tm4, sec1)] = Position.LANE_DIC[(Position.CENTER, pos4)]
                            break
                        else:
                            if cnt + 3 < length:
                                tm4 = self.intersec_sequence[trail][cnt + 3].time
                                self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos3)]
                                self.lane[trail][(tm2, tm3, sec1)] = Position.LANE_DIC[(pos2, pos3)]
                                self.lane[trail][(tm3, tm4, sec1)] = Position.LANE_DIC[(Position.CENTER, pos3)]
                                cnt += 3
                            else:
                                if pos1 != 0:
                                    self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos2)]
                                    self.lane[trail][(tm2, tm3, sec1)] = Position.LANE_DIC[(pos2, pos3)]
                                    break
                                else:
                                    self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos2)]
                                    self.lane[trail][(tm2, tm3, sec1)] = Position.LANE_DIC[(pos1, pos3)]
                                    break
                    else:
                        if cnt + 2 < length:
                            tm3 = self.intersec_sequence[trail][cnt + 2].time
                            pos3 = self.intersec_sequence[trail][cnt + 2].pos
                            self.lane[trail][(tm1, tm3, sec1)] = Position.LANE_DIC[(Position.CENTER, -pos3)]
                            cnt += 2
                        else:
                            if pos1 != pos2:
                                self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos2)]
                                break
                            else:
                                len1 = self.intersec_sequence[trail][cnt].get_info_dir_length()
                                len2 = self.intersec_sequence[trail][cnt + 1].get_info_dir_length()
                                if len1 <= len2:
                                    self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(Position.CENTER, pos2)]
                                    break
                                else:
                                    self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(pos1, pos2)]
                                    break
                else:
                    if cnt + 1 < length:
                        tm2 = self.intersec_sequence[trail][cnt + 1].time
                        pos2 = self.intersec_sequence[trail][cnt + 1].pos
                        self.lane[trail][(tm1, tm2, sec1)] = Position.LANE_DIC[(Position.CENTER, -pos2)]
                        cnt += 1
                    else:
                        break

    def get_trail_key(self, from_info):
        for trail in self.trail_key:
            if trail[0] <= from_info.time <= trail[1]:
                return trail[0], trail[1], trail[2], trail[3]

    def get_segment_key(self, from_info, trail):
        for i in self.lane[trail]:
            if i[0] <= from_info.time <= i[1]:
                return i


# Location info about intersections
class InterSection:
    n = 0
    dict_location = {0: (521677, 58127),
                     1: (521580, 57490),
                     2: (521520, 57090),
                     3: (521457, 56668),
                     4: (521426, 55855),
                     5: (521418, 54888),
                     6: (521406, 53996)}
    # 1: (521580, 57466)
    # 2: (521520, 57059)
    # 3: (521452, 56668)
    # 4: (521433, 55855)
    # 5: (521411, 54880)
    # 6: (521400, 53998)}

    def __init__(self):
        self.n = len(self.dict_location)

    # Find the nearest intersection of a vehicle or a trail info
    def find_nearest_inter(self, from_info):
        temp = []
        for i in range(self.n):
            temp.append([i, pow(self.dict_location[i][0] - from_info.x_coordinate, 2) +
                         pow(self.dict_location[i][1] - from_info.y_coordinate, 2)])
        return min(temp, key=lambda x: x[1])[0]


# A table mapping location and time information to a vehicle
class TimeIntsecLaneIdTable:
    map_table = {}

    def __init__(self, info, data_process):
        self.map_table = {}
        trail = data_process.vehicles[info.id].get_trail_key(info)
        segmt_key = data_process.vehicles[info.id].get_segment_key(info, trail)
        key = (info.time, info.intr_sec, data_process.vehicles[info.id].lane[trail][segmt_key])
        self.map_table[key] = []
        self.map_table[key].append(info.id)

    def add_mapping(self, info, data_process):
        trail = data_process.vehicles[info.id].get_trail_key(info)
        segmt_key = data_process.vehicles[info.id].get_segment_key(info, trail)
        key = (info.time, info.intr_sec, data_process.vehicles[info.id].lane[trail][segmt_key])
        if key in self.map_table:
            self.map_table[key].append(info.id)
        else:
            self.map_table[key] = []
            self.map_table[key].append(info.id)


class DataProcess:
    info_list_from_data = []
    vehicles = {}
    info_of_all = []   # Set of all 'Info' class
    map_table = {}

    def __init__(self):
        self.info_list_from_data = []
        self.vehicles = {}
        self.info_of_all = []
        self.map_table = {}

        with open('trail_info.txt', 'r') as data:
            file_list = data.readlines()
            for i in range(1, len(file_list)):
                self.info_list_from_data.append(file_list[i].split(','))
                self.info_list_from_data[-1].pop()
                self.info_list_from_data[-1][1] = dt.datetime.fromtimestamp(int(self.info_list_from_data[-1][1]))
                self.info_list_from_data[-1][2] = round(float(self.info_list_from_data[-1][2]))
                self.info_list_from_data[-1][3] = round(float(self.info_list_from_data[-1][3]))
                self.info_list_from_data[-1][4] = float(self.info_list_from_data[-1][4])
                self.info_list_from_data[-1][5] = int(self.info_list_from_data[-1][5])

    def process(self):
        last_vehicle = ''
        for j in self.info_list_from_data:
            single_info = Info(j)
            self.info_of_all.append(single_info)
            if j[0] in self.vehicles:
                self.vehicles[j[0]].add_info(single_info)
            else:
                if len(last_vehicle) > 0:
                    self.vehicles[last_vehicle].set_lane()
                self.vehicles[j[0]] = Vehicle(single_info)
                last_vehicle = j[0]
        self.vehicles[last_vehicle].set_lane()

        time_mapping = TimeIntsecLaneIdTable(self.info_of_all[0], self)
        for i in self.info_of_all[1:]:
            time_mapping.add_mapping(i, self)
        self.map_table = time_mapping.map_table.copy()

    def get_vehicles_number(self, tm_intsec_lne):
        return len(self.map_table[tm_intsec_lne])


if __name__ == "__main__":
    a = DataProcess()
    a.process()

    with open('mapping_table.txt', 'w') as mapping:
        for i in a.map_table:
            s = str(i) + ': ' + str(a.map_table[i])
            mapping.write(s)
            mapping.write('\n')

    # count = {}
    # for i in a.vehicles:
    #     count[i] = 0
    #     for j in a.vehicles[i].info[1:]:
    #         idx = a.vehicles[i].info.index(j)
    #         x1 = time.mktime(j.time.timetuple())
    #         x2 = time.mktime(a.vehicles[i].info[idx - 1].time.timetuple())
    #         if abs(x1 - x2) > 10:
    #             count[i] = count[i] + 1
    # sum = 0
    # for i in count:
    #     sum += count[i]
    #     print i, count[i]
    # print '\n'
    # print sum
    # with open('mp.txt', 'r') as mp:
    #

    # num0 = num1 = num2 = num3 = num4 = num5 = num6 = num7 = num8 = num9 = num10 = num11 = num12 = num13 = \
    # num14 = num15 = num_1 = 0
    # for i in a.map_table:
    #     if i[2] == 0:
    #         num0 += 1
    #     elif i[2] == 1:
    #         num1 += 1
    #     elif i[2] == 2:
    #         num2 += 1
    #     elif i[2] == 3:
    #         num3 += 1
    #     elif i[2] == 4:
    #         num4 += 1
    #     elif i[2] == 5:
    #         num5 += 1
    #     elif i[2] == 6:
    #         num6 += 1
    #     elif i[2] == 7:
    #         num7 += 1
    #     elif i[2] == 8:
    #         num8 += 1
    #     elif i[2] == 9:
    #         num9 += 1
    #     elif i[2] == 10:
    #         num10 += 1
    #     elif i[2] == 11:
    #         num11 += 1
    #     elif i[2] == 12:
    #         num12 += 1
    #     elif i[2] == 13:
    #         num13 += 1
    #     elif i[2] == 14:
    #         num14 += 1
    #     elif i[2] == 15:
    #         num15 += 1
    #     elif i[2] == -1:
    #         num_1 += 1
    # print 'num0 = ', num0
    # print 'num1 = ', num1
    # print 'num2 = ', num2
    # print 'num3 = ', num3
    # print 'num4 = ', num4
    # print 'num5 = ', num5
    # print 'num6 = ', num6
    # print 'num7 = ', num7
    # print 'num8 = ', num8
    # print 'num9 = ', num9
    # print 'num10 = ', num10
    # print 'num11 = ', num11
    # print 'num12 = ', num12
    # print 'num13 = ', num13
    # print 'num14 = ', num14
    # print 'num15 = ', num15
    # print 'num_1 = ', num_1
    # print num0 + num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8 + num9 + num10 + num11 + num12


