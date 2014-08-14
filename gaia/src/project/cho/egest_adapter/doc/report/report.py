from gaia.gift.gift25 import meta
from project.cho.hard_coded_mcodes import HardCodedMCodes


class Report:
    def meta_mcode(self):
        return meta.mcode(HardCodedMCodes.mcode_from_psmid(self.psmid()))
