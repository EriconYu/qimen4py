# qimen4py

Python 原生奇门遁甲排盘 SDK。历法使用 `lunar-python`，运行时不依赖 Node.js 或其他语言。

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
