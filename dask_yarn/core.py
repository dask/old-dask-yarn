

from hashlib import sha1
import os
import re

from knit import Knit, CondaCreator
from distributed import LocalCluster
from toolz import unique

global_packages = ['dask>=0.11', 'distributed>=1.13']

prog = re.compile('\w+')


def first_word(s):
    return prog.match(s).group()


class YARNCluster(object):
    def __init__(self, packages=[]):
        self.local_cluster = LocalCluster(n_workers=0)
        self.packages = list(unique(packages + global_packages, key=first_word))
        self.knit = Knit(autodetect=True)

    @property
    def scheduler_address(self):
        return self.local_cluster.scheduler_address

    def start(self, n_workers, cpus=1, memory=4000):
        env_name = 'dask-' + sha1('-'.join(self.packages).encode()).hexdigest()
        if os.path.exists(os.path.join(CondaCreator().conda_envs, env_name + '.zip')):
            env = os.path.join(CondaCreator().conda_envs, env_name + '.zip')
        else:
            env = self.knit.create_env(env_name=env_name, packages=self.packages)
        command = ('$PYTHON_BIN $CONDA_PREFIX/bin/dask-worker %s > /tmp/worker-log.out 2> /tmp/worker-log-err' %
                   self.local_cluster.scheduler.address)
        app_id = self.knit.start(command, env=env, num_containers=n_workers,
                                 virtual_cores=cpus, memory=memory)
        self.app_id = app_id
        return app_id

    def stop(self):
        try:
            self.knit.kill(self.app_id)
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.local_cluster.close()
        self.stop()
