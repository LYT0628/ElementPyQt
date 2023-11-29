import os.path as op

from EPyQt import EUtils

basedir = op.dirname(__file__)


def load():
    with open(op.join(basedir, 'bootstrap.qss')) as f:
        qss = f.read()
    return EUtils.toCSS(qss)
