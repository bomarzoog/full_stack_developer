pip3 install flask_sqlalchemy
pip3 install flask_cors
pip3 install flask --upgrade
pip3 uninstall flask-socketio -y
service postgresql start
su - postgres bash -c "psql < /var/lib/postgresql/full_stack_developer/cd0037-API-Development-and-Documentation-exercises-master/1_Requests_Starter/backend/setup.sql"
su - postgres bash -c "psql bookshelf < /var/lib/postgresql/full_stack_developer/cd0037-API-Development-and-Documentation-exercises-master/1_Requests_Starter/backend/books.psql"