import time

from web3.contract import AsyncContract

from client import Client
from config import IZUMI_CONTRACTS, IZUMI_SWAP_QUOTER_ABI, IZUMI_SWAP_ROUTER_ABI, TOKENS_PER_CHAIN, ZERO_ADDRESS

class iZumiSwap:
    def __init__(self, client: Client, logger = None):
        self.client = client
        self.logger = logger
        self.quoter_contract : AsyncContract = self.client.get_contract(
            contract_address=IZUMI_CONTRACTS[self.client.chain_name_code]['quoter'],
            abi=IZUMI_SWAP_QUOTER_ABI
        )
        self.router_contract : AsyncContract = self.client.get_contract(
            contract_address=IZUMI_CONTRACTS[self.client.chain_name_code]['router'],
            abi=IZUMI_SWAP_ROUTER_ABI
        )

    def get_path(self, from_token_name: str, to_token_name: str):
        pool_fee: int = {
            "Arbitrum": {
                'ETH/USDC': 500,
                'USDC/ETH': 500
            },
            "Base": {
                'ETH/USDC': 500,
                'USDC/ETH': 500
            }
        }[self.client.chain_name_code][f"{from_token_name}/{to_token_name}"]

        from_address_bytes = self.client.w3.to_bytes(hexstr=TOKENS_PER_CHAIN[self.client.chain_name_code][from_token_name])
        to_address_bytes = self.client.w3.to_bytes(hexstr=TOKENS_PER_CHAIN[self.client.chain_name_code][to_token_name])
        pool_fee_bytes = pool_fee.to_bytes(3, 'big')
        self.logger.info(f"path - {self.client.w3.to_hex(from_address_bytes + pool_fee_bytes + to_address_bytes)}")
        return from_address_bytes + pool_fee_bytes + to_address_bytes

    async def get_min_amount_out(self, path : str, amount_in_wei: int):
        response_quote = await self.quoter_contract.functions.swapAmount(
            amount_in_wei,
            path
        ).call()
        min_amount_out = response_quote[0]
        self.logger.info(f"min_amount_out - {min_amount_out}")
        return min_amount_out

    async def swap(self, from_token_name: str, to_token_name: str, amount_in_wei: int):

        path = self.get_path(from_token_name, to_token_name)
        deadline = int(time.time() + 1200)
        min_amount_out_in_wei = await self.get_min_amount_out(path, amount_in_wei)
        value = amount_in_wei if from_token_name == self.client.name_native_token else 0

        if from_token_name != self.client.name_native_token:
            from_token_address = TOKENS_PER_CHAIN[self.client.chain_name_code][from_token_name]
            await self.client.make_approve(
                token_address=from_token_address, spender_address=self.router_contract.address,
                amount_in_wei=amount_in_wei
            )

        full_data = [self.router_contract.encodeABI(
            fn_name='swapAmount',
            args=([
                [
                    path,
                    self.client.address if to_token_name != self.client.name_native_token else ZERO_ADDRESS,
                    amount_in_wei,
                    min_amount_out_in_wei,
                    deadline
                ]
            ])
        )]

        if from_token_name == self.client.name_native_token or to_token_name == self.client.name_native_token:
            additional_data = self.router_contract.encodeABI(
                fn_name='refundETH' if from_token_name == 'ETH' else 'unwrapWETH9',
                args=() if from_token_name == 'ETH' else (
                    min_amount_out_in_wei,
                    self.client.address
                )
            )
            self.logger.info(f"additional_data - {additional_data}")
            full_data.append(additional_data)
        self.logger.info(f"full data - {full_data}")

        transaction = await self.router_contract.functions.multicall(
            full_data
        ).build_transaction(await self.client.prepare_tx(value=value))

        self.logger.info(f"transaction - {transaction}")
        return await self.client.send_transaction(transaction, without_gas=True)
