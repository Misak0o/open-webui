FROM alpine:latest

# Installation des outils que l'on veut (peut être amené à évoluer si on en a besoin d'autre)
RUN apk add --no-cache \
    bash \
    curl \
    wget \
    nmap \
    netcat-openbsd \
    tcpdump \
    wireshark-common \
    bind-tools \
    openssh-client \
    python3 \
    py3-pip \
    sudo \
    shadow \
    && apk del --purge \
    && rm -rf /var/cache/apk/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Création d'un user qui n'est pas root
RUN addgroup -g 1000 sandbox && \
    adduser -D -u 1000 -G sandbox -s /bin/bash sandbox && \
    echo "sandbox:sandbox" | chpasswd

# Ajout sudoers car tcpdump en a besoin
RUN echo "sandbox ALL=(ALL) NOPASSWD: /usr/bin/tcpdump" >> /etc/sudoers

RUN chown -R sandbox:sandbox /home/sandbox && \
    chmod 750 /home/sandbox

# Pour retirer le bit SUID aux fichiers, supprimer la création de fichiers non autorisé, sécurise les fichiers d'authentification
RUN find /usr/bin /bin /sbin /usr/sbin -perm -4000 -exec chmod u-s {} \; && \
    find / -type d -perm -002 -exec chmod o-w {} \; 2>/dev/null || true && \
    chmod 600 /etc/shadow && \
    chmod 644 /etc/passwd && \
    chmod 644 /etc/group && \
    rm -f /root/.ash_history && \
    rm -f /home/sandbox/.ash_history && \
    mkdir -p /tmp/sandbox && \
    chown sandbox:sandbox /tmp/sandbox && \
    chmod 1700 /tmp/sandbox

# De ce que j'ai compris ça limite le nombre de fichiers et processus ouverts
RUN echo "* soft nofile 1024" >> /etc/security/limits.conf && \
    echo "* hard nofile 2048" >> /etc/security/limits.conf && \
    echo "* soft nproc 256" >> /etc/security/limits.conf && \
    echo "* hard nproc 512" >> /etc/security/limits.conf


# On définit le user par defaut et où il va travailler
USER sandbox
WORKDIR /home/sandbox

# Mieux de définir des variables d'environnement
ENV HOME=/home/sandbox
ENV USER=sandbox
ENV TMPDIR=/tmp/sandbox
ENV SHELL=/bin/bash

CMD ["bash"]
