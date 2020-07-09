IMAGE="harbor.ctyun.dev:1443/function-compute/tplink-demo:$1"
sudo docker build . -t ${IMAGE}
sudo docker push ${IMAGE}
