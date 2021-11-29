FROM python:buster
COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN export DEBUG_METRICS=false && chmod +x /app/docker-entrypoint.sh
EXPOSE 7000
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]