# Reference fee arithmetic tests

This is a standalone Python **reference implementation** for the proposed 2% split. It does not change CKPool, build a coinbase transaction, validate addresses or enable mining.

From the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The official CKPool integration must use checked integer arithmetic in C and be tested independently against Bitcoin Core regtest. This Python reference is not a substitute for consensus or integration tests.
