
## Example

```python

  from dask_yarn import YARNCluster
  cluster = YARNCluster

   from dask.distributed import Client
   client = Client(cluster)
   client.start_workers(2)

   >>> future = client.submit(lambda x: x + 1, 10)
   >>> future.result()
   11
```

