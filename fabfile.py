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
    run("crontab -l | {{ cat; echo '@daily {} >> {} 2>&1' ; }} | crontab -".format(SCRIPT, LOGFILE))

@task
def create_daily_backup_sqlite_cron_job():
    SCRIPT = ('/usr/lib/cytora/backup-sqlite.py')
    LOGFILE = '/var/log/sqlite-backup.txt'
    run("crontab -l | {{ cat; echo '@daily {} >> {} 2>&1' ; }} | crontab -".format(SCRIPT, LOGFILE)) 

#BOOTSTRAPS

@task
def production_backup():
    backup_sqlite_deploy()
    create_daily_backup_sqlite_cron_job()

@task 
def backup_backup():
    rsync_deploy()
    create_daily_backup_rsync_cron_job()
