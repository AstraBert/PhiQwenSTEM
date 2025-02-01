FROM node:18-alpine

WORKDIR /ui/
COPY . /ui/

RUN npm install

ENTRYPOINT ["npm", "run", "dev"]