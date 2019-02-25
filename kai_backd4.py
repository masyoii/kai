#!/usr/bin/env python
"""

(C) Copyright 2018 aphip_uhuy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import os
import schedule
import time
import datetime
import pycurl
import json
from io import StringIO
import logging

logging.basicConfig(filename='kai_backd-' + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def main():
    print('=======================================================')
    print('              Nggolek Tiket V2.7')
    print('')
    print('This tools used to book ticket smartly')
    print('This program is secret software: you cant redistribute it and/or modify')
    print('it under the terms of the Himacrot License as published by')
    print('the Secret Software Society, either version 3 of the License, or')
    print('any later version.')
    print('')
    print('Usage: python kai_backd.py retry_num use_proxy(0 if no, 1 if yes) set_seat(0 if no, 1 if yes) recipe')
    print('')
    print('=======================================================')
    print('')

    args = len(sys.argv)
    if args < 5:
        print('\nUsage: python ' + str(sys.argv[0]) + ' retry_num use_proxy(0 if no, 1 if yes) set_seat(0 if no, 1 if yes) recipe\n')
        sys.exit()

    numretry = sys.argv[1]
    isusingproxy = sys.argv[2]
    issetseat = sys.argv[3]
    filepath = sys.argv[4]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    if numretry == "":
        print("Num of retry cannot be blank. Exiting...")
        sys.exit()

    if isusingproxy == "":
        print("use of proxy cannot be blank. Exiting...")
        sys.exit()

    if issetseat == "":
        print("set seat cannot be blank. Exiting...")
        sys.exit()

    linedata = []
    with open(filepath) as my_file:
        linedata = my_file.readlines()

    if issetseat == "1":
        if linedata.count < 3:
            print("please define json seat data on recipe. Exiting...")
            sys.exit()

    if issetseat == "0":
        linedata[2] = "{}"

    kai_booktiket(linedata[0].strip(), linedata[1].strip(), numretry, isusingproxy, issetseat, linedata[2].strip())


def retry_login(logindata, numretry, usingproxy):
    successlogin = False
    usingproxy = bool(int(usingproxy) > 0)
    retrylogin = 0
    maxretrylogin = int(numretry)
    reslogin = ""

    while retrylogin < maxretrylogin and not successlogin:
        try:
            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Retrying login no : ' + str(retrylogin))
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> login to kai :')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data login to kai :')
            print(logindata)
            # print('#########################################')
            buf = cStringIO.StringIO()
            e = pycurl.Curl()
            e.setopt(
                e.URL, 'https://kaiaccess11.kai.id/api/v12/auth/login')
            e.setopt(e.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'Accept: application/json',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e.setopt(e.POST, 1)
            e.setopt(
                e.POSTFIELDS, logindata)
            e.setopt(e.WRITEFUNCTION, buf.write)
            e.setopt(e.VERBOSE, False)
            e.setopt(e.CONNECTTIMEOUT, 60)
            e.setopt(e.SSL_VERIFYPEER, 0)
            e.setopt(e.SSL_VERIFYHOST, 0)
            if(usingproxy):
                e.setopt(e.PROXY, '127.0.0.1')
                e.setopt(e.PROXYPORT, 9050)
                e.setopt(e.PROXYTYPE, e.PROXYTYPE_SOCKS5)
            e.perform()

            if e.getinfo(e.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf.getvalue())
                logging.warning('error login res : ' + str(buf.getvalue))
                buf.close()
                raise Exception

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> login res : ' + buf.getvalue())
            reslogin = json.loads(buf.getvalue())
            logging.info('login res : ' + str(reslogin))
            buf.close()
            successlogin = True
            print('#########################################')
            print('')

        except Exception as err:
            print(err)
            time.sleep(20)
            retrylogin += 1
            if retrylogin >= maxretrylogin:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Too many error attempts .. Quiting .. ')
                sys.exit()

    return reslogin


def booking_class(loginres, logindata, bookingdata, numretry, usingproxy):
    successbook = False
    usingproxy = bool(int(usingproxy) > 0)
    retrybook = 0
    maxretrybook = int(numretry)
    resbooking = ""

    while retrybook < maxretrybook and not successbook:
        try:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Retrying no : ' + str(retrybook))
            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> sending raw data booking to kai :')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data booking to kai ...')
            tokenhead = loginres['token']
            print(bookingdata)

            buf2 = cStringIO.StringIO()
            e2 = pycurl.Curl()
            e2.setopt(
                e2.URL, 'https://kaiaccess11.kai.id/api/v12/booking_b2b')
            e2.setopt(e2.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'accept: application/json, text/plain, */*',
                'authorization: Bearer ' + tokenhead + '',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e2.setopt(e2.POST, 1)
            e2.setopt(
                e2.POSTFIELDS, bookingdata)
            e2.setopt(e2.WRITEFUNCTION, buf2.write)
            e2.setopt(e2.VERBOSE, False)
            e2.setopt(e2.CONNECTTIMEOUT, 60)
            e2.setopt(e2.SSL_VERIFYPEER, 0)
            e2.setopt(e2.SSL_VERIFYHOST, 0)
            if(usingproxy):
                e2.setopt(e2.PROXY, '127.0.0.1')
                e2.setopt(e2.PROXYPORT, 9050)
                e2.setopt(e2.PROXYTYPE, e2.PROXYTYPE_SOCKS5)
            e2.perform()

            if e2.getinfo(e2.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf2.getvalue())
                logging.warning('error booking res : ' + str(buf2.getvalue()))
                if str(buf2.getvalue()) == '{"error":"token_invalid"}' or (str(buf2.getvalue()) == '{"error":"token_expired"}'):
                    loginres = retry_login(logindata, numretry, usingproxy)
                raise Exception

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> booking res : ' + buf2.getvalue())
            resbooking = json.loads(buf2.getvalue())
            logging.info('booking res : ' + str(resbooking))
            buf2.close()
            successbook = True
            print('#########################################')
            print('')

        except Exception as err:
            print(err)
            time.sleep(20)
            retrybook += 1
            if retrybook >= maxretrybook:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Too many error attempts .. Quiting .. ')
                sys.exit()

    return resbooking


def payment1_class(loginres, logindata, bookcode, numcode, numretry, usingproxy):
    successpay = False
    usingproxy = bool(int(usingproxy) > 0)
    retrypay = 0
    maxretrypay = int(numretry)
    respay = ""

    while retrypay < maxretrypay and not successpay:
        try:
            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> sending raw data payment to kai :')

            datapayment = json.dumps({})
            # bookcode = resbooking['data']['order']['book_code']
            # numcode = resbooking['data']['order']['num_code']
            tokenhead = loginres['token']
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data payment to kai ...')

            print('booking code : ' + bookcode)
            print('order code : ' + numcode)

            buf3 = cStringIO.StringIO()
            e3 = pycurl.Curl()
            e3.setopt(
                e3.URL, 'https://kaiaccess11.kai.id/api/v12/add_extra_fee?book_code=' + bookcode + '&payment_type=ATM')
            e3.setopt(e3.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'accept: application/json, text/plain, */*',
                'authorization: Bearer ' + tokenhead + '',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e3.setopt(e3.POST, 1)
            e3.setopt(
                e3.POSTFIELDS, datapayment)
            e3.setopt(e3.WRITEFUNCTION, buf3.write)
            e3.setopt(e3.VERBOSE, False)
            e3.setopt(e3.SSL_VERIFYPEER, 0)
            e3.setopt(e3.SSL_VERIFYHOST, 0)

            if(usingproxy):
                e3.setopt(e3.PROXY, '127.0.0.1')
                e3.setopt(e3.PROXYPORT, 9050)
                e3.setopt(e3.PROXYTYPE, e3.PROXYTYPE_SOCKS5)

            e3.perform()

            if e3.getinfo(e3.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf3.getvalue())
                logging.info('error pay res : ' + str(buf3.getvalue()))
                if str(buf3.getvalue()) == '{"error":"token_invalid"}' or (str(buf3.getvalue()) == '{"error":"token_expired"}'):
                    loginres = retry_login(logindata, numretry, usingproxy)
                raise Exception

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> payment res : ' + buf3.getvalue())
            respay = json.loads(buf3.getvalue())
            logging.info('pay res : ' + str(respay))
            buf3.close()
            successpay = True
            print('#########################################')
            print('')

        except Exception as err:
            print(err)
            time.sleep(20)
            retrypay += 1
            if retrypay >= maxretrypay:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Too many error attempts .. Quiting .. ')
                sys.exit()

    return respay


def flag_class(loginres, logindata, bookcode, numcode, numretry, usingproxy):
    successflag = False
    usingproxy = bool(int(usingproxy) > 0)
    retryflag = 0
    maxretryflag = int(numretry)
    resflag = ""

    while retryflag < maxretryflag and not successflag:
        try:
            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> sending raw data payment flag to kai :')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data payment flag to kai ...')

            print('booking code : ' + bookcode)
            print('order code : ' + numcode)

            tokenhead = loginres['token']

            buf4 = cStringIO.StringIO()
            e4 = pycurl.Curl()
            e4.setopt(
                e4.URL, 'https://kaiaccess11.kai.id/api/v12/payment/pay?book_code=' + bookcode + '&token=' + tokenhead + '&num_code=' + numcode + '&payment_type=ATM')
            e4.setopt(e4.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'accept: application/json, text/plain, */*',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e4.setopt(e4.WRITEFUNCTION, buf4.write)
            e4.setopt(e4.VERBOSE, False)
            e4.setopt(e4.SSL_VERIFYPEER, 0)
            e4.setopt(e4.SSL_VERIFYHOST, 0)

            if(usingproxy):
                e4.setopt(e4.PROXY, '127.0.0.1')
                e4.setopt(e4.PROXYPORT, 9050)
                e4.setopt(e4.PROXYTYPE, e4.PROXYTYPE_SOCKS5)

            e4.perform()

            if e4.getinfo(e4.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf4.getvalue())
                logging.info('flag res : ' + str(buf4.getvalue()))
                if str(buf4.getvalue()) == '{"error":"token_invalid"}' or (str(buf4.getvalue()) == '{"error":"token_expired"}'):
                    loginres = retry_login(logindata, numretry, usingproxy)
                raise Exception

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> payment flag res : ' + buf4.getvalue())
            resflag = buf4.getvalue()
            logging.info('flag res : ' + str(resflag))
            buf4.close()
            successflag = True

            print('#########################################')
            print('')

            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> sending raw data payment flag 2 to kai :')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data payment flag 2 to kai ...')

            print('booking code : ' + bookcode)
            print('order code : ' + numcode)

            tokenhead = loginres['token']

            buf5 = cStringIO.StringIO()
            e5 = pycurl.Curl()
            e5.setopt(
                e5.URL, 'https://kaiaccess11.kai.id/api/v12/order/history/detail?book_code=' + bookcode)
            e5.setopt(e5.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'accept: application/json, text/plain, */*',
                'authorization: Bearer ' + tokenhead + '',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e5.setopt(e5.WRITEFUNCTION, buf5.write)
            e5.setopt(e5.VERBOSE, False)
            e5.setopt(e5.SSL_VERIFYPEER, 0)
            e5.setopt(e5.SSL_VERIFYHOST, 0)

            if(usingproxy):
                e5.setopt(e5.PROXY, '127.0.0.1')
                e5.setopt(e5.PROXYPORT, 9050)
                e5.setopt(e5.PROXYTYPE, e5.PROXYTYPE_SOCKS5)

            e5.perform()

            if e5.getinfo(e5.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf5.getvalue())
                buf5.close()

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> payment flag 2 res : ' + buf5.getvalue())
            respayment2flag = json.loads(buf5.getvalue())
            logging.info('flag2 res : ' + str(respayment2flag))
            buf5.close()
            # success = True
            print('#########################################')

        except Exception as err:
            print(err)
            time.sleep(20)
            retryflag += 1
            if retryflag >= maxretryflag:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Too many error attempts .. Quiting .. ')
                sys.exit()

    return resflag


def seat_class(loginres, logindata, bookcode, numcode, numretry, usingproxy, seatdata):
    successseat = False
    usingproxy = bool(int(usingproxy) > 0)
    retryseat = 0
    maxretryseat = 1
    resseat = ""

    while retryseat < maxretryseat and not successseat:
        try:
            print('#########################################')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> sending raw data set seat to kai :')

            print(seatdata)
            dataseatjson = '{"book_code": "' + bookcode + '", "passenger":[' + seatdata + ']}'  # json.dumps({"book_code": bookcode, "passenger": [seatdata]})
            dataseat = str(dataseatjson)
            # bookcode = resbooking['data']['order']['book_code']
            # numcode = resbooking['data']['order']['num_code']
            tokenhead = loginres['token']
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> try sending raw data set seat to kai ...')

            print('data seat : ' + dataseat)

            buf6 = cStringIO.StringIO()
            e6 = pycurl.Curl()
            e6.setopt(
                e6.URL, 'https://kaiaccess11.kai.id/api/v12/manual_seat')
            e6.setopt(e6.HTTPHEADER, [
                'Content-Type: 	application/json;charset=utf-8', 'accept: application/json, text/plain, */*',
                'authorization: Bearer ' + tokenhead + '',
                'source: mobile', 'User-Agent: okhttp/3.4.1'])
            e6.setopt(e6.POST, 1)
            e6.setopt(
                e6.POSTFIELDS, dataseat)
            e6.setopt(e6.WRITEFUNCTION, buf6.write)
            e6.setopt(e6.VERBOSE, False)
            e6.setopt(e6.SSL_VERIFYPEER, 0)
            e6.setopt(e6.SSL_VERIFYHOST, 0)

            if(usingproxy):
                e6.setopt(e6.PROXY, '127.0.0.1')
                e6.setopt(e6.PROXYPORT, 9050)
                e6.setopt(e6.PROXYTYPE, e6.PROXYTYPE_SOCKS5)

            e6.perform()

            ''' if e3.getinfo(e3.HTTP_CODE) != 200:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> opps found error :')
                print(buf3.getvalue())
                logging.info('error pay res : ' + str(buf3.getvalue()))
                if str(buf3.getvalue()) == '{"error":"token_invalid"}' or (str(buf3.getvalue()) == '{"error":"token_expired"}'):
                    loginres = retry_login(logindata, numretry, usingproxy)
                raise Exception '''

            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' process -> set seat res : ' + buf6.getvalue())
            resseat = json.loads(buf6.getvalue())
            logging.info('pay res : ' + str(resseat))
            buf6.close()
            successseat = True
            print('#########################################')
            print('')

        except Exception as err:
            print(err)
            time.sleep(20)
            retryseat += 1
            if retryseat >= maxretryseat:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Too many error attempts .. Quiting .. ')
                # sys.exit()

    return resseat


def kai_booktiket(logindata, bookingdata, numretry, usingproxy, setseat, seatdata):
    success = False
    usingproxy = bool(int(usingproxy) > 0)
    retry = 0
    maxretry = int(numretry)

    while retry < maxretry and not success:
        try:
            reslogin = retry_login(logindata, numretry, usingproxy)

            if reslogin['status'] == 200:
                resbooking = booking_class(reslogin, logindata, bookingdata, numretry, usingproxy)

                if resbooking['status'] == 200:
                    bookcode = resbooking['data']['order']['book_code']
                    numcode = resbooking['data']['order']['num_code']
                    if setseat == "1":
                        resseat = seat_class(reslogin, logindata, bookcode, numcode, numretry, usingproxy, seatdata)

                    respayment = payment1_class(reslogin, logindata, bookcode, numcode, numretry, usingproxy)

                    if respayment['status'] == 200:
                        resflag = flag_class(reslogin, logindata, bookcode, numcode, numretry, usingproxy)

                        print(resflag)
                        success = True

        except Exception as er:
            print(er)
            # logging.error('Exception : ' + er)
            time.sleep(20)
            # continue

        retry += 1
        print('=======================================================')


if __name__ == '__main__':
    main()
