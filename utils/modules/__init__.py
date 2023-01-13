from glob import glob
from os import sep

__modules = glob(f'utils{sep}modules{sep}*.py')

for m in __modules:
    if m[:2] != "__":
        m = m.replace(sep, ".")
        string = f'from {m} import *'
        exec(string)