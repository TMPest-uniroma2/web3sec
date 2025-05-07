FROM node:18

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

# Fa in modo che si possa eseguire `walletlab` come comando
RUN chmod +x cli.js && npm link

CMD ["tail", "-f", "/dev/null"]
