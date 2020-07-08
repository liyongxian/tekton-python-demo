FROM harbor.ctyun.dev:1443/function-compute/python:3.6-alpine3.11 

WORKDIR /workspace/
COPY . .

CMD ["echo hello"]
