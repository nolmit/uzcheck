__author__ = 'kit'
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import json
from jjdecode import JJDecoder
from urllib import quote
from models.trains_model import TrainModel


class uzrequest(object):

    urlMain = "http://booking.uz.gov.ua"
    urlApiSearch = "http://booking.uz.gov.ua/ru/purchase/search/"
    urlStation = "http://booking.uz.gov.ua/ru/purchase/station/"

    def getDestinationID(self, destinationName):
        fullUrl=  self.urlStation+destinationName
        response = requests.post(fullUrl)
        jsObject = json.loads(response._content)
        arr = jsObject.get('value')
        if len(arr) > 0:
            return arr[0]['station_id']



    def getTokenAndCookies(self):
        response = requests.post(self.urlMain)
        content = response.content
        match = re.search('gaq.push....trackPageview...;(.*?);.function',content )
        gv_token_code = match.group(1)
        cookie_values = response.cookies.values()
        line = JJDecoder(gv_token_code).decode()
        gv_token = re.search("\,..(.*?).\);", line).group(1)
        list = [gv_token, cookie_values]

        return list

    def formingBodyJson(self, arr, dest, date):

        arr_id = self.getDestinationID(arr)
        dest_id = self.getDestinationID(dest)
        if arr_id is not None & dest_id is not None:
             encodedArr = quote(arr)
             encodedDest = quote(dest)
             json = ('station_id_from='+arr_id +
                   '&station_id_till='+dest_id +
                   '&station_from='+encodedArr +
                   '&station_till='+encodedDest +
                   '&date_dep='+date+
                   '&time_dep=00%3A00'+
                   '&another_ec=0')
        return json

    def formingHeadersJson(self):

        paramList = self.getTokenAndCookies()

        json = {'Accept': '*/*',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,uk;q=0.2,pl;q=0.2',
               'Accept-Encoding': 'gzip, deflate',
               'GV-Token': paramList[0],
               'Content-Type': 'application/x-www-form-urlencoded',
               'GV-Ajax': '1',
               'Connection': 'keep-alive',
               'Cookie': '_gv_sessid='+paramList[1][2]+';HTTPSERVERID='+paramList[1][0]+';_gv_lang=ru;',
               'GV-Screen': '1280x800',
               'GV-Referer': 'http://booking.uz.gov.ua/ru/',
               }

        return json

    def parse_response(self, content):
        jsObj = json.loads(content)
        root = jsObj.get('value')
        isl = isinstance(root, list)
        ne = root.__len__() > 0
        if isl & ne:
            trains = []
            for train in root:
                num = train.get('num')
                travel_time = train.get('travel_time')
                station_from = train.get('from').get('station')
                station_from_date = train.get('from').get('src_date')
                station_till = train.get('till').get('station')
                station_till_date = train.get('till').get('src_date')
                places_type = train.get('types')
                tp = []
                if places_type.__len__() > 0:
                    for places in places_type:
                        title = places.get('title')
                        places_num = places.get('places')
                        tp.append(title+':'+str(places_num))
                tm = TrainModel(num, station_from, station_from_date, station_till, station_till_date, travel_time, tp)
                trains.append(tm)

            return trains


    def postRequest(self, arr, dest,date):

        body = self.formingBodyJson(arr, dest, date)
        if body is not None:
           ansv = requests.post(url=self.urlApiSearch, data=body, headers=self.formingHeadersJson())

           return ansv




