FROM python:3

RUN pip3 install python-telegram-bot requests bs4 pytz

#ADD https://api.github.com/repos/KtlTheBest/indigo/git/refs/heads/local_hosted version.json
#RUN git clone https://github.com/KtlTheBest/indigo

COPY . /indigo
WORKDIR /indigo
RUN git checkout local_hosted

CMD ["python3", "main.py"]
