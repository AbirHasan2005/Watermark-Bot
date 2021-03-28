# (c) @AbirHasan2005

import os
import shutil
from configs import Config

async def delete_trash(file):
    try:
        os.remove(file)
    except Exception as e:
        print(e)

async def delete_all():
    try:
        root = Config.DOWN_PATH + "/WatermarkAdder/"
        shutil.rmtree(root)
    except Exception as e:
        print(e)
