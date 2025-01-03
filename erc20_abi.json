# https://docs.pancakeswap.finance/developers/smart-contracts/pancakeswap-exchange/v3-contracts#address

import json

RPC_URLS = {
    "Arbitrum": "https://endpoints.omniatech.io/v1/arbitrum/one/public",
    "Optimism": "https://op-pokt.nodies.app",
    # "Base": "https://1rpc.io/base"
    "Base": "https://base-pokt.nodies.app"
    # "Base": "https://base.meowrpc.com"
    # "Base": "https://base.drpc.org"
}

EXPLORERS_URL = {
    "Arbitrum": "https://arbiscan.io/",
    "Optimism": "https://optimistic.etherscan.io/",
    "Base": "https://basescan.org/"
}

CHAIN_ID_BY_NAME = {
    'Arbitrum': 42161,
    'Optimism': 10,
    'Base': 8453
}

ETH_MASK = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

IZUMI_CONTRACTS = {
    'Arbitrum': {
        'quoter': '0x96539F87cA176c9f6180d65Bc4c10fca264aE4A5',
        'router': '0x01fDea353849cA29F778B2663BcaCA1D191bED0e'
    },
    'Base': {
        'quoter': '0x2db0AFD0045F3518c77eC6591a542e326Befd3D7',
        'router': '0x02F55D53DcE23B4AA962CC68b0f685f26143Bdb2'
    }
}

# UNISWAP_CONTRACTS = {
#     'Arbitrum': {
#         'quoter': '0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6',
#         'router': '0xE592427A0AEce92De3Edee1F18E0157C05861564'
#     }
# }


TOKENS_PER_CHAIN = {
    'Arbitrum': {
        "ETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        # "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
    },
    'Optimism': {
        "ETH": "0x4200000000000000000000000000000000000006",
        # "WETH": "0x4200000000000000000000000000000000000006",
        "USDC":"0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"
    },
    'Base': {
        "ETH" : "0x4200000000000000000000000000000000000006",
        # "ETH": "0x0000000000000000000000000000000000000000",
        # "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    }
}

with open('erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('izumi_swap_quoter_abi.json') as file:
    IZUMI_SWAP_QUOTER_ABI = json.load(file)

with open('izumi_swap_router_abi.json') as file:
    IZUMI_SWAP_ROUTER_ABI = json.load(file)
