#!/bin/bash

BASE_URL="http://18.228.211.17"
URL="${BASE_URL}/user-service/users/order"
echo $URL

while true; do
    # ===User service===
    # List users
    # curl "http://localhost:3000/users"

    # Place order
    curl -X POST -H "Content-Type: application/json" -d '{
        "user_id": "1",
        "product_ids": [1, 3],
        "quantities": [1, 3]
    }' $URL

    sleep 2
done
