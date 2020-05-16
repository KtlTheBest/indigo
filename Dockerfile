FROM python3

ADD https://api.github.com/KtlTheBest/indigo/commits/local_hosted
RUN git clone https://github.com/KtlTheBest/indigo
WORKDIR indigo
RUN git checkout local_hosted

CMD ["python3", "main.py"]
