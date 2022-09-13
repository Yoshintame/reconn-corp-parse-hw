import requests
from bs4 import BeautifulSoup
from pprint import pprint
from config import CORP_USERNAME, CORP_PASSWORD
from loguru import logger

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


def parse_hw_page(session, headers, hw_number):
    """
    parse corp hw page

    Args:
        session: request session object
        headers: http headers
        hw: hardware number for link

    Returns:
    """

    hw_info = {}

    hw_url = HW_URL_TEMPLATE + str(hw_number)
    response = session.get(hw_url,
                           headers=headers,
                           verify='reconnLocal.pem',
                           cert=('myCert.crt', 'myKey.key'))
    soup = BeautifulSoup(response.content, 'lxml')

    table_elements = soup.find("table", {"class": "table table-striped table-bordered detail-view"}).findAll("tr")
    for tr in table_elements:
        # print(tr.th.text.strip() + ": " + tr.td.text.strip())
        td = tr.td.text.strip()
        match tr.th.text.strip():
            case "Название":
                hw_info["name"] = td
            case "Серийный номер":
                hw_info["serial_number"] = td
            case "Производитель":
                hw_info["manufacturer"] = td
            case "Количество юнитов":
                hw_info["units_amount"] = td

    table_elements = soup.findAll("table", {"class": "table"})[1].findAll("tr")
    for tr in table_elements:
        td = tr.td.text.strip()
        match tr.th.text.strip():
            case "Стойка":
                hw_info["rack"] = td
            case "Юнит":
                hw_info["unit"] = td

    hw_info["hw_url"] = hw_url
    pprint(hw_info)
    return hw_info


def corp_authentication(session, headers):
    response = session.get(AUTH_URL,
                           headers=headers,
                           verify='reconnLocal.pem',
                           cert=('myCert.crt', 'myKey.key'))

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
                            verify='reconnLocal.pem',
                            cert=('myCert.crt', 'myKey.key'))

    logger.info(response)
    return


if __name__ == "__main__":
    session = requests.Session()

    corp_authentication(session, headers)

    parse_hw_page(session, headers, 1548)
