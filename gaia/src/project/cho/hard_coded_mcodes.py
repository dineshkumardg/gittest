class HardCodedMCodes:
    # http://jira.cengage.com/browse/EG-455
    @classmethod
    def mcode_from_psmid(cls, psmid):
        # see release_view.py
        psmid_prefix = psmid[:12]
        if psmid_prefix in ['cho_meet_192', 'cho_meet_193', 'cho_meet_194', 'cho_meet_195', 'cho_meet_196', 'cho_meet_197']:
            return '5XFF'
        elif psmid_prefix in ['cho_meet_198', 'cho_meet_199', 'cho_meet_200', 'cho_meet_201']:
            return '6SBM'
        elif psmid_prefix in ['cho_chrx_191', 'cho_chrx_192', 'cho_chrx_193', 'cho_chrx_194', 'cho_chrx_195', 'cho_chrx_196', 'cho_chrx_197', 'cho_rpax_192', 'cho_rpax_193', 'cho_rpax_194', 'cho_rpax_195', 'cho_rpax_196', 'cho_rpax_197', 'cho_chbp_197']:
            return '5XFC'
        elif psmid_prefix in ['cho_rpax_198', 'cho_rpax_199', 'cho_rpax_200', 'cho_rpax_201', 'cho_chrx_198', 'cho_chrx_199', 'cho_chrx_200', 'cho_chrx_201']:
            return '6SBN'
        else:
            return None
