# -*- coding: utf-8 -*-

import sys
import sqlite3 as lite

DICT_DB = 'dict_ua.db'

def getAccent(con, wf, fid):
    ret = wf
    cur = con.cursor()
    # TODO: add mapping table fid --> fid
    cur.execute("select wf.accent from wf where wf = ? and fid = ?", (wf,fid))
    data = cur.fetchall()
    if len(data) == 1 and data[0][0] == 'empty_':
        # nothing found
        pass
    else:
        if len(data) == 1:
            ret = data[0][0].replace('"','\N{COMBINING ACUTE ACCENT}')
        else:
            # too much found
            pass
    return ret

try:
    con = lite.connect(DICT_DB)
    print(getAccent(con, 'абажур', '8_1'))
finally:
    if con:
        con.close()


