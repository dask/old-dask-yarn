[![Build Status](https://travis-ci.org/dask/dask-yarn.svg?branch=master)](https://travis-ci.org/dask/dask-yarn)
[![Coverage Status](https://coveralls.io/repos/github/dask/dask-yarn/badge.svg?branch=master)](https://coveralls.io/github/dask/dask-yarn?branch=master)

## Example

```python

>>> from dask_yarn import YARNCluster
>>> cluster = YARNCluster()

>>> from dask.distributed import Client
>>> client = Client(cluster)
>>> cluster.start(2, cpus=1, memory=100)

>>> future = client.submit(lambda x: x + 1, 10)
>>> future.result()
11
```
