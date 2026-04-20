FROM node:25-alpine3.21

LABEL maintener="William"

VOLUME [ "/var/nodeapp" ]

RUN adduser -h /var/nodeapp \
            -s /bin/bash \
            -D nodeapp

WORKDIR /var/node

COPY app.js .

RUN chown nodeapp:nodeapp app.js

EXPOSE 3000

ARG VERSION

ENV VERSION=${VERSION:-1.0.0}

USER nodeapp

CMD [ "node", "app.js" ]
