#!/usr/bin/env python3
import sys

sys.path.append(".")
from src.data import Data

data = Data()
s = """\
某君昆仲，今隐其名，皆余昔日在中学时良友；\
分隔多年，消息渐阙。日前偶闻其一大病；适归故乡，迂道往访，则仅晤一人，言病者其弟也。\
劳君远道来视，然已早愈，赴某地候补⑵矣。因大笑，出示日记二册，谓可见当日病状，不妨献诸旧友。\
持归阅一过，知所患盖“迫害狂”之类。语颇错杂无伦次，又多荒唐之言；亦不著月日，惟墨色字体不一，知非一时所书。\
间亦有略具联络者，今撮录一篇，以供医家研究。记中语误，一字不易；惟人名虽皆村人，不为世间所知，无关大体，然亦悉易去。\
至于书名，则本人愈后所题，不复改也。七年四月二日识。\
"""
try:
    for x in [k for i in s.split("，") for j in i.split("；") for k in j.split("。")]:
        data.addItem(x, x[::-1])
except FileExistsError:
    exit()
