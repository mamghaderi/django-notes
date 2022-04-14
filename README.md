# Backend Coding Challenge

[![Build Status](https://github.com/Thermondo/backend-code-challenge/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/Thermondo/backend-code-challenge/actions)


### Application:

* Users can add, delete and modify their notes
* Users can see a list of all their notes
* Users can filter their notes via tags
* Users must be logged in, in order to view/add/delete/etc. their notes

### Developed endpoints:

* /admin: GET endpoint for admin panel usages. 
  * Please create a superuser in container manually to login in admin panel
  * Use This panel to add new user
* /api-token-auth/: POST endpoint for get user's token
  * pass username and password of you created user, to get its token. 
  * This token will be used in Authentication required endpoints
  * Example:

        curl --location --request POST 'http://0.0.0.0:8000/api-token-auth/' --header 'Content-Type: application/json' \
        --data-raw '{
          "username": "serveh3",
          "password": "dreadlord"
        }'
* /tags: GET endpoint for list of tags.
  * It does not need any authentication
  * Example:

         curl --location --request GET 'http://0.0.0.0:8000/tags'


* /notes: All rest endpoint for managing note features
  * If no authentication provided, it will return public notes
  * 'tags' can be used as query param to filter notes by tag
  * Example:

        # Get notes by Anonymous user
        curl --location --request GET 'http://0.0.0.0:8000/notes'

        # Get notes by Authenticate user
        curl --location --request GET 'http://0.0.0.0:8000/notes' --header 'Authorization: Token 6ccbc00d2251c0bdb4ee7e2f65eced63721f4d07'

        # Create notes
        curl --location --request GET 'http://0.0.0.0:8000/notes' \
        --header 'Authorization: Token 6ccbc00d2251c0bdb4ee7e2f65eced63721f4d07' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "title7",
            "body": "body1",
            "tags": ["tag1"],
            "public": true
        }'

        # Filter notes by tags
        curl --location --request GET 'http://0.0.0.0:8000/notes?tags=tag1&tags=tag2' \
        --header 'Authorization: Token 6ccbc00d2251c0bdb4ee7e2f65eced63721f4d07' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "title": "title7",
            "body": "body1",
            "tags": ["tag1"],
            "public": true
        }'
