FROM node:18

WORKDIR /usr/src/app

# Ensure dependencies are installed
COPY package*.json ./
RUN npm install

# Then copy the actual source code
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
