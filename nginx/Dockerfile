FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf

# The temp.conf file is to allow the container to start without any errors and opens port 80
ADD conf.d/temp.conf /etc/nginx/conf.d

# The app.conf file is the actual configuration file for the application with SSL enabled
#ADD conf.d/app.conf /etc/nginx/conf.d