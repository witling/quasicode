from qclib.library import *

from botlib.bot import Bot
from botlib.sonar import Sonar

class BotLibrary(PyLibrary):
    __module__ = '__main__'

    MIN_DIST = 20
    MAX_DIST = 50

    def __init__(self):
        PyLibrary.__init__(self)
        self._inst = None

        self.ident('fahre', create_fn([Ident('arg1')], self._drive))
        self.ident('lenke', create_fn([Ident('arg1')], self._steer))
        self.ident('stop', create_fn([], self._stop))
        self.ident('linetracker', create_fn([Ident('arg1')], self._linetracker))

        self.ident('ist_sensor_frei?', create_fn([Ident('arg1')], self._check_sensor))
        self.ident('klassifiziere?', create_fn([Ident('arg1')], self._classify))

        self.ident('links', create_const(Sonar.LEFT))
        self.ident('links45', create_const(Sonar.LEFT45))
        self.ident('linksvorne', create_const(Sonar.LEFT_FRONT))
        self.ident('rechtsvorne', create_const(Sonar.RIGHT_FRONT))
        self.ident('rechts45', create_const(Sonar.RIGHT45))
        self.ident('rechts', create_const(Sonar.RIGHT))
        self.ident('hinten', create_const(Sonar.BACK))

    def _get_inst(self):
        if not self._inst:
            self._inst = Bot()
            self._inst.calibrate()
        return self._inst

    def _stop(self, ctx):
        self._get_inst().stop_all()

    def _drive(self, ctx):
        arg1 = ctx['arg1']
        self._get_inst().drive_power(arg1)

    def _steer(self, ctx):
        arg1 = ctx['arg1']
        self._get_inst().drive_steer(arg1)

    def _linetracker(self, ctx):
        arg1 = ctx['arg1']
        self._get_inst().linetracker().autopilot(arg1)

    def _check_sensor(self, ctx):
        arg1 = ctx['arg1']
        ret = self._getinst().sonar().read(arg1)
        return BotLibrary.MIN_DIS <= ret <= BotLibrary.MAX_DIS

    def _classify(self, ctx):
        arg1 = ctx['arg1']
        return self._get_inst().objdetect().detect(arg1)
