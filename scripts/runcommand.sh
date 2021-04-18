if [[ "$1" == "test" ]]; then
    docker-compose run app sh -c "python3 manage.py test"
# elif [[ "$1" == "runserver"]]; then
#     docker-compose run app sh -c "python3 manage.py runserver"
# elif [[ "$1" == "makemigrations"]]; then
#     docker-compose run app sh -c "python3 manage.py makemigrations $2"
# elif [[ "$1" == "migrate"]]; then
#     docker-compose run app sh -c "python3 manage.py migrate $2"
else
    echo "docker-compose run --rm app sh -c '.....'  : "
    read commandToRun
    
    docker-compose run app sh -c "python3 manage.py $commandToRun"
fi