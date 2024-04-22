FROM node

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY /view/ /app/

EXPOSE 3000

CMD ["npm", "start"]