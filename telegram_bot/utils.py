from typing import Optional

from loguru import logger


def create_hw_data_message(hw_data: dict[str, Optional[str]]) -> str:
    logger.info(hw_data)
    for name, value in hw_data.items():
        if not value or value == "":
            value = "-"

    logger.info(hw_data)

    return f"""
    <b><a href="{hw_data["hw_url"]}">HW</a></b>{hw_data["hw"]}
    Стойка: {hw_data["rack"]}
    Юнит: {hw_data["unit"]}
    Объект: <b><a href="{hw_data["placement_facility_url"]}">{hw_data["placement_facility"]}</a></b>
    Занимаемые юниты: {hw_data["units_amount"]}
    Производитель: {hw_data["manufacturer"]}
    Модель: {hw_data["name"]}
    Серийный номер: {hw_data["serial_number"]}
    Комментарий: {hw_data["comment"]}
    Комментарий клиента: {hw_data["client_comment"]}
    """
