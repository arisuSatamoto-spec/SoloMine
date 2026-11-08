#include <assert.h>
#include <stdint.h>
#include "reward_split.h"
static void check(uint64_t total, uint64_t expected_miner, uint64_t expected_dev)
{
    uint64_t miner = 0, dev = 0;
    assert(solomine_split_reward(total, &miner, &dev) == 0);
    assert(miner == expected_miner && dev == expected_dev);
    assert(miner + dev == total);
}
int main(void)
{
    uint64_t miner, dev;
    check(0, 0, 0);
    check(49, 49, 0);
    check(50, 49, 1);
    check(99, 98, 1);
    check(320000000, 313600000, 6400000);
    check(312500000, 306250000, 6250000);
    check(SOLOMINE_MAX_MONEY, 2058000000000000ULL, 42000000000000ULL);
    assert(solomine_split_reward(SOLOMINE_MAX_MONEY+1, &miner, &dev) == -1);
    assert(solomine_split_reward(100, 0, &dev) == -1);
    assert(solomine_split_reward(100, &miner, 0) == -1);
    return 0;
}
