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
    ```
    docker build -t kai_backd .
    ```
    
4. access folder with json data
5. run script with docker
    ```
    unix    -> docker run --rm -v "$PWD":/data kai_backd 1 0 0 /data/recipe.txt
    windows -> docker run --rm -v %cd%:/data kai_backd 1 0 0 /data/recipe.txt
    ```

6. profit

## with katacoda -> free docker playground online

1. open link https://www.katacoda.com/courses/docker/playground
2. create folder projects
    ```
    mkdir projects
    ```
3. cd to folder projects
    ```
    cd projects
    ```
4. git setting to folder projects
    ```
    git init
    ```
5. pull this repo
    ```
    git pull https://github.com/macbook47/kai_backd/
    ```
6. edit recipe.txt with your data -> kalau gak tau vi, googling dl aja :P
    ```
    vi recipe.txt
    ```
7. build docker
    ```
    docker build -t kai_backd .
    ```
8. run docker
    ```
    docker run kai_backd 1 0 0 recipe.txt
    ```
9. profit


## json recipe detail

line 1 is user pass kai mobile -> 
```
{"password": -> password mobile kai, "username": -> password mobile kai}
```


line 2 is passenger data ->
```
{
  "address": "Gedung IT BRI Jakarta", -> alamat mu ndes, ojo di isi akhirat yo
  
  "date_return": "20180318", -> your date return -> isi aja kayak dep date
  
  "dep_date": "20180318", -> your depature date -> tgl keberangkatan
  
  "des": "CN", -> stasiun tujuan -> untuk kode cek aja di web kai
  
  "email": "macbook.47@gmail.com", -> email nanti yg nerima notif
  
  "isreturn": false, -> kalo mau bolak balik
  
  "name": "Jehan Rachmatika", -> nama yg pesen
  
  "num_pax_adult": "2", -> jumlah penumpang dewasa -> menentukan jumlah array di penumpang dewasa
  
  "num_pax_infant": "1", -> jumlah penumang anak -> menentukan jumlah array di penumpang anak, klo 0 gak usah diisi json nya
  
  "org": "GMR", -> stasiun keberangkatan -> untuk kode cek aja di web kai
  
  "passenger": { -> data penumpang
    "adult": [ 
      {
        "birthdate": "19110101",
        "id_no": "3201111101110009",
        "mobile": "085111111110",
        "name": "harry potter"
      },
      {
        "birthdate": "19110609",
        "id_no": "347101010111003",
        "mobile": "081111111119",
        "name": "marvolo riddle"
      }
    ],
    "infant": [
      {
        "birthdate": "20110110",
        "name": "Dumbbledore"
      }
    ]
  },
  
  "phone": "085111111110", -> no hape pemesan
  
  "subclass": "X", -> kelas keretanya -> kode bisa di liat di web kai
  
  "subclass_return": "", -> kelas kereta klo pesen bolak balik
  
  "train_no": "16", -> kode kereta nya -> kode bisa di liat di web kai
  
  "train_no_return": 0
  
}
```


line 3 is seat data -> jumlah aray json sesuai dg penumpang dewasa -> masih ada bug -> coba2 sendiri aja yes :P

```
{"seat": "9A","wagon_code": "EKS","wagon_no": "3"},{"seat": "9B","wagon_code": "EKS","wagon_no": "3"}
```
