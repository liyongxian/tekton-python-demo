FROM python:3.6-buster 

WORKDIR /workspace/
COPY . .

CMD ["echo hello"]
