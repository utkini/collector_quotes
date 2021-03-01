from base import collect_data

from apscheduler.schedulers.blocking import BlockingScheduler

from logger import LOG

LOG.info('Starting')
sched = BlockingScheduler()
sched.add_job(collect_data, 'interval', hours=1)

sched.start()
