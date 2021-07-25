import argparse
import os

from brownie import multicall
from brownie import web3
from brownie.network import disconnect
from pandas import DataFrame

from src.core.datastructures.current_position import Position
from src.core.operations.get_pool_txes import get_mint_txes
from src.core.operations.get_position import CurvePositionCalculator
from src.core.products_factory import TRICRYPTO_V2
from src.utils.network_utils import connect


ALCHEMY_URL = f"https://eth-mainnet.alchemyapi.io/v2/{os.environ['ALCHEMY_API_KEY']}"
ETH_ADDRESS = os.environ.get("ETH_ADDRESS", "0x989aeb4d175e16225e39e87d0d97a3360524ad80")
BLOCK_STEPS = int(os.environ.get("BLOCK_STEPS", 100))


def main():
    # connect to custom note provider in args
    connect(ALCHEMY_URL)

    # initialise tricrypto calculator
    tricrypto_calculator = CurvePositionCalculator(TRICRYPTO_V2)

    # get address's first transaction:
    added_liquidity_txes = get_mint_txes(
        user_address=ETH_ADDRESS,
        token_addr=TRICRYPTO_V2.token_contracts["crv3crypto"].addr,
        from_block=TRICRYPTO_V2.contract.genesis_block,
    )

    if not added_liquidity_txes:  # no txes made
        pass

    latest_block = web3.eth.block_number

    block_start = int(added_liquidity_txes[0]["blockNum"], 16)
    query_blocks = list(range(block_start, latest_block + 1, BLOCK_STEPS))
    if latest_block not in query_blocks:
        query_blocks.append(latest_block)

    columns = [
        "block_number",
        "time",
        "lp_balance",
        "curve_gauge_balance",
        "convex_gauge_balance",
        "num_usdt_tokens",
        "num_wbtc_tokens",
        "num_eth_tokens",
    ]
    position_data = DataFrame(index=query_blocks, columns=columns)

    print(f"User Address: {ETH_ADDRESS}")
    print("Fetching all deposits to Curve v2 TriCrypto pool.")

    for idx, _ in position_data.iterrows():

        idx: int = idx

        try:

            block_position = tricrypto_calculator.get_position(
                ETH_ADDRESS, block_number=idx
            )
            position_data = shove_data(block_position, position_data, idx)

            print(f"Calculated position in block {idx}.")

        except ValueError:
            continue

    position_data.dropna(inplace=True)
    position_data.set_index("time", inplace=True)
    position_data.to_csv(f"./{ETH_ADDRESS}.csv")

    # disconnect
    disconnect()


def shove_data(
    block_position: Position, position_data: DataFrame, idx: int
) -> DataFrame:

    try:
        position_data.loc[idx, "block_number"] = block_position.block_number
        position_data.loc[idx, "time"] = block_position.time
        position_data.loc[idx, "lp_balance"] = block_position.token_balances[
            "liquidity_pool"
        ]
        position_data.loc[
            idx, "curve_gauge_balance"
        ] = block_position.token_balances["curve_gauge"]
        if "convex_gauge" not in block_position.token_balances.keys():
            position_data.loc[idx, "convex_gauge_balance"] = 0
        else:
            position_data.loc[
                idx, "convex_gauge_balance"
            ] = block_position.token_balances["convex_gauge"]
        position_data.loc[idx, "num_usdt_tokens"] = block_position.tokens[
            0
        ].num_tokens
        position_data.loc[idx, "num_wbtc_tokens"] = block_position.tokens[
            1
        ].num_tokens
        position_data.loc[idx, "num_eth_tokens"] = block_position.tokens[
            2
        ].num_tokens

        return position_data

    except KeyError:  # if missing keys then don't store data
        return position_data


if __name__ == "__main__":
    main()
