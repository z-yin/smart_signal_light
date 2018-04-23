import os
import re


with open("not_exam_para.txt", "w") as res:
    for root, dirs, files in os.walk("./"):
        files = sorted(files)
        for name in files:
            if name.startswith("final_") and name.endswith(".txt"):
                with open(name, "r") as f:
                    lines = f.readlines()
                    lines = filter(lambda x: not re.match(r'^\s*$', x), lines)
                # if not lines[-1].startswith("total time"):
                    res.write(name)
                    res.write(" : ")
                    res.write(lines[-1])
                    res.write("\n")
