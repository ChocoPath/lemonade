<?php

use Illuminate\Support\Facades\Route;

// ...existing code...

Route::get('/', function () {
    return 'Hello World';
});

// ...existing code...

# filepath: /Users/worsleyquaye/Documents/lemonade/docker-laravel/hello-world-app/nginx.conf
server {
    listen 80;
    server_name localhost;

    root /var/www/public;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    location ~ /\.ht {
        deny all;
    }
}
