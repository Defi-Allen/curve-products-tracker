from src.utils.contract_utils import init_contract


# https://etherscan.io/address/0x6955a55416a06839309018A8B0cB72c4DDC11f15
TRICRYPTO_CURVE_GAUGE = init_contract(
    "0x6955a55416a06839309018A8B0cB72c4DDC11f15",
)

# https://etherscan.io/address/0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF
TRICRYPTO_LP_TOKEN = init_contract(
    "0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF",
)

# https://etherscan.io/address/0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F
CONVEX_GETREWARDS_CONTRACT = init_contract(
    "0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F",
)

# https://etherscan.io/address/0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5
TRICRYPTO_POOL_CONTRACT = init_contract(
    "0x80466c64868E1ab14a1Ddf27A676C3fcBE638Fe5",
)

# https://etherscan.io/address/0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785
TRICRYPTO_DEPOSIT_CONTRACT = init_contract(
    "0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
)

TRICRYPTO_LP_TOKEN_LIST = ["USDT", "WBTC", "ETH"]
TOKEN_DECIMAL_MULTIPLIER = {"USDT": 1e-6, "WBTC": 1e-8, "ETH": 1e-18}
