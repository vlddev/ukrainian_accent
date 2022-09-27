# -*- coding: utf-8 -*-

import sys
import sqlite3 as lite

class AccentDb:
    DICT_DB = 'dict_ua.db'

    def __init__(self, dbFile=DICT_DB, useAmbiguous=False):
        self.con = lite.connect(dbFile)
        self.ambiguous = set()
        if useAmbiguous:
            self.loadAmbiguous()

    def getAccent(self, wf, fid):
        ret = wf
        if self.isAmbiguous(wf):
            cur = self.con.cursor()
            cur.execute("""select distinct wf.accent 
                            from wf, fidmap 
                            where wf = ? and wf.fid = fidmap.fid and fidmap.udfid = ?""", (wf,fid))
            data = cur.fetchall()
            if len(data) == 0:
                # nothing found
                pass
            elif len(data) == 1 and data[0][0] == 'empty_':
                # nothing found
                pass
            else:
                if len(data) == 1:
                    ret = data[0][0].replace('"','\N{COMBINING ACUTE ACCENT}')
                else:
                    # too much found
                    pass
        return ret

    def loadAmbiguous(self):
        cur = self.con.cursor()
        cur.execute("select wf from ambiguous")
        data = cur.fetchall()
        for row in data:
            self.ambiguous.add(row[0])

    def isAmbiguous(self, wf):
        if len(self.ambiguous) == 0:
            return True
        if wf in self.ambiguous:
            return True
        return False

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