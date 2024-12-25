Useful notes:

To use Amazon Location Service to address auto-complete:
1. Log into AWS console
2. Go to Amazon Location Service
3. On the left menu, click on "Maps, places, routes"
4. Click on the "Places" tab
5. Click on the "Create place index" button and name it "AustraliaAddressIndex" and select "HERE" as Data Provider and create the place index
6. After the index is created, reference it in the python code
7. Attach an inline-policy to EC2 role so that it is allowed for Action "geo:SearchPlaceIndexForSuggestions" on the above created resource "arn:aws:geo:ap-southeast-2:940482453018:place-index/AustraliaAddressIndex"

To build and run docker container locally:
docker build -t cai-gift-shop-api .
docker run --env-file .env -p 8888:8080 cai-gift-shop-api

To build docker container for aws:
docker build --platform linux/amd64 -f Dockerfile_aws -t cai-gift-shop-api:1.0 .

Commands to push a docker image to ECR (Remember to delete existing docker image before pushing a new one so it is always within the storage limit):
1. aws ecr create-repository --repository-name cai-gift-shop-api (once-off)
2. aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com
3. docker tag cai-gift-shop-api:1.0 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0
4. docker push 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0

To make the hosted API inside docker container accessible, the network mode
of the ECS task definition has to be host, cannot be awsvpc, and port mapping
is also required to to make the API inside docker container accessible from
EC2's public IP address.

It is also worth nothing that the task definition's CPU and Memory hard/soft limit
has to be less than that of EC2's, since the EC2 is almost guaranteed to have run
something that consumes a bit of CPU and memory. (for example, 0.8 CPU and 0.8 memory
for task definition with 1 CPU and 1 memory for EC2, t2.micro).

1. To run the backend API in http mode, docker build with Dockerfile
2. To run the backend API in https mode, docker build with Dockerfile_aws

Running frontend locally doesn't need backend with http, but
running frontend in netlify does need backend with https, so
to make backend https, we need to add certs to the certs running on EC2.

Since backend doesn't currently have its own domain, I've used DuckDNS (Dynamic DNS (DDNS) service)
to register a subdomain, and linked EC2's public IP address to that subdomain,
then I was able to generate certs for the subdomain.

To generate certs for the domain on EC2:
sudo certbot certonly --standalone -d goodyhub.duckdns.org

By default, when the certs are generated, they are located on EC2:
/etc/letsencrypt/live/goodyhub.duckdns.org/fullchain.pem and
/etc/letsencrypt/live/goodyhub.duckdns.org/privkey.pem

which are symbolic linked to /etc/letsencrypt/archive/goodyhub.duckdns.org/fullchain1.pem and /etc/letsencrypt/archive/goodyhub.duckdns.org/privkey1.pem

Symbolic linked files won't work for volumn mounts, the docker container will error out with file not found. To make it work, the certs files will need to be copied from /etc/letsencrypt/archive/goodyhub.duckdns.org/ to /etc/certs/

change permission of certs files so that they can be read:
sudo chmod 644 /etc/certs/fullchain.pem
sudo chmod 644 /etc/certs/privkey.pem

and then mount them like:
-v /etc/certs/:/app/certs/

To check a docker container's configuration, including mounts and networking (it works even for a stopped container):
sudo docker inspect <container_id> and volume mounts can be seen from the "Mounts" section

To run commands from a docker container's bash inside EC2 using a docker image:
sudo docker run -it --rm -v /etc/certs/:/app/certs/ 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0 /bin/bash

Tail docker container logs inside EC2:
sudo docker logs -f <container_id>

To see the list of running docker containers inside EC2:
sudo docker ps

To see the entire list of docker containers EC2, including stopped ones:
sudo docker ps -a
