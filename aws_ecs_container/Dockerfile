FROM python:3.10.7-bullseye

# the WORKDIR within the container
WORKDIR /usr/src/auth_src

# the COPY from path is relative to the build context, not to the Dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y binutils libproj-dev gdal-bin vim

# These are non essential libraries
# RUN apt-get install -y net-tools

COPY ./ ./

#ENV HUGGINGFACE_HUB_CACHE=/ml_models/huggingface/diffusers/

#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]

# chmod +x makes the entrypoint.sh file executable (it gets execute permissions)
RUN chmod +x aws_ecs_container/entrypoint.sh

ENTRYPOINT ["aws_ecs_container/entrypoint.sh"]