from fabric.api import *

# BOOM

@task
def production():
    env.forward_agent = True
    env.user = 'root'
    env.hosts = ['208.68.39.191']

@task
def backup():
    env.forward_agent = True
    env.user = 'root'
    env.hosts = ['162.243.234.7']
    
@task
def backup-sqlite_deploy():
    sudo ('mkdir -p /usr/lib/cytora')
    put ('backup-sqlite.py', '/usr/lib/cytora', use sudo=True)

@task 
def rsync_deploy();
    put ('backup-rsync.sh', '/usr/lib/cytora', use sudo=True)
    sudo ('chmod u+x /usr/lib/cytora/backup-rsync.sh')

@task
def create_daily_backup-rsync_cron_job():
    SCRIPT = ('/usr/lib/cytora/backup-rsync.sh')
    LOGFILE = '/var/log/rsync-backup.txt'
    cron = "@daily {} >> {} 2>&1".format(SCRIPT, LOGFILE)
    run('echo \"{}\" | crontab'.format(cron))

@task
def create_daily_backup-sqlite_cron_job():
    SCRIPT = ('/usr/lib/cytora/backup-sqlite.py')
    LOGFILE = '/var/log/sqlite-backup.txt'
    cron = "@daily {} >> {} 2>&1".format(SCRIPT, LOGFILE)
    run('echo \"{}\" | crontab'.format(cron))
