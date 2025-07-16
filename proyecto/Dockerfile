FROM php:8.2-apache

RUN docker-php-ext-install mysqli pdo pdo_mysql

# Opcional: para ver errores en el navegador
RUN echo "display_errors=On\nerror_reporting=E_ALL" > /usr/local/etc/php/conf.d/docker-php-errors.ini
