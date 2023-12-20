FROM node
COPY ./ansible_runner /ansible_runner
WORKDIR /ansible_runner
ENV NODE_OPTIONS=--openssl-legacy-provider

RUN npm install --global serve && npm run build


CMD serve -s ./build
