from fabric.api import *

# BOOM

@task
def production():
    env.forward_agent = True
    env.user = 'root'
    env.hosts = ['162.243.35.155']

@task
def backup():
    env.forward_agent = True
    env.user = 'root'
    env.hosts = ['162.243.234.7']
    
@task
def backup_sqlite_deploy():
    sudo ('mkdir -p /usr/lib/cytora')
    put ('backup-sqlite.py', '/usr/lib/cytora', use_sudo=True)

@task 
def rsync_deploy():
    put ('backup-rsync.sh', '/usr/lib/cytora', use_sudo=True)
    sudo ('chmod u+x /usr/lib/cytora/backup-rsync.sh')

@task
def create_daily_backup_rsync_cron_job():
    SCRIPT = ('/usr/lib/cytora/backup-rsync.sh')
    LOGFILE = '/var/log/rsync-backup.txt'
    cron = "@daily {} >> {} 2>&1".format(SCRIPT, LOGFILE)
    run('echo \"{}\" | crontab'.format(cron))

@task
def create_daily_backup_sqlite_cron_job():
    SCRIPT = ('/usr/lib/cytora/backup-sqlite.py')
    LOGFILE = '/var/log/sqlite-backup.txt'
    cron = "@daily {} >> {} 2>&1".format(SCRIPT, LOGFILE)
    run('echo \"{}\" | crontab'.format(cron))

@task
def create_daily_alert_check_cron_job():
    SCRIPT = ('/usr/lib/cytora/data-services-front-end/'
              'cytora/scripts/daily_alert_check.sh')
    LOGFILE = '/vagrant/log.txt'
    cron = "0 12 * * * {} >> {} 2>&1".format(SCRIPT, LOGFILE)
    run('echo \"{}\" | crontab'.format(cron))

#BOOTSTRAPS

@task
def production_backup():
    backup_sqlite_deploy()
    create_daily_backup_sqlite_cron_job()

@task 
def backup_backup():
    rsync_deploy()
    create_daily_backup_rsync_cron_job()
