import asyncio
import logging

from client import Client
from config import RPC_URLS
from iZumiSwap import iZumiSwap
from config import TOKENS_PER_CHAIN

def init_logger():
    """
    Инициализация логгера
    """
    logging.basicConfig(filename='myapp.log',level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def print_available_chains() -> None:
    """
    Вывод доступных сетей согласно настройке в файле config.py
    """
    print(f"Available chains in app: {[k for k in TOKENS_PER_CHAIN.keys()]}\n")

async def init_chain_by_input(logger) -> str:
    """
    Указание пользователем сети блокчейна
    """
    while True:
        print_available_chains()
        chain_name = input("Enter blockchain for swap: ")
        if chain_name in RPC_URLS.keys():
            logger.info("Blockchain correctly!")
            return chain_name
        else:
            print("Blockchain not correctly! Please try again!\n")
            logger.warning("input blockchain not correctly!")

def init_pk_by_input(logger, chain_name) -> str:
    """
    Указание пользователем приватного ключа
    """
    while True:
        pk = input("Enter private key: ")
        try:
            client = Client(pk, chain_name)
            if client.validate_address() and (len(pk) == 66 or len(pk) == 64):
                logger.info("Private  key correctly")
                return pk
            else:
                print("Private key not correctly!")
                logger.warning(f"input private key {pk} not correctly!")
        except Exception as exc:
            print("Private key not correctly!")
            logger.warning(exc)

async def print_balance(client : Client, name_token : str = None) -> None:
    """
    Вывод баланса токена
    """
    decimals =  await client.get_decimals(token_name=name_token)
    balance = client.from_wei_custom(await client.get_balance(name_token), decimals)
    print(f"Balance {name_token} token: {balance}  {name_token}")

async def init_amount_in_token_for_swap_by_input(client: Client, name_code_token_in :str, logger) -> int:
    """
    Указание пользователем кол-ва входного токена для обмена
    """
    while True:
        try:
            amount_input = input(f"\nEnter value of  token for swap {name_code_token_in} (format example-\"0.1\") or enter \"ALL\" for full balance: ")

            if amount_input == 'ALL':
                if name_code_token_in != client.name_native_token and (await client.get_balance("ETH") > (await client.w3.eth.gas_price) * 4):
                    amount_input_token_for_swap_in_wei = await client.get_balance(name_code_token_in)
                    logger.info(f"check_balance_for_swap_by_ALL {amount_input_token_for_swap_in_wei} {name_code_token_in} is True")
                    return amount_input_token_for_swap_in_wei
                elif name_code_token_in == client.name_native_token and ((await client.get_balance(name_code_token_in) - (await client.w3.eth.gas_price) * 4) > 0):
                    amount_input_token_for_swap_in_wei = (await client.get_balance(name_code_token_in)) - (await client.w3.eth.gas_price) * 4
                    return amount_input_token_for_swap_in_wei

                print("\nNot enough balance for this amount! Please change amount!\n")

            amount_input_token_for_swap = float(amount_input)
            decimals = await client.get_decimals(token_name=name_code_token_in)
            amount_input_token_for_swap_in_wei = client.to_wei_custom(amount_input_token_for_swap, decimals)
            if await check_balance_for_swap(client, logger, amount_input_token_for_swap_in_wei, name_code_token_in):
                logger.info(f"check_balance_for_swap_by_amount for {amount_input_token_for_swap} is True")
                return amount_input_token_for_swap_in_wei
            else:
                print("\nNot enough balance for this amount! Please change amount!\n")
                logger.warning("Balance not enough for input amount nft!")
        except ValueError:
            print("Amount not number! Please try again!\n")
            logger.warning("input amount of token not correctly!")

async def check_balance_for_swap(client : Client, logger, amount_token_for_swap_in_wei, name_code_token_in) -> bool:
    """
    Проверка баланса на возможность транзакции с учетом указанного  пользователем кол-ва токена
    """
    gas_price_wei = (await client.w3.eth.gas_price) * 4
    logger.info(f"gas_estimate: {gas_price_wei} WEI")

    logger.info(f"client balance swap token {name_code_token_in}: {await client.get_balance(name_code_token_in)} WEI")
    logger.info(f"client balance native token ETH: {await client.w3.eth.get_balance(client.address)} WEI")

    if name_code_token_in != client.name_native_token:
        if (await client.get_balance(name_code_token_in) >= amount_token_for_swap_in_wei and
                (await client.w3.eth.get_balance(client.address) > gas_price_wei)):
            return True

    if name_code_token_in == client.name_native_token:
        if await client.get_balance(name_code_token_in) > (gas_price_wei + amount_token_for_swap_in_wei):
            return True

    return False

def set_slippage_by_input(logger):
    while True:
        try:
            amount_slippage = float(input(f"\nEnter value of slippage for swap in %(format example-\"0.5, 1, 2, 3,...\"): "))
            logger.info(f"gas_estimate: {amount_slippage} %")
            return amount_slippage
        except ValueError:
            print("Amount not number! Please try again!\n")
            logger.warning("input amount slippage not correctly!")



# 0xb
async def main():
    logger = init_logger()
    # ввод пользователем сети обмена
    chain_name_swap = await init_chain_by_input(logger)

    # ввод пользователем приватного ключа
    pk = init_pk_by_input(logger, chain_name_swap)
    client = Client(pk, chain_name_swap, logger)

    # вывод доступных сетей
    print(f"\nAvailable tokens for {chain_name_swap} chain in app:"
          f" {[k for k in TOKENS_PER_CHAIN.get(chain_name_swap).keys()]}\n")

    # ввод входящей и исходящей монеты с проверкой
    name_code_token_in = "XXX"
    name_code_token_out = "XXX"
    while name_code_token_in == name_code_token_out:
        name_code_token_in = input("Enter input token: ")
        name_code_token_out = input("Enter output token: ")
        if name_code_token_in == name_code_token_out:
            print("INPUT and OUTPUT tokens must be different!")

    # вывод текущего баланса
    await print_balance(client, name_code_token_in)
    await print_balance(client, name_code_token_out)

    # ввод кол-ва входящих монет
    amount_for_swap_in_wei = await init_amount_in_token_for_swap_by_input(client, name_code_token_in, logger)


    # инициализация клиент swap
    swap_client = iZumiSwap(client, logger)
    # выполнение транзакции swap
    print("Выполнение транзакции swap ... ")
    await  swap_client.swap(name_code_token_in, name_code_token_out, amount_for_swap_in_wei,)
    print("Транзакция закончена")

if __name__ == "__main__":
    asyncio.run(main())
