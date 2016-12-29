
## Example

```python

from dask_yarn import YARNCluster
cluster = YARNCluster()

from dask.distributed import Client
client = Client(cluster)
cluster.start(2, cpus=1, memory=100)

>>> future = client.submit(lambda x: x + 1, 10)
>>> future.result()
11
```
