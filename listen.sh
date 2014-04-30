#! /bin/bash
PORT=$1
echo "Listening on port $1"
echo "Logging requests to requests.log"
echo "PID of servers is $$"
while true; 
  do nc -l -p $PORT -e ./response.sh -vv >> requests.log; 
  date >> requests.log; 
done
