FROM nginx:latest

# Remove the default.conf file
RUN rm /etc/nginx/conf.d/default.conf

# The app.conf file
ADD conf.d/app.conf /etc/nginx/conf.d