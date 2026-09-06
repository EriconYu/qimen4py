# qimen4py

Python 奇门遁甲排盘 SDK，包内自带经过版本锁定的排盘引擎。要求 Python 3.9+ 和 Node.js 20+。

```python
from qimen4py import calculate, canonical

input_data = {
    "year": 2026, "month": 4, "day": 10, "hour": 14, "minute": 0,
    "timezone": "Asia/Shanghai",
}
chart = calculate(input_data)
portable = canonical(input_data)
```

`calculate` 返回完整结构化盘面，`canonical` 返回规范 JSON。当前算法版本为 `qimen-zhuanpan-chaibu-v1`。
