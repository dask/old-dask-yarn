import os
import sys
import time
import errno
import signal
import subprocess
from functools import wraps

from dask_yarn import YARNCluster
from distributed import Client
from distributed.utils_test import loop


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def test_yarn_cluster(loop):
    python_version = '%d.%d' % (sys.version_info.major, sys.version_info.minor)
    python_pkg = 'python=%s' % (python_version)
    with YARNCluster(packages=[python_pkg]) as cluster:

        @timeout(600)
        def start_dask():
            cluster.start(2, cpus=1, memory=256)
        try:
            start_dask()
        except Exception as e:
            cluster.knit.kill(cluster.knit.app_id)
            print("Fetching logs from failed test...")
            time.sleep(5)
            print(cluster.knit.logs(cluster.knit.app_id))
            print(subprocess.check_output(['free', '-m']))
            print(subprocess.check_output(['df', '-h']))

            sys.exit(1)

        @timeout(300)
        def do_work():
            with Client(cluster, loop=loop) as client:
                print(client)
                future = client.submit(lambda x: x + 1, 10)
                assert future.result() == 11
                print(client)
                print(future)

        time.sleep(2)
        try:
            do_work()
        except Exception as e:
            print(subprocess.check_output(['free', '-m']))
            cluster.knit.kill(cluster.knit.app_id)
            print("Fetching logs from failed test...")
            time.sleep(5)
            print(subprocess.check_output(['free', '-m']))
            print(cluster.knit.logs(cluster.knit.app_id))
            print(subprocess.check_output(['df', '-h']))
            sys.exit(1)
