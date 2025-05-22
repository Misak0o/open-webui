FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y nmap whois net-tools curl wget iputils-ping netbase && apt-get clean && useradd -ms /bin/bash sandbox

USER sandbox

WORKDIR /home/sandbox

CMD ["bash"]
