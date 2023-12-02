import os.path as op

basedir = op.dirname(__file__)


def load_boot_strap():
    with open(op.join(basedir, 'bootstrap.qss')) as f:
        qss = f.read()
    return qss
