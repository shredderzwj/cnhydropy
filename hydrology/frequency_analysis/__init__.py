import os

from .frequency import PearsonThree
from .frequency import PearsonThreeContinuousFit
from .frequency import PearsonThreeDiscontinuousFit
from cnhydropy.utils.md2html import MD2Html


class Documentation(object):
    @property
    def principle(self):
        md = MD2Html(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'principle.md'))
        return md.html
