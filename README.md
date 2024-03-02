# hsbcrate

```sh
pip install hsbcrate
```

```python
from hsbcrate import Range
from hsbcrate import RateRequest

resp = RateRequest(ccy_pairs=["USDTWD", "JPYTWD"], range=Range.ONE_DAY).do()
for r in resp:
    print(r.latest)
```
