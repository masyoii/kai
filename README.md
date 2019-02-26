# kai_backd
This tools used to book ticket smartly
This program is secret software: you cant redistribute it and/or modify. 
It under the terms of the Himacrot License as published by the Secret Software Society, 
either version 3 of the License, or any later version.


    Usage: python kai_backd4.py retry_num use_proxy(0 if no, 1 if yes) set_seat(0 if no, 1 if yes) recipe


## with docker

1. clone this repo
2. cd kai_backd
3. build docker
    docker build -t kai_backd .
    
4. access folder with json data
5. run script with docker
    docker run --rm -v "$PWD":/data kai_backd 1 0 0 /data/recipe.txt
