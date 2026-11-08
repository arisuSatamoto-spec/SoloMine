"""Reference arithmetic for SoloMine's proposed coinbase split.

This module is NOT wired into CKPool. No Bitcoin transactions are constructed here.
"""
from __future__ import annotations

FEE_BASIS_POINTS = 200
BASIS_POINTS = 10_000
MAX_MONEY_SATS = 21_000_000 * 100_000_000


def split_reward(total_satoshis: int) -> tuple[int, int]:
    """Return (miner_satoshis, developer_satoshis).

    The developer share is floored to a whole satoshi; the remainder goes
    to the miner. This avoids floating-point rounding.
    """
    if type(total_satoshis) is not int:
        raise TypeError("reward must be an integer number of satoshis")
    if not 0 <= total_satoshis <= MAX_MONEY_SATS:
        raise ValueError("reward is outside the Bitcoin money range")
    developer = total_satoshis * FEE_BASIS_POINTS // BASIS_POINTS
    miner = total_satoshis - developer
    return miner, developer
