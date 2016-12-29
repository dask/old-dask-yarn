ANACONDADIR=${1:-"/opt/anaconda"}

$ANACONDADIR/bin/pip install pytest-cov
$ANACONDADIR/bin/py.test --cov=dask_yarn dask_yarn/tests --cov-report term-missing -s -vv
