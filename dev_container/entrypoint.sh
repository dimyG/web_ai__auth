#!/bin/sh
# * The #!/bin/sh shebang specifies that the script should be run with the /bin/sh shell,
#   which is a standard shell in many Unix-like operating systems.

# * The file is executed from the WORKDIR directory as defined in the Dockerfile so the path to files are relative
#   to WORKDIR and not to the file's position

# * Notice that the EOL character of this file must be UNIX style (LF) otherwise you will get an error when the
#   script runs in the container

# I use the cache_dir argument instead of setting the HUGGINGFACE_HUB_CACHE environment variable (couldn't make it work)
# set the huggingface cache directory from which the models are downloaded and read from. We set it to the path
# in which we stored the models in the docker image so that we don't have to download them again in the container.
#export HUGGINGFACE_HUB_CACHE='/usr/src/model_scheduler_src/ml_models/huggingface/diffusers/'

# set -e sets a shell option to immediately exit if any command being run exits with a non-zero exit code.
# The script will return with the exit code of the failing command.
set -e

python manage.py start_consumer_thread &  # the & makes the command to run in the background so that it doesn't block the script
export CONSUMER_THREAD_PID=$! # the $! variable contains the return value of the most recently executed background process
echo "Consumer thread started with PID: $CONSUMER_THREAD_PID"
#python manage.py runserver 0.0.0.0:8000
gunicorn auth_prj.wsgi --bind 0.0.0.0:8000 --log-level info --capture-output --timeout 60 --reload

# It basically takes all the extra command line arguments and execs them as a command. The intention is basically
# "Do everything in this .sh script, then in the same shell run the command the user passes in on the command line".
exec "$@"
