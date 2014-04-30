#! /bin/bash
echo "HTTP/1.1 200 OK"
echo "Server: sub.domain.com"
echo "Content-Length: 10"
echo -e "Content-Type: text/html\n"
echo -e "goodbye\n"
