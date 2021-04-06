export FLASK_ENV=development
export FLASK_APP=tt

# default is port 6677 but you can
# add a new --port NNNN when calling run_flask.sh and that will be used
flask run --port 7766 --without-threads $*
