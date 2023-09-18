FROM nginx:1.25-alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/conf.d
COPY conf.d/00_default.conf /etc/nginx/conf.d/00_default.conf
COPY conf.d/01_api_http.conf /etc/nginx/conf.d/01_api_http.conf.bak
COPY conf.d/02_api_https.conf /etc/nginx/conf.d/02_api_https.conf.bak

COPY 404.html /usr/share/nginx/html/404.html

COPY start /start
RUN chmod +x /start
CMD /start
