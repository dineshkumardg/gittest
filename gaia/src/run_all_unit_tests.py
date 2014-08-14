'''
TODO have it so that run_all_unit_tests can be run inside eclipse (but it works just fine in pycharm)
= get round unicode issues
'''
import argparse
import unittest
from coverage import coverage
from cStringIO import StringIO


def run_in_parallel():
    from testing.test_suite_cengage import TestSuiteCengage
    from testing.test_suite_gaia import TestSuiteGaia
    from testing.test_suite_project import TestSuiteProject
    from testing.test_suite_project_doc import TestSuiteProjectDoc
    from testing.test_suite_project_doc2 import TestSuiteProjectDoc2
    from testing.test_suite_project_doc3 import TestSuiteProjectDoc3
    from testing.test_suite_qa import TestSuiteQA

    processes = []
    processes.append(TestSuiteCengage())
    processes.append(TestSuiteGaia())  # TODO 1 tmp folder left behind
    processes.append(TestSuiteProject())  # TODO n tmp folders left behind
    processes.append(TestSuiteProjectDoc())  # TODO n tmp folders left behind
    processes.append(TestSuiteProjectDoc2())  # TODO n tmp folders left behind
    processes.append(TestSuiteProjectDoc3())  # TODO n tmp folders left behind
    processes.append(TestSuiteQA())

    try:
        for process in processes:
            process.start()

        for process in processes:
            process.join(60 * 3)  # 3 mins to wait in total :-(
            queue_dict = process.queue.get()
            process.print_results(queue_dict['standard_results'])
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()


def run_coverage(limited=False):
    omit = ['*__init__*', '*/__init__*', '*/test_*']
    if limited:
        omit.extend(['*log/log*', '*run_all_unit_tests'])

    stats = coverage(omit=omit)
    stats.start()

    # imports are required inside the coverage!
    if limited:
        tests = _get_current_dev_work()
    else:
        tests = _get_tests()

    results = StringIO()
    for test in tests:
        unittest.TextTestRunner(stream=results, verbosity=2).run(test)

    stats.stop()
    output = StringIO()
    stats.report(file=output)
    if limited:
        print '\n' + output.getvalue()
    else:
        fname = open(',coverage.txt', 'w')
        fname.write(output.getvalue())
        fname.close()


def _get_current_dev_work():
    import scripts.reports.author.test_generate_author_report
    return [scripts.reports.author.test_generate_author_report.suite]


def _get_tests():
    from testing.test_suite_cengage import TestSuiteCengage
    from testing.test_suite_gaia import TestSuiteGaia
    from testing.test_suite_project import TestSuiteProject
    from testing.test_suite_project_doc import TestSuiteProjectDoc
    from testing.test_suite_project_doc2 import TestSuiteProjectDoc2
    from testing.test_suite_qa import TestSuiteQA

    all_tests = []
    all_tests.extend(TestSuiteCengage().standard_tests)
    all_tests.extend(TestSuiteGaia().standard_tests)
    all_tests.extend(TestSuiteProject().standard_tests)
    all_tests.extend(TestSuiteProjectDoc().standard_tests)
    all_tests.extend(TestSuiteProjectDoc2().standard_tests)
    all_tests.extend(TestSuiteQA().standard_tests)
    return all_tests


# py run_all_unit_tests.py
# py run_all_unit_tests.py --mode=run_coverage
# py run_all_unit_tests.py --mode=run_limited_coverage
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='run_in_parallel', choices=['run_in_parallel', 'run_coverage', 'run_limited_coverage'])
    args = parser.parse_args()

    if args.mode == 'run_coverage':
        run_coverage()
    elif args.mode == 'run_limited_coverage':
        run_coverage(limited=True)
    else:
        run_in_parallel()
