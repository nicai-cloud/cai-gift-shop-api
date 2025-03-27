Useful notes:

Analysis for a return statement such as "return Bag(**bag.to_dict())" in BagFeature class:
bag.to_dict() will return a BagModel like dict which include all fields except "deleted_at", "created_at" and "updated_at",
then Bag(**bag.to_dict()) will return a Bag object defined inside api.types.py

Useful stripe CLI commands:
stripe login --interactive
stripe payment_intents list --limit 3

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
Account1:
1. aws ecr create-repository --repository-name cai-gift-shop-api (once-off)
2. aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com
3. docker tag cai-gift-shop-api:1.0 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0
4. docker push 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0

Account2:
1. aws ecr create-repository --repository-name cai-gift-shop-api (once-off)
2. aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 476114150599.dkr.ecr.ap-southeast-2.amazonaws.com
3. docker tag cai-gift-shop-api:1.0 476114150599.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0
4. docker push 476114150599.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0

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
First EC2:
sudo certbot certonly --standalone -d goodyhub.duckdns.org
Second EC2:
sudo certbot certonly --standalone -d giftoz.duckdns.org

By default, when the certs are generated, they are located on EC2:
/etc/letsencrypt/live/goodyhub.duckdns.org/fullchain.pem and
/etc/letsencrypt/live/goodyhub.duckdns.org/privkey.pem

which are symbolic linked to /etc/letsencrypt/archive/goodyhub.duckdns.org/fullchain1.pem and /etc/letsencrypt/archive/goodyhub.duckdns.org/privkey1.pem

Symbolic linked files won't work for volumn mounts, the docker container will error out with file not found.
So to make it work, the certs files will need to be copied from /etc/letsencrypt/archive/goodyhub.duckdns.org/ to /etc/certs/

change permission of certs files so that they can be read:
sudo chmod 644 /etc/certs/fullchain.pem
sudo chmod 644 /etc/certs/privkey.pem

and then mount them like:
-v /etc/certs/:/app/certs/

To check a docker container's configuration, including mounts and networking (it works even for a stopped container):
sudo docker inspect <container_id> and volume mounts can be seen from the "Mounts" section

To run commands from a docker container's bash inside EC2 using a docker image:
Account1:
sudo docker run -it --rm -v /etc/certs/:/app/certs/ 940482453018.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0 /bin/bash
Account2:
sudo docker run -it --rm -v /etc/certs/:/app/certs/ 476114150599.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0 /bin/bash

Tail docker container logs inside EC2:
sudo docker logs -f <container_id>

To see the list of running docker containers inside EC2:
sudo docker ps

To see the entire list of docker containers EC2, including stopped ones:
sudo docker ps -a

If there are issues with starting ECS-service, it is very likely because of the container has insufficient CPU or memory.

Steps to create a new backend API in AWS:
1. Create a new IAM user (with new user group of full admin permission)
2. Create EC2
    1. Name - Cai’s gift shop
    2. AMI - Amazon Linux 2023 AMI
    3. Architecture - 64-bit (x86)
    4. Instance type - t2.micro
    5. No key pair for login
    6. Network settings
        1. Allow SSH traffic from Anywhere (0.0.0.0/0)
        2. Allow HTTPS traffic from the internet
        3. Allow HTTP traffic from the internet
    7. Default storage
    8. Create a new EC2-role called “ec2-role” which has the permission “AmazonEC2ContainerServiceForEC2Role” and "AmazonSESFullAccess"
    9. In EC2 console, click on Actions -> Security -> Modify IAM role, choose "ec2-role" as the IAM role so that the EC2 can be registered under the ECS cluster which will be created later on
    10. In the Security Groups section, for the security group “launch-wizard-2”, which is used by the created EC2, add Inbound rule of “Allow All traffic from All”
3. Launch EC2
4. Create a new subdomain in DuckDNS
    1. Create a new subdomain called giftoz.duckdns.org
    2. Update IP address of the subdomain to be that of the above EC2's public IP address, which can be found from AWS console's EC2 attribute
5. Install certbot - Inside EC2, run
    1. sudo yum install certbot
6. Generate Certs for EC2 - Inside EC2, run
    1. sudo certbot certonly --standalone -d giftoz.duckdns.org
7. Copy certificate files - Inside EC2, run the following commands:
    1. sudo mkdir -p /etc/certs
    2. sudo cp /etc/letsencrypt/archive/giftoz.duckdns.org/fullchain1.pem /etc/certs/fullchain.pem
    3. sudo cp /etc/letsencrypt/archive/giftoz.duckdns.org/privkey1.pem /etc/certs/privkey.pem
    4. (for certificate renewals only) sudo mv /etc/letsencrypt/archive/giftoz.duckdns.org/ /etc/letsencrypt/archive/16-03-2025-giftoz.duckdns.org/
7a. To check the expiry date of a certificate, run
    openssl x509 -in /etc/certs/fullchain.pem -noout -enddate
7b. If required, re-run steps 6 & 7 above to generate new certificates
7c. IMPORTANT! - Check the certificate's expiry date every 60 days
8. Create a new Programmatic Access key for the user:
    1. Inside IAM, select the user, under “Security credentials” tab, click on “Create access key”, then select “Command Line Interface (CLI)”, and click “Next”
    2. Download the .csv file
9. Go back to VSCode console and add another AWS account:
    1. code ~/.aws/credentials
    2. Add a new profile for the new AWS account
    3. code ~/.aws/config
    4. Add the new profile account
    5. Switch between AWS account: export AWS_PROFILE=account1 (or $Env:AWS_PROFILE="account1" for Powershell and set AWS_PROFILE=account1 on Windows)
    6. Check current AWS account: aws sts get-caller-identity
10. Get ready to work with AWS:
    1. Build docker image
    2. Tag the image
    3. Create a new registry in ECR (once-off)
    4. Push the docker image to ECR
    5. Create a new ECS cluster called “Cai-gift-shop-cluster” without any ASG (auto-scaling group)
    6. Add EC2 to the created ECS cluster, inside EC2, run:
        1. sudo yum install -y ecs-init
        2. sudo echo "ECS_CLUSTER=Cai-gift-shop-cluster" >> /etc/ecs/ecs.config
        3. sudo systemctl enable --now ecs
        4. Go to ECS -> "Infrastructure" tab, and make sure the EC2 shows up in the Container instances list
    7. Create a new Task definition:
        1. Launch type of AWS EC2 instances
        2. Architecture - Linux/X86_64
        3. Network mode - host
        4. CPU - 1 vCPU
        5. Memory - 0.8GB
        6. Task role -
        7. Task execution role - Create new role
        8. Container - 1:
            1. Name: Cai-gift-shop
            2. Image URI: 476114150599.dkr.ecr.ap-southeast-2.amazonaws.com/cai-gift-shop-api:1.0
            3. Container port: 8080
            4. Port name: cai-gift-shop-8080-tcp
            5. Resource allocation limits:
                1. CPU - 0.8
                2. Memory hard limit - 0.8
            6. Add environment variables
            7. De-select "Use log collection"
        9. Add volume:
            1. Volume name: certs-volume
            2. Configuration type - Configure at task definition creation
            3. Volume type - Bind mount
            4. Source path - /etc/certs/
            5. Add Container mount points:
                1. Container: Cai-gift-shop
                2. Source volume: certs-volume
                3. Container path: /app/certs/
        10. Create the task definition
        11. Create a new service with the above task definition
        12. If the deployment failed, go to Cluster -> Cai-gift-shop-cluster -> Services -> cai-gift-shop-api -> Deployments -> See the Events at the bottom for error logs
        13. Address auto-complete uses Amazon Location Service. To use it, from AWS console, go to Amazon Location Service, from the left panel, go to “Manage Resources” -> “Maps, Places, routes” -> “Places” tab, then click on “Create place index”, choose “HERE” as Data Provider, once it is created, add “address-lookup” policy in ec2-role in IAM.
11. Create a Budget alert in the admin account:
    1. Go to "Billing and Cost Management" -> "Budgets" -> Click on "Create budget" -> Choose "Zero-Spend Budget"
12. To use SES to send email:
    1. Go to SES and create an entity with "nicai.goodyhub@gmail.com", verify it when receiving email
    2. Go to IAM role ec2-role and attach AmazonSESFullAccess policy to it
 