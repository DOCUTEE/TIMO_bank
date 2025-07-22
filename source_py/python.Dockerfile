FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt ./requirements.txt

# Install dependencies + SSH server
RUN apt-get update && apt-get install -y openssh-server && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    mkdir /var/run/sshd

# Create a user for SSH
RUN useradd -m airflow_user && echo "airflow_user:airflow" | chpasswd

# Allow password login
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

COPY src/ .

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
