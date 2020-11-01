from ..library import *

#from botlib.bot import Bot
#from botlib.sonar import Sonar

class BotLibrary(Library):
    MIN_DIST = 20
    MAX_DIST = 50

    def __init__(self):
        self._inst = None

        module = pylovm2.ModuleBuilder.named('bot')

        module.add('fahre').pyfn(self._drive)
        module.add('lenke').pyfn(self._steer)
        module.add('stop').pyfn(self._stop)
        module.add('linetracker').pyfn(self._linetracker)

        module.add('ist_sensor_frei?').pyfn(self._check_sensor)
        module.add('klassifiziere?').pyfn(self._classify)

        """
        module.add('links') create_const(Sonar.LEFT))
        module.add('links45') create_const(Sonar.LEFT45))
        module.add('linksvorne') create_const(Sonar.LEFT_FRONT))
        module.add('rechtsvorne') create_const(Sonar.RIGHT_FRONT))
        module.add('rechts45') create_const(Sonar.RIGHT45))
        module.add('rechts') create_const(Sonar.RIGHT))
        module.add('hinten') create_const(Sonar.BACK))
        """

        super().__init__(module.build())

    def _get_inst(self):
        if not self._inst:
            self._inst = Bot()
            self._inst.calibrate()
        return self._inst

    def _stop(self, ctx):
        self._get_inst().stop_all()

    def _drive(self, arg1):
        self._get_inst().drive_power(arg1)

    def _steer(self, arg1):
        self._get_inst().drive_steer(arg1)

    def _linetracker(self, arg1):
        self._get_inst().linetracker().autopilot(arg1)

    def _check_sensor(self, arg1):
        ret = self._getinst().sonar().read(arg1)
        return BotLibrary.MIN_DIS <= ret <= BotLibrary.MAX_DIS

    def _classify(self, arg1):
        return self._get_inst().objdetect().detect(arg1)
