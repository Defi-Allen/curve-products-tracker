import argparse
import sys
import json
import os
from src.utils.network_utils import connect

from src.core.operations.get_pool_rewards import (
    OutstandingRewardsCalculator,
)
from src.core.products_factory import TRICRYPTO_V2_POOL


def parse_args():
    parser = argparse.ArgumentParser(
        description="Get outstanding rewards for user."
    )
    parser.add_argument('--address', '-a',
                        dest="address",
                        help="Address to fetch info for.",
                        type=str,
                        # default is convex finance
                        default="0x989aeb4d175e16225e39e87d0d97a3360524ad80"
                        )
    return parser.parse_args()


def main():
    connect(f"https://eth-mainnet.alchemyapi.io/v2/{os.environ['ALCHEMY_API_KEY']}")

    args = parse_args()
    print(f"User Address: {args.address}")
    print("Fetching all unclaimed rewards.")

    rewards_calculator = OutstandingRewardsCalculator(TRICRYPTO_V2_POOL)
    pool_rewards, curve_rewards, convex_rewards = rewards_calculator.get_outstanding_rewards(args.address)
    print(pool_rewards)
    print(curve_rewards)
    print(convex_rewards)


if __name__ == "__main__":
    main()
