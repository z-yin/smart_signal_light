# -*- coding: utf-8 -*-

import numpy as np
import adapt_func as adp
import data_process as dp


def get_phase(a, day, start_time, phase_num, phase_final):
    sab = 0.3
    for h in range(7):
        t = minu[h][phase_num]
        if t != 0:
            piA = []
            piB = []
            for j in range(4):
                pia = adp.get_p_num(a, day, start_time, h, 3*j) + \
                      adp.get_p_num(a, day, start_time, h, 3*j + 1) + \
                      adp.get_p_num(a, day, start_time, h, 3*j + 2)
                pib = adp.get_p_num(a, day, start_time, h, j + 12)
                piA.append(pia)
                piB.append(pib)
            wab = {}
            for k in range(4):
                wab[k] = {}
                for kk in range(4):
                    if kk != k:
                        piab = adp.get_p_num(a, day, start_time, h, ab_dic[(k, kk)])
                        dab = min(piab / sab, 1)
                        w_ = max(piA[k] - piB[kk], 0)
                        w_ = w_ * dab
                        wab[k][kk] = w_

            result = {}
            for phase_time in range(t, 201 - 3 * t):
                result_ = 0
                for m in range(4):
                    for mm in range(4):
                        if mm != m:
                            if p_[h][m][mm] == 1:
                                vab = sab
                            else:
                                vab = 0
                            result_ += wab[m][mm] * vab * phase_time
                result[phase_time] = result_
            phase_final_ = max(result)
            phase_final.append(phase_final_)
        else:
            phase_final.append(0)


if __name__ == "__main__":
    a = dp.DataProcess()
    a.process()

    print "a over"

    minu = [[35, 8, 10, 35, 0], [8, 35, 8, 35, 0], [10, 35, 35, 0, 0], [10, 35, 10, 8, 35], [10, 35, 35, 0, 0],
            [10, 35, 10, 35, 0], [10, 35, 35, 0, 0]]
    phase = [4, 4, 3, 5, 3, 4, 3]
    P = [[], [], [], [], []]
    final_phase = [[], [], [], [], []]
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

    p_ = [p1, p2, p3, p4, p5, p6, p7]

    ab_dic = {(0, 1): 1,
              (0, 2): 2,
              (0, 3): 0,
              (1, 0): 4,
              (1, 2): 3,
              (1, 3): 5,
              (2, 0): 6,
              (2, 1): 8,
              (2, 3): 7,
              (3, 0): 11,
              (3, 1): 9,
              (3, 2): 10}

    start_time = 0
    for phase_id in range(5):
        get_phase(a, (5, 4), start_time, phase_id, final_phase[phase_id])
        start_time += max(final_phase[phase_id])
    for i in range(7):
        print(final_phase[0][i])
        print(final_phase[1][i])
        print(final_phase[2][i])
        print(final_phase[3][i])
        print(final_phase[4][i])
