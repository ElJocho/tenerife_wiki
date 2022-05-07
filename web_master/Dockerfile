FROM python:3.8

# get pg to check for database status
RUN apt-get update && \
    apt-get install --yes --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# setup non root user for security reasons
RUN useradd -md /home/tenerife tenerife
WORKDIR /opt/tenerife
RUN chown tenerife:tenerife . -R
USER tenerife:tenerife
COPY --chown=tenerife:tenerife . .
ENV PATH "$PATH:/home/tenerife/.local/bin"
RUN pip install -r requirements.txt

