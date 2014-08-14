import time
import unittest
from gaia.task.job_queue import JobQueue

class TestJobQueue(unittest.TestCase):

    def test_append(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q._jobs))
        q.append(1)
        self.assertEqual(1, len(q._jobs))
        q.append(2)
        self.assertEqual(2, len(q._jobs))
        q.append(3)
        self.assertEqual(3, len(q._jobs))
        q.append(4)
        self.assertEqual(4, len(q._jobs))
        q.append(5)
        self.assertEqual(5, len(q._jobs))

    def test_append_string_jobs(self):
        q = JobQueue(max_size=999, expiry_period=999)
        q.append('job1')
        q.append('job2')
        q.append('job3')
        q.append('job4')
        q.append('job5')
        self.assertEqual(5, len(q._jobs))

    def test_append_dups(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q._jobs))
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)
        self.assertEqual(4, len(q._jobs))
        last_job_time = q._jobs[4]

        time.sleep(0.1) # make sure that time moves on!
        q.append(4) # append a job that's already been added.
        self.assertEqual(4, len(q._jobs))   # Note: the job is replaced, not added..
        self.assertNotEqual(q._jobs[4], last_job_time) # but gets a new timestamp

    def test_remove(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q._jobs))
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)
        q.append(5)
        self.assertEqual(5, len(q._jobs))
        q.remove(3)
        self.assertEqual(4, len(q._jobs))
        q.remove(2)
        self.assertEqual(3, len(q._jobs))
        q.remove(4)
        self.assertEqual(2, len(q._jobs))
        q.remove(1)
        self.assertEqual(1, len(q._jobs))
        q.remove(5)
        self.assertEqual(0, len(q._jobs))

    def test_remove_NOT_EXISTS(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q._jobs))
        q.append(1)
        q.append(2)
        self.assertRaises(KeyError, q.remove, 999)  # Note: KeyError (dict-like), not ValueError (list-like)

    def test_is_full(self):
        q = JobQueue(max_size=3, expiry_period=999)
        self.assertFalse(q.is_full())
        q.append(1)
        self.assertFalse(q.is_full())
        q.append(2)
        self.assertFalse(q.is_full())
        q.append(3)
        self.assertFalse(q.is_full())
        q.append(4)
        self.assertTrue(q.is_full())

    def test_expired_ALL_EXPIRED(self):
        q = JobQueue(max_size=999, expiry_period=0.0000001)
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)
        self.assertEqual(4, len(q._jobs))
        time.sleep(0.1)

        expired_jobs = q.expired()
        self.assertEqual(4, len(expired_jobs))
        self.assertEqual((1,2,3,4), tuple(expired_jobs))    # should come out in expired order
        self.assertEqual(0, len(q._jobs))

    def test_expired_NO_EXPIRIES(self):
        q = JobQueue(max_size=999, expiry_period=60*1000)
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)
        self.assertEqual(4, len(q._jobs))

        expired_jobs = q.expired()
        self.assertEqual(0, len(expired_jobs))
        self.assertEqual(4, len(q._jobs))

    def test_expired_SOME_EXPIRED(self):
        expiry_time = 3 # must be able to get to step B in this time..

        q = JobQueue(max_size=999, expiry_period=expiry_time)
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)

        expired_jobs = q.expired()  # step B: nothing has expired yet.
        self.assertEqual(0, len(expired_jobs))
        time.sleep(expiry_time + 2) # wait for expiry
        q.append(5)
        q.append(6)

        expired_jobs = q.expired()
        self.assertEqual(4, len(expired_jobs))
        self.assertEqual((1,2,3,4), tuple(expired_jobs))    # should come out in expired order
        self.assertEqual(2, len(q._jobs))

    def test_str(self):
        q = JobQueue(max_size=999, expiry_period=999)
        q.append(1)
        q.append(2)
        q.append(3)
        q.append(4)

        self.assertEqual('[1, 2, 3, 4]', str(q))

    def test_size(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, q.size())

        q.append(1)
        q.append(2)
        q.append(3)

        self.assertEqual(3, q.size())

        q.remove(1)

        self.assertEqual(2, q.size())

    def test_len(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q))

        q.append(1)
        q.append(2)
        q.append(3)

        self.assertEqual(3, len(q))

        q.remove(1)

        self.assertEqual(2, len(q))


    def test_iteartion_protocol(self):
        q = JobQueue(max_size=999, expiry_period=999)
        self.assertEqual(0, len(q))

        q.append(1)
        q.append(2)
        q.append(3)

        self.assertEqual(3, len(q))

        jobs = []
        for job in q:
            jobs.append(job)

        self.assertEqual([1, 2, 3], jobs)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestJobQueue),
    ])

if __name__ == "__main__":
    unittest.main()
