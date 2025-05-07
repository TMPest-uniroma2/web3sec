FROM mythril/myth:latest

WORKDIR /usr/src/app

# Install jq (opzionale, utile per parsing JSON output)
RUN apt-get update && apt-get install -y jq

ENTRYPOINT [ "myth" ]
