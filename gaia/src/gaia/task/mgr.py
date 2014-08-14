import os
import socket
import zmq
import time
import cPickle as pickle
from abc import ABCMeta, abstractmethod
from collections import deque
from gaia.log.log import Log
from gaia.error import GaiaError
from gaia.task.job_queue import JobQueue
from gaia.task.msg.job_reply import JobReply
from gaia.task.send_recv import SendRecv
from gaia.task.manageable_task_process import ManageableTaskProcess

class Mgr(SendRecv, ManageableTaskProcess):
    ''' This base class provides all the functionality to send/receive jobs and
    handle outstanding requests.
    
    Subclasses *must* provide a jobs() method to provide jobs for the workers.
    '''
    __metaclass__ = ABCMeta
    _dispatch_pause = 1 # pause 1 second before sending each job (_very_ basic throttling!)
    process_name = 'mgr' # Note that this is used also as a log_name and a management_topic. Please override. 

    def __init__(self, job_sockets, config):
        self.config = config
        log_name = self.process_name
        fname = Log.configure_logging(log_name, config)

        print '=== WORKER STARTED with job_sockets="', str(job_sockets) ,'", config=', str(config)
        print "... logging to file: ", fname
        self._log = Log.get_logger(self)
        self._log.info('='*79)
        self._log.info('=== WORKER STARTED with :', job_sockets=job_sockets)
        self._log.info('config:...')
        self._log.info(str(config))
        self._log.info('-'*79)

        SendRecv.__init__(self, is_master=True, config=config)
        ManageableTaskProcess.__init__(self)

        self._id = str(os.getpid())
        self._hostname = socket.getfqdn()
        self._jobs_done_handled = True # when we start up, let's get some jobs first

        self.job_sockets = job_sockets
        self.management_sockets = config.management_sockets

        self._saved_state_fname = os.path.join(config.working_dir, '%s.state' % self.process_name)
        self._restore_state()

    def run(self):
        self._log.info('START -----------------------------------------------')
        self._log.info('Response Threshold', threshold=self.config.response_threshold)

        self._max_requests_outstanding = self.config.max_requests_outstanding
        self._response_threshold = self.config.response_threshold
        self._backlog = JobQueue(max_size=self._max_requests_outstanding, expiry_period=self._response_threshold)
        self._new_jobs = deque(self._startup_jobs) # a double-ended queue (FIFO), primed with any old, saved jobs

        context = self._setup_zmq()
        
        try:
            self._handle_msgs()
        except zmq.ZMQError, e:
            #if e.strerror == 'Context was terminated':  # eg by Ctrl-C/SIGTERM
            self._log.error('terminated with messaging error: "%s"' % str(e))
        except Exception, e:
            self._log.error('terminated with unexpected error: "%s"' % str(e))
        except (KeyboardInterrupt, SystemExit), e:
            self._log.error('terminated with KeyboardInterrupt.')

        # Add new adnin protocol: close all workers: wait for them to die; then ask mgr to die. (?)
        # TODO: status: backlog, jobs

        self._log.info('about to shutdown ...')
        self._save_state()
        self._teardown_zmq(context)
        self._log.info('END -----------------------------------------------')

    def _handle_msgs(self):
        self._log.enter()
        poller = zmq.Poller()
        SendRecv.register_with_poller(self, poller)
        ManageableTaskProcess.register_with_poller(self, poller)

        exit = False
        while not exit:
            self._log.info('-'*60)
            self._log.info('--- LOOP: outstanding requests = %s' % str(self._backlog))
            # handle incoming (replies or commands) ---------------
            self._log.debug('polling for work and/or management requests ...')

            socks = dict(poller.poll(0)) # don't wait (0 timeout)
            if ManageableTaskProcess.is_msg(self, socks):
                exit = self.handle_management()

            if not exit:
                if SendRecv.is_msg(self, socks):
                    self._handle_job_replies() #self._handle_job()

                # send new job requests -----------------------------------------
                self._send_jobs()

            self._log.debug('pausing %d seconds ...' % self.config.poll_interval)
            time.sleep(self.config.poll_interval)   # TODO: change this to loop around to increase responsiveness (by looping and testing cumulative time against poll interval rather than sleeping)

        self._log.exit()

    def _send_jobs(self):
        self._log.enter()

        if not self._new_jobs: # refill the job queue only if it's empty.
            new_jobs = self.jobs()      # see if there are any new jobs
            if new_jobs:                # if there are some, do the work
                self._new_jobs = deque(new_jobs)
                self._jobs_done_handled = False # once this new "batch" of jobs are processed, we'll need to handle the "jobs done" event again
            elif len(self._backlog) == 0 and not self._jobs_done_handled:
                # if all jobs have been dealt with (including new new-ones above), and this ("jobs done") event has not yet been handled
                # (note that this allows 2 consequtive releases to be handled as one).
                self._log.info('JOBS_DONE: The jobs have been done, calling the jobs_done handler')
                final_jobs = self.handle_jobs_done()
                self._new_jobs = deque(final_jobs)
                self._jobs_done_handled = True

        # deal with any old jobs that seem to have got lost
        for job in self._backlog.expired(): # Note this _removes_ expired jobs from the backlog, and returns them to the new jobs queue
            self._log.warning('re-queuing EXPIRED job (will try again after new jobs): %s' % job)
            self._new_jobs.appendleft(job) # put expired jobs back onto the _end_ of the job queue (to try again later, _after_ new jobs)

        # if the backlog isn't too big, deal with new requests
        if self._backlog.is_full():
            # let's wait to get replies for these jobs before sending out new requests
            self._log.warning('DELAYING dispatch: max outstanding requests (%d) reached (Please check that workers are okay)' % self._max_requests_outstanding)
        else:
            should_continue = True  # are there any more jobs to deal with? (if new jobs are exhausted, we're done for now).
            while should_continue:
                should_continue = self._send_next_job()

        self._log.exit()

    def _send_next_job(self):
        ''' get the next JobRequest and send it to workers
            or do nothing if no workers are available

            return whether or not there are more jobs that can be worked on at this point in time.
        '''
        self._log.enter()
        try:
            job_request = self._new_jobs.pop()  # FIFO (left to right queue) (IndexError when trying to pop an empty list)
        except IndexError, e:
            self._log.exit('NO more jobs.')
            return False # no more jobs

        self._log.info('--> dispatching new job ', job_request=job_request)
        time.sleep(self._dispatch_pause)

        self._backlog.append(job_request)

        try:
            # Note: we use NOBLOCK so that if there are no workers running, we can still
            # pick up management requests rather than block here forever.
            SendRecv.send(self, job_request.encode(), flags=zmq.NOBLOCK)

        except zmq.ZMQError, e:
            if e.errno == zmq.EAGAIN:  # due to NOBLOCK
                # not sent; so try again later (after undoing what we did just above)
                self._log.info('no workers to send to (or send did not complete for some other reason)?.', error=e) 
                self._backlog.remove(job_request)
                self._new_jobs.append(job_request)  # put back onto FRONT (right) of queue
                self._log.exit('more jobs, but cannot send.')
                return False # don't continue
            else:
                self._log.error('Got and re-raising ERROR: %s' % str(e))
                raise GaiaError('Messaging Error sending jobs: "%s".' % (str(e)))

        self._log.exit('more jobs...')
        return True # there are more jobs

    def _handle_job_replies(self):
        self._log.enter()
        try:
            while 1:    # get all the results that are available; then raise EAGAIN
                msg = SendRecv.recv(self, flags=zmq.NOBLOCK)

                reply = JobReply.decode(msg)
                self._log.info('Got REPLY', reply=reply)

                try:
                    original_request = reply.request()

                    if reply.is_try_again():
                        self._log.info('will retry on expiry (asked to TRY AGAIN later)', original_request=original_request)
                    else:
                        self._backlog.remove(original_request)

                except KeyError, e:
                    self._log.warning('Ignoring REPLY for unexpected job: "%s" (Err = "%s")' % (str(reply), str(e)))
                    
        except zmq.ZMQError, e:
            if e.errno == zmq.EAGAIN:
                self._log.info('no more results available.')   # due to NOBLOCK
            else:
                self._log.error('Got and re-raising ERROR: %s' % str(e))
                raise GaiaError('Messaging Error receiving results: "%s".' % (str(e)))

        self._log.exit()

    def _setup_zmq(self):
        context = zmq.Context() # WARNING: Should only be one of these per process!

        send_socket = self.job_sockets['request']['send']
        recv_socket = self.job_sockets['reply']['recv']
        self._log.info('sending jobs on', send_socket=send_socket)
        self._log.info('rceiving replies from jobs on', recv_socket=recv_socket)
        SendRecv.setup_zmq(self, send_socket, recv_socket, context)

        topic = self.process_name
        pub_socket = self.management_sockets['status']['send']
        sub_socket = self.management_sockets['command']['recv']
        ManageableTaskProcess.setup_zmq_slave(self, topic, pub_socket, sub_socket, context)
        
        return context

    def _teardown_zmq(self, context):
        self._log.enter()
        # Note: maybe send a "I'm dying" status message here?

        time.sleep(1) # was reqd to allow zmq to flush buffers, etc (?) # don't think is necessary anymore (ie infinite linger is default) TODO: review

        ManageableTaskProcess.teardown_zmq(self)
        SendRecv.teardown_zmq(self)
        
        context.term()
        #context.destroy(linger=self.term_timeout)   # note: based on document it should work, need further investigation?
        self._log.exit()

    def _restore_state(self):
        ' restore the state of jobs if we saved state on exit '
        if os.path.exists(self._saved_state_fname):
            state_file = open(self._saved_state_fname, 'rb')
            self._startup_jobs = pickle.load(state_file)
            state_file.close()

            os.remove(self._saved_state_fname)
            self._log.info('RESTORED SAVED JOBS', restored_jobs=self._startup_jobs)
        else:
            self._log.info('no saved jobs file', fname=self._saved_state_fname)
            self._startup_jobs = []

    def _save_state(self):
        ''' Save the state of jobs so that we can pickup on restart.
            There are 2 queues to save: new_jobs and backlog

            Note that we will re-try all of the backlog jobs even though they 
            may still be in progress with workers. In the worst case, we may
            re-try a job that's already been done (and this should work ok).
        '''
        
        jobs = self._new_jobs
        for job in self._backlog:
            jobs.append(job) # put onto the FRONT of the queue

        if len(jobs) > 0:
            state_file = open(self._saved_state_fname, 'wb')
            pickle.dump(jobs, state_file)
            state_file.close()

            self._log.info('SAVING JOBS', jobs=jobs, fname=self._saved_state_fname)
        else:
            self._log.info('SAVING JOBS: no jobs to save.')

    def status(self):
        ' return a status dictionary # Note: do NOT use the key: "status" '
        _status = {
            'type': 'MGR',
            'id': self._id,
            'hostname': self._hostname,
            'num_jobs': len(self._new_jobs),
            'num_backlog': len(self._backlog),
            'jobs': self._new_jobs,
        }
        return _status

    def handle_jobs_done(self):
        ''' If special processing is required each time a "batch" of jobs is finished, 
            this method should return extra JobRequest objects~ to do this.
            (eg to create feed files after converting a batch of jobs on release).
        '''
        return []   # no extra jobs to do (by default)

    @abstractmethod
    def jobs(self):
        ''' Return a list of JobRequest objects to be worked on.
            You *must* provide this in sub-classes.
        '''
        #raise NotImplementedError
        pass # will raise TypeError if not overridden.
