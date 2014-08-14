import doctest


suite = doctest.DocFileSuite('test_hard_coded_mcodes.py')

if __name__ == '__main__':
    doctest.testfile("test_hard_coded_mcodes.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from project.cho.hard_coded_mcodes import HardCodedMCodes
>>> HardCodedMCodes.mcode_from_psmid('cho_bcrc_1933_0001_000_0000')  # its in the mcode table, so isn't hard coded!


>>> HardCodedMCodes.mcode_from_psmid('cho_meet_1923_0001_000_0000')  # its hard coded!
'5XFF'

>>> HardCodedMCodes.mcode_from_psmid('cho_meet_1993_0001_000_0000')  # its hard coded!
'6SBM'

>>> HardCodedMCodes.mcode_from_psmid('cho_rpax_1943_0001_000_0000')  # its hard coded!
'5XFC'

>>> HardCodedMCodes.mcode_from_psmid('cho_chrx_2013_0001_000_0000')  # its hard coded!
'6SBN'

# EgestAdapterError: Failed to transfer files to an export platform (error="McodeMissing: Tried to release an item, but we do not yet have an MCode for this item (psm_id="cho_rpax_1998_negrine_000_0000")")
>>> HardCodedMCodes.mcode_from_psmid('cho_rpax_1998_negrine_000_0000')
'6SBN'

'''
