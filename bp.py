# -*- coding: utf-8 -*-

import numpy as np
import adapt_func as adp
import data_process as dp
import operator


def get_phase(a, day, start_time):
    phase_final = []
    sab = 0.003
    for h in range(7):
        t = 20  # minu[h][phase_num]

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
        for pi in range(5):
            result_ = 0
            for m in range(4):
                for mm in range(4):
                    if mm != m:
                        result_ += wab[m][mm] * 1 * vab(pi, m, mm, h)
            result[pi] = result_
        print(result)
        phase_final.append(max(result.iteritems(), key=operator.itemgetter(1))[0])
    return phase_final


def vab(pi, a, b, h):
    return p_[h][pi][ab_dic[(a, b)]]


if __name__ == "__main__":
    a = dp.DataProcess()
    a.process()

    print "a over"

    minu = [[35, 8, 10, 35, 0], [8, 35, 8, 35, 0], [10, 35, 35, 0, 0], [10, 35, 10, 8, 35], [10, 35, 35, 0, 0],
            [10, 35, 10, 35, 0], [10, 35, 35, 0, 0]]
    phase = [4, 4, 3, 5, 3, 4, 3]
    P = [[], [], [], [], []]
    final_phase = [[], [], [], [], []]
    p0 = [[0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
          [0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p1 = [[0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
          [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
          [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p2 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p3 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1]]
    p4 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p5 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
          [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    p6 = [[0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
          [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    p_ = [p0, p1, p2, p3, p4, p5, p6]

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

    start_time = 1000
    phases = []
    for t in range(1000, 1600, 20):
        phases.append(get_phase(a, (5, 4), t))
    print phases
