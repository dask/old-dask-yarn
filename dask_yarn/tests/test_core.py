from dask_yarn import YARNCluster
from distributed import Client
from distributed.utils_test import loop

def test_yarn_cluster(loop):
    with YARNCluster() as cluster:
        cluster.start(2, cpus=1, memory=1000)
        with Client(cluster, loop=loop) as client:
            future = client.submit(lambda x: x + 1, 10)
            assert future.result() == 11

