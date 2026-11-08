#ifndef SOLOMINE_REWARD_SPLIT_H
#define SOLOMINE_REWARD_SPLIT_H
#include <stdint.h>
/* Pure arithmetic only; not yet connected to CKPool coinbase construction. */
#define SOLOMINE_FEE_BPS UINT64_C(200)
#define SOLOMINE_BPS_DENOM UINT64_C(10000)
#define SOLOMINE_MAX_MONEY UINT64_C(2100000000000000)
/* Returns 0 on success, -1 for invalid input. */
static inline int solomine_split_reward(uint64_t total, uint64_t *miner, uint64_t *developer)
{
    if (!miner || !developer || total > SOLOMINE_MAX_MONEY) return -1;
    /* Safe within Bitcoin's money range: total*200 < UINT64_MAX. */
    const uint64_t fee = total * SOLOMINE_FEE_BPS / SOLOMINE_BPS_DENOM;
    *developer = fee;
    *miner = total - fee;
    return 0;
}
#endif
