# -*- coding: utf-8 -*-

import sys
import sqlite3 as lite

class AccentDb:
    DICT_DB = 'dict_ua.db'

    def __init__(self, dbFile=DICT_DB):
        self.con = lite.connect(dbFile)

    def getAccent(self, wf, fid):
        ret = wf
        cur = self.con.cursor()
        # TODO: add mapping table fid --> fid
        cur.execute("""select wf.accent from wf, fidmap 
                        where wf = ? and wf.fid = fidmap.fid and fidmap.udfid = ?""", (wf,fid))
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

    def close(self):
        if self.con:
            self.con.close()

"""
try:
    accentDb = AccentDb() 
    print(accentDb.getAccent('абажур', '8_1'))
finally:
    accentDb.close()
"""