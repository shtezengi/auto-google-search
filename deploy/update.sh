PROJECT_DIR=`dirname $0`/..
VIRTUAL_ENVIRONMENT=`dirname $0`/../../../virtualenv/

if [ -d "/vagrant/" ]; then
  VIRTUAL_ENVIRONMENT=~/virtualenv
fi

HOSTNAME=`hostname`
grep 'CentOS' /etc/redhat-release 2>&1 >/dev/null
ON_CENTOS=$?

PYTHON="${VIRTUAL_ENVIRONMENT}/bin/python"
if [ ! -f "${PYTHON}" ]; then
    echo "creating python virtualenv ${VIRTUAL_ENVIRONMENT}"
    virtualenv-2.7 $VIRTUAL_ENVIRONMENT
fi

${VIRTUAL_ENVIRONMENT}/bin/pip install -r "${PROJECT_DIR}/requirements.txt"
if [ "x$?" != "x0" ]; then
    echo "unable to install python dependencies.  check your network and try again."
    exit 1
fi

MANAGE=${PROJECT_DIR}/src/manage.py

$PYTHON $MANAGE migrate --noinput
$PYTHON $MANAGE collectstatic --noinput

