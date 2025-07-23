FROM apache/superset:latest

USER root

RUN pip install psycopg2-binary

USER superset

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]