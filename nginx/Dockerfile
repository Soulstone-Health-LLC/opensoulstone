FROM nginx:latest

# Remove the default.conf file
RUN rm /etc/nginx/conf.d/default.conf

# The temp.conf file is to allow the container to start without any errors and opens port 80
ADD conf.d/app.conf /etc/nginx/conf.d