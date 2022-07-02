from trade.models import *
from django.shortcuts import render
from django.db import connection

class SQL:
    cursor = connection.cursor()

    def select(self, sql):
        try:
            query = sql
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            #connection.commit()
            connection.close()
            return result

        except Exception as e:
            #connection.rollback()
            return e

class tradeReport(SQL):
    def client_misu(self):
        misu = list()
        clients = Client.objects.all()

        for client in clients:
            tmp = dict()
            sql = f"select sum(price - pay) from trade_clientTrade where client = '{client.client}'"
            res = self.select(sql)
            tmp["name"] = client.client
            tmp["misu"] = res[0][0]
            misu.append(tmp)
            print(client.client, res[0][0])

        return misu

    def fix_misu(self):
        misu = list()
        fixs = Fix.objects.filter(paytype="수기납부")

        for fix in fixs:
            tmp = dict()
            sql = f"select sum(price - pay) from trade_fixCost where fix='{fix.fix}'"
            res = self.select(sql)
            tmp["name"] = fix.fix
            tmp["misu"] = res[0][0]
            misu.append(tmp)
        return misu

    def royal_misu(self):
        misu = list()
        fixs = Fix.objects.filter(paytype="수기납부")

        for fix in fixs:
            tmp = dict()
            sql = f"select sum(price - pay) from trade_fixCost where fix='{fix.fix}'"
            res = self.select(sql)
            tmp["name"] = fix.fix
            tmp["misu"] = res[0][0]
            misu.append(tmp)
        return misu

    def manage_misu(self):
        misu = list()
        fixs = Fix.objects.filter(paytype="수기납부")

        for fix in fixs:
            tmp = dict()
            sql = f"select sum(price - pay) from trade_fixCost where fix='{fix.fix}'"
            res = self.select(sql)
            tmp["name"] = fix.fix
            tmp["misu"] = res[0][0]
            misu.append(tmp)
        return misu

    def rant_misu(self):
        misu = list()
        rants = Rant.objects.all()

        sql = "select strftime('%Y-%m', date), rant from trade_rantpay where (price-pay) > 0"
        res = self.select(sql)
        print(res)

        return res