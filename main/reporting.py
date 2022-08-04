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

            connection.close()
            return result

        except Exception as e:
            #connection.rollback()
            return e

class tradeReport(SQL):
    def misu_select_sql(self, table_name, name, target):
        sql = f"select {name}, sum(price - pay) as misu from {table_name} where {name}='{target}'"
        res = self.select(sql)
        return res[0]

    def misu(self, table_name, name, target):
        misu = dict()
        res = self.misu_select_sql(table_name, name, target)
        if res[1]:
            misu["name"] = res[0]
            misu["misu"] = res[1]

        return misu

    def client_misu(self):
        misu = list()
        clients = Client.objects.all()

        for client in clients:
            res = self.misu("trade_clientTrade", "client", client.client)
            if res:
                misu.append(res)

        return misu

    def fix_misu(self):
        misu = list()
        fixs = FixCost.objects.all()

        for fix in fixs:
            res = self.misu("trade_fixCost", "fix", fix.fix)
            if res:
                misu.append(res)

        return misu

    def royal_misu(self):
        misu = list()
        royals = Royalty.objects.all()
        for royal in royals:
            res = self.misu("trade_royalty", "royalty", royal.royalty)
            if res:
                misu.append(res)

        return misu

    def manage_misu(self):
        misu = list()
        manages = Manage.objects.all()
        sql = "select date, price from trade_manage where status='미납'"
        res = self.select(sql)
        for r in res:
            print(r)
            misu.append({'name': r[0], 'misu': r[1]})
        return misu

    def rant_misu(self):
        misu = list()
        rants = RantPay.objects.all()
        for rant in rants:
            res = self.misu("trade_rantpay", "rant", rant.rant)
            if res:
                misu.append(res)

        return misu