import gc
from collections import Counter

my_str = "034218743296528739100654931865453543"

c = Counter(my_str)
del my_str
gc.collect()

my_str = f"{0:0<{c['0']}}{1:1<{c['1']}}{1:2<{c['2']}}{3:3<{c['3']}}{4:4<{c['4']}}" \
         f"{5:5<{c['5']}}{6:6<{c['6']}}{7:7<{c['7']}}{8:8<{c['8']}}{9:9<{c['9']}}"
