import os
import sys

from pprint import pprint

pprint(sys.path)
pprint(os.getenv("PYTHONPATH"))
# base_dir = scripts.basedir()
# sys.path.append(base_dir)
# pprint("Post-append")
# pprint(sys.path)

try:
    from MVUtils.MVModules.base.MVModuleBase import MVModuleBase
except:
    pprint("MVar Plot not working", stream=sys.stderr)

try:
    import modules.scripts as scripts
except:
    pprint("scripts not working", stream=sys.stderr)

try:
    from PIL import Image
except:
    pprint("WebUI not working", stream=sys.stderr)