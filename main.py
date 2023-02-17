import json
import random
import asyncio
from contextlib import suppress

import aiohttp


class VK:
    """
    Класс для взаимодействия с ВК
    """
    def __init__(self, token: str) -> None:
        """
        Метод инициализации класса

        :param token: Токен аккаунта ВК
        """
        self.token = token

    async def set_online(self) -> tuple[bool, str | None]:
        """
        Метод для отправки статуса онлайн аккаунта ВК

        :return: tuple[bool, str | None]
        """
        headers = {'Authorization': f'Bearer {self.token}'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'https://api.vk.com/method/account.setOnline?v=5.131') as response:
                json_response = await response.json()
                if 'error' in json_response:
                    return False, json_response["error"]["error_msg"]
                else:
                    return True, None


def file_input() -> dict:
    """
    Функция читает и возвращает словарь с данными аккаунтов

    :return: dict
    """
    with open('./input.json', 'r') as file:
        return json.load(file)


async def main() -> None:
    """
    Главная функция запуска

    :return: None
    """
    input_data = file_input()  # Получаем словарь с данными аккаунтов
    while True:
        for key in input_data.keys():  # Перебираем словарь по его ключам
            account = input_data[key]
            vk = VK(token=account['access_token'])  # Инициализируем класс
            status, response = await vk.set_online()  # Отправляем статус онлайн на аккаунт ВК
            if status:  # Если отправка статуса онлайн удалось
                print(f'Отправлен статус онлайн для аккаунта - {account["url_profile"]}')
            else:  # Если отправка статуса онлайн не удалось
                print(f'Произошла ошибка аккаунта - {account["url_profile"]}: {response} ')

        await asyncio.sleep(random.randint(200, 250))  # Ожидаем перед началом следующего круга


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):  # Игнорирование ошибок при остановке
        asyncio.run(main())  # Запуск асинхронной функции из синхронного контекста
