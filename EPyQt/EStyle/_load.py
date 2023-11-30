import os.path as op
from EPyQt.EStyle import EQss


basedir = op.dirname(__file__)


def load_bs_style():
    with open(op.join(basedir, 'bootstrap.qss')) as f:
        qss = f.read()
    return EQss.toCSS(qss)
