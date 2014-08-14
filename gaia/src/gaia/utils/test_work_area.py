import os
import unittest
from testing.gaia_test import GaiaTest
from gaia.utils.work_area import WorkArea

class TestWorkArea(GaiaTest):

    def test(self):
        class Config:
            working_dir = self.test_dir

        config = Config()

        #print self.test_dir
        # check creation and naming
        work_area = WorkArea(config)
        self.assertTrue(os.path.basename(work_area.path).startswith('work_area_'))
        #print work_area.path

        work_area = WorkArea(config, prefix='egest_pid99')
        #print work_area.path
        self.assertTrue(os.path.basename(work_area.path).startswith('egest_pid99_'))    # note that the extra underscore should be added.

        work_dir = work_area.path
        self.assertTrue(os.path.exists(work_dir))
        

        # check ls()
        fpaths = work_area.ls()
        self.assertEqual([], fpaths)

        num_files = 3
        for f_num in range(0, num_files):
            f = open(os.path.join(work_dir, 'f%d.txt' % f_num), 'w')
            f.write('hello')
            f.close()

        fpaths = work_area.ls()
        self.assertEqual(num_files, len(fpaths))

        # make sure remove cleans up properly.
        work_area.remove()
        self.assertFalse(os.path.exists(work_dir))

        # check that a new area is created each time
        work_area2 = WorkArea(config)
        self.assertNotEqual(work_area2.path, work_dir)

        work_area3 = WorkArea(config)
        self.assertNotEqual(work_area3.path, work_dir)
        self.assertNotEqual(work_area3.path, work_area2.path)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestWorkArea),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
