echo "docker-compose run --rm app sh -c 'python3 manage.py .....'  : "
read commandToRun
    
docker-compose run app sh -c "python3 manage.py $commandToRun"
