#
# Docker CMS, (c) 2017 BachNX
# Website: http://ngobach.com
# 

# Base image
FROM ubuntu:14.04
# Change repository to some fast mirror
RUN sed -iE 's/archive.ubuntu.com/opensource.xtdv.net/' /etc/apt/sources.list
# Essentials packages
RUN apt-get update && apt-get install -y build-essential postgresql postgresql-client \
	gettext python2.7 python-setuptools python-tornado python-psycopg2 \
	python-sqlalchemy python-psutil python-netifaces python-crypto \
	python-tz python-six iso-codes shared-mime-info stl-manual \
	python-beautifulsoup python-mechanize python-coverage python-mock \
	cgroup-lite python-requests python-werkzeug python-gevent patool
RUN apt-get install -y wget python-pip python-dev libcups2-dev
# Download CMS
ADD ./cms /cms
WORKDIR /cms
RUN pip install -r REQUIREMENTS.txt
RUN ./setup.py build && ./setup.py install

# Configure db
RUN service postgresql start && \
	su - postgres -c 'printf "nope\nnope\n" | createuser --username=postgres -P cmsuser' && \
    su - postgres -c 'createdb --username=postgres --owner=cmsuser database' && \
    su - postgres -c 'psql --username=postgres --dbname=database --command="ALTER SCHEMA public OWNER TO cmsuser"' && \
    su - postgres -c 'psql --username=postgres --dbname=database --command="GRANT SELECT ON pg_largeobject TO cmsuser"' && \
	sed -iE 's/cmsuser:password/cmsuser:nope/;s/"admin_listen_address": ""/"admin_listen_address": "0.0.0.0"/' /usr/local/etc/cms.conf

# Finally
ADD ./bachnx.sh /entrypoint.sh
ADD ./contest /contest
EXPOSE 8888 8889 8890
VOLUME /contest
ENTRYPOINT /entrypoint.sh
