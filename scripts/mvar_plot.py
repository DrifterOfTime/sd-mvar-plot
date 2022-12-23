import os
import sys

from pprint import pprint

pprint(os.getenv("PYTHONPATH"))

try:
    from utils.modules.base.MVModuleBase import MVModuleBase
except:
    pprint("MVar Plot not working", stream=sys.stderr)

try:
    from PIL import Image
except:
    pprint("WebUI not working", stream=sys.stderr)