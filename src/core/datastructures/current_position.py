from dataclasses import field
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pytz as pytz
from marshmallow_dataclass import dataclass

from src.core.datastructures.base import BaseDataStruct
from src.core.datastructures.fees import PoolFees
from src.core.datastructures.rewards import Rewards
from src.core.datastructures.tokens import Token


@dataclass
class Position(BaseDataStruct):

    time: datetime = pytz.utc.localize(datetime.utcnow())
    block_number: Optional[int] = 0
    token_balances: Dict[str, float] = field(default_factory=lambda: {"": 0})
    accrued_fees: PoolFees = PoolFees()
    tokens: List[Token] = field(default_factory=lambda: [Token()])
    outstanding_rewards: List[Rewards] = field(
        default_factory=lambda: [Rewards()]
    )
