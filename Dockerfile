FROM node

WORKDIR /app

COPY view/package*.json /app/

RUN npm install

COPY /view/ /app/

EXPOSE 3000

CMD ["npm", "start"]