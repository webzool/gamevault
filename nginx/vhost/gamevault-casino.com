

auth_basic "Restricted Content";
auth_basic_user_file /gamevaultcasino/nginx/.htpasswd;

location /static/ {
    alias /gamevaultcasino/static/;
}

location /media/ {
    alias /gamevaultcasino/media/;
}



location = /about/index.html {
   rewrite ^/about/index.html(.*)$ https://gamevault-casino.com/about/ permanent;
}

location = /faq/index.html {
   rewrite ^/faq/index.html(.*)$ https://gamevault-casino.com/faq/ permanent;
}

location = /contact/index.html {
   rewrite ^/contact/index.html(.*)$ https://gamevault-casino.com/contact/ permanent;
}

location = /games/index.html {
   rewrite ^/games/index.html(.*)$ https://gamevault-casino.com/games/ permanent;
}

location = /terms-and-conditions/index.html {
   rewrite ^/terms-and-conditions/index.html(.*)$ https://gamevault-casino.com/terms-and-conditions/ permanent;
}

location = /privacy-policy/index.html {
   rewrite ^/privacy-policy/index.html(.*)$ https://gamevault-casino.com/privacy-policy/ permanent;
}
