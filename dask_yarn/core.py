

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
    nn = "localhost"
    nn_port = 8020
    rm = "localhost"
    rm_port = 8088

    def __init__(self, nn=None, nn_port=None, rm=None,
                 rm_port=None, autodetect=True, validate=False, packages=[]):
        try:
            self.local_cluster = LocalCluster(n_workers=0)
        except (OSError, IOError):
            self.local_cluster = LocalCluster(n_workers=0, scheduler_port=0)
        self.packages = list(unique(packages + global_packages, key=first_word))

        # if any hdfs/yarn settings are used don't use autodetect
        if autodetect or not any([nn, nn_port, rm, rm_port]):
            self.knit = Knit(autodetect=True, validate=validate)
        else:
            nn = nn or self.nn
            nn_port = nn_port or self.nn_port
            rm = rm or self.rm
            rm_port = rm_port or self.rm_port
            self.knit = Knit(nn=nn, nn_port=nn_port, rm=rm, rm_port=rm_port,
                             validate=validate)

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
