from typing import Optional

from loguru import logger


def create_hw_data_message(hw_data: dict[str, Optional[str]]) -> str:
    if hw_data["parent_device"]:
        message = create_hw_data_message_with_parent_device(hw_data)
    else:
        message = create_hw_data_message_without_parent_device(hw_data)
    return message

def create_hw_data_message_with_parent_device(hw_data: dict[str, Optional[str]]) -> str:
    for name, value in hw_data.items():
        if not value or value == "":
            hw_data[name] = " -"

    parent_device = hw_data["parent_device"]
    parent_device_str = f"""<b><a href="{parent_device["hw_url"]}">{parent_device["id"]}</a></b>
        Стойка:  {parent_device["rack"]}
        Юнит:  {parent_device["unit"]}
        Объект:  <a href="{parent_device["placement_facility_url"]}">{parent_device["placement_facility"]}</a>
        Занимаемые юниты:  {parent_device["units_amount"]}
        Производитель:  {parent_device["manufacturer"]}
        Модель:  {parent_device["name"]}
        Серийный номер:  {parent_device["serial_number"]}
        Клиент: {parent_device["client"]}
        Комментарий:  {parent_device["comment"]}
        Комментарий клиента:  {parent_device["client_comment"]}
    """

    return f"""<b><a href="{hw_data["hw_url"]}">{hw_data["id"]}</a></b>
Занимаемые юниты:  {hw_data["units_amount"]}
Производитель:  {hw_data["manufacturer"]}
Модель:  {hw_data["name"]}
Серийный номер:  {hw_data["serial_number"]}
Комментарий:  {hw_data["comment"]}
Комментарий клиента:  {hw_data["client_comment"]}
Родительское устройство:  {parent_device_str}
    """


def create_hw_data_message_without_parent_device(hw_data: dict[str, Optional[str]]) -> str:
    for name, value in hw_data.items():
        if not value or value == "":
            hw_data[name] = " -"

    return f"""<b><a href="{hw_data["hw_url"]}">{hw_data["id"]}</a></b>
Стойка:  {hw_data["rack"]}
Юнит:  {hw_data["unit"]}
Объект:  <a href="{hw_data["placement_facility_url"]}">{hw_data["placement_facility"]}</a>
Занимаемые юниты:  {hw_data["units_amount"]}
Производитель:  {hw_data["manufacturer"]}
Модель:  {hw_data["name"]}
Серийный номер:  {hw_data["serial_number"]}
Комментарий:  {hw_data["comment"]}
Клиент: {hw_data["client"]}
Комментарий клиента:  {hw_data["client_comment"]}
Родительское устройство:  {hw_data["parent_device"]}
    """
