export $(cat ../.environments.stage/.env.auth | xargs) &&
flask --app ../main create-user $SUPERUSER_USERNAME $SUPERUSER_PASSWORD $SUPERUSER_ROLE
