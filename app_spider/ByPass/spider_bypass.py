import requests

def header_request(url,data):
    header = {
        "Accept":"*/*",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Cache-Control":"no-cache",
        "X-Requested-With":"XMLHttpRequest",
        "If-Modified-Since":"0",
        "Referer":"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc",
        "Host":"kyfw.12306.cn",
    }
    response = requests.get(url=url,headers=header,data=data)
    return response

def header_index():
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-08-17&leftTicketDTO.from_station=VVP&leftTicketDTO.to_station=HZH&purpose_codes=ADULT'
    data = {
        "JSESSIONID":"03B9D494C0D937BAC712CB415BE9EBB4;",
        "route":"6f50b51faa11b987e576cdb301e545c4;",
        "BIGipServerotn":"854589962.24610.0000;",
        "_jc_save_fromStation":"%u77f3%u5bb6%u5e84%u5317%2CVVP;",
        "_jc_save_toStation":"%u676d%u5dde%2CHZH;",
        "_jc_save_fromDate":"2020-08-17;",
        "_jc_save_toDate":"2020-07-19;",
        "_jc_save_wfdc_flag":"dc;",
        "RAIL_EXPIRATION":"1595407923706;",
        "RAIL_DEVICEID":"qhruDztCnKBqoTGgEDFJmzDhEVsLW60gYEwnYZzHMtX43nBX94LPxmytVH-lWpKthCNYDXQlmhH9anqn5d6RZSZOSaDtecBG6o-V1w0Ip7tWx2nFVc71hGJIS6SHx4amLnWpmVVTiUvnimNHfC3YCeQWJ3PM_V_7",
    }
    response = header_request(url=url,data=data)
    print(response.text)

header_index()