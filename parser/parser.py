from typing import Optional
import os

import requests
from bs4 import BeautifulSoup
from pprint import pprint
from config import CORP_USERNAME, CORP_PASSWORD
from loguru import logger
# import validators


HW_URL_TEMPLATE = "https://corp.reconn.local/device/"
AUTH_URL = "https://corp.reconn.local/login"
AUTH_LDAP_URL = "https://corp.reconn.local/login/ldap/login"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://corp.reconn.local',
    'Connection': 'keep-alive',
    'Referer': 'https://corp.reconn.local/login',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

session = requests.Session()

def parse_hw_page_by_hw_number(hw: str | int) -> dict[str, Optional[str]]:
    hw_url = HW_URL_TEMPLATE + str(hw)
    return parse_hw_page(hw_url)

def parse_hw_page(hw_url: str | int) -> dict[str, Optional[str]]:
    """
    parse corp hw page

    Args:
        session: request session object
        headers: http headers
        hw: hardware number without "hw" or valide url

    Returns:
        dict:
            'hw_url'
            'hw'
            'name'
            'serial_number'
            'units_amount'
            'manufacturer'
            'rack'
            'unit'
    """

    logger.info(f"Start parsing {hw_url}")
    hw_info = {
        "hw_url": None,
        "id": None,
        "name": None,
        "comment": None,
        "client":None,
        "client_comment": None,
        "parent_device": None,
        "placement_facility": None,
        "placement_facility_url": None,
        "serial_number": None,
        "manufacturer": None,
        "units_amount": None,
        "rack": None,
        "unit": None
    }

    parent_device_url = None

    # if not validators.url(hw_url):
    #     raise ValueError("Not valid url")

    hw_info["hw_url"] = hw_url

    response = session.get(hw_url,
                           headers=headers,
                           verify='parser/reconnLocal.pem',
                           cert=('parser/myCert.crt', 'parser/myKey.key'))
    soup = BeautifulSoup(response.content, 'lxml')

    table_elements = soup.find("table", {"class": "table table-striped table-bordered detail-view"}).findAll("tr")
    for tr in table_elements:
        # print(tr.th.text.strip() + ": " + tr.td.text.strip())
        td = tr.td.text.strip()
        match tr.th.text.strip():
            case "ID":
                hw_info["id"] = td
            case "Название":
                hw_info["name"] = td
            case "Родительское устройство":
                if tr.td.find("a"):
                    parent_device_url = tr.td.find("a").get("href")
            case "Серийный номер":
                hw_info["serial_number"] = td
            case "Производитель":
                hw_info["manufacturer"] = td
            case "Количество юнитов":
                hw_info["units_amount"] = td
            case "Количество юнитов":
                hw_info["units_amount"] = td
            case "Комментарий":
                hw_info["comment"] = td
            case "Комментарий клиента":
                hw_info["client_comment"] = td
            case "Владелец":
                hw_info["client"] = td

    panel_bodys = soup.find_all("div", {"class": "panel-body"})
    placement_body = None
    for panel_body in panel_bodys:
        panel_body_h3_array = panel_body.findAll("h3")
        for h3 in panel_body_h3_array:
            if ("Размещение" in h3.text.strip()):
                placement_body = panel_body
                break

    if (placement_body):
        logger.info("found placement_body")

        panel_body_h4_array = placement_body.findAll("h4")
        placement_facility_h4 = None
        for h4 in panel_body_h4_array:
            if ("Размещено на объекте:" in h4.text.strip()):
                placement_facility_h4 = h4
                break

        if (placement_facility_h4):
            logger.info("found placement_facility_h4")
            hw_info["placement_facility"] = placement_facility_h4.find("a").text.strip()
            hw_info["placement_facility_url"] = placement_facility_h4.find("a").get("href")

        placement_table = placement_body.find("table", {"class": "table"})
        if placement_table:
            logger.info("found placement_table")
            placement_table_trs = placement_table.findAll("tr")
            if (placement_table_trs):
                for tr in placement_table_trs:
                    td = tr.td.text.strip()
                    match tr.th.text.strip():
                        case "Стойка":
                            hw_info["rack"] = td
                        case "Юнит":
                            hw_info["unit"] = td

    if parent_device_url is not None:
        hw_info["parent_device"] = parse_hw_page(parent_device_url)

    logger.info(hw_info)
    return hw_info

def corp_authentication():
    response = session.get(AUTH_URL,
                           headers=headers,
                           verify='parser/reconnLocal.pem',
                           cert=('parser/myCert.crt', 'parser/myKey.key'))

    soup = BeautifulSoup(response.content, 'lxml')
    auth_token = soup.find_all("input", {"name": "_token"})[0].get("value")

    session.headers.update({'Referer': AUTH_URL})
    session.headers.update(headers)

    auth_data = {
        "_token": auth_token,
        "ldap_username": CORP_USERNAME,
        "password": CORP_PASSWORD
    }

    response = session.post(AUTH_LDAP_URL,
                            headers=headers,
                            data=auth_data,
                            cookies=session.cookies,
                            verify='parser/reconnLocal.pem',
                            cert=('parser/myCert.crt', 'parser/myKey.key'))

    logger.info(f"Corp authentication: {response}")
    return


if __name__ == "__main__":
    corp_authentication()
    hw_info = parse_hw_page_by_hw_number(2935)
    pprint(hw_info)

