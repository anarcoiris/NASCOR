FROM debian:bullseye

RUN apt update && apt install -y \
  apache2 \
  gcc \
  libmariadb-dev \
  apache2-bin \
  apache2-utils \
  apache2-suexec-pristine \
  apache2-suexec-custom \
  curl \
  build-essential \
  && a2enmod cgi

COPY doom-web /var/www/html/doom-web
COPY datos /var/www/html/datos
COPY cgi-bin/tu_api.c /usr/lib/cgi-bin/
RUN gcc /usr/lib/cgi-bin/tu_api.c -o /usr/lib/cgi-bin/tu_api && chmod +x /usr/lib/cgi-bin/tu_api

COPY cgi.conf /etc/apache2/conf-available/cgi.conf
RUN a2enconf cgi.conf
RUN gcc /usr/lib/cgi-bin/tu_api.c -o /usr/lib/cgi-bin/tu_api && chmod +x /usr/lib/cgi-bin/tu_api

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
