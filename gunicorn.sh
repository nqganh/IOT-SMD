#!/bin/bash
set -e
LOGFILE=/var/log/iot_admin.log
LOGDIR=$(dirname $LOGFILE)

# The number of workers is number of worker processes that will serve requests.
# You can set it as low as 1 if you?~@~Yre on a small VPS.
# A popular formula is 1 + 2 * number_of_cpus on the machine (the logic being,
# half of the processess will be waiting for I/O, such as database).
NUM_WORKERS=3

# user/group to run as
USER=www-data
GROUP=www-data

cd /var/www/iot_admin

test -d $LOGDIR || mkdir -p $LOGDIR

#Execute unicorn
exec gunicorn project.wsgi:application -b 127.0.0.1:8123 -w $NUM_WORKERS --timeout=300 \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
