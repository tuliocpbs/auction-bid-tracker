# Auction Bid Tracker

Auction system which will allow users to concurrently bid on items for sale.

> PS.: This auction allows the user to bid with a somaller value than the last one. =D

### Infrastructure

Each of the container above has a propose.

- Locust: Simulate user's bids and execute a load testing to measure performance of Bid API
- Auction: Responsible for auction's endpoints such as 
- Bid: RestAPI to interacte (create, update, delete, get, list) with bids
- APM elastic/Elasticsearch/Kibana: Implement APM to measure performance on aplications

![Auction Infrastructure Architecture](https://github.com/tuliocpbs/auction-bid-tracker/blob/master/images/auction-bid-tracker.png)

### Requirements to run this project

##### Docker - [Link for instrucitons](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

##### Docker Compose - [Link for instructions](https://docs.docker.com/compose/install/)

### Some configurations you can do, before run the project

**Items quantity**: Set the quantity in docker-compose file, line 26

### How to Run

###### Execute the commands bellow in sequence:

`$ git clone https://github.com/tuliocpbs/auction-bid-tracker.git`

`$ cd auction-bid-tracker`

`$ docker-compose up -d`

> Wait for all dependencies be up

> Dependes on your docker settings, you will need to set more memory so the elasticsearch stay up. For that you can use:

- **For linux SO**:
`$ sudo sysctl -w vm.max_map_count=262144`

- **For mac OS**:
Open Docker Desktop -> Select Resources -> Set more memory

### How to interact with the Application

##### Auction's API

API responsible for provide information about the auction, such as 

Access `Auction's swagger doc` : <http://localhost:5000/docs>

> To user any requests insert the Api-Key value on Authorize field

| Credentials | Value|
|------------|-------|
|Api-Key |secret-api-key |

Endpoints available:
- /api/v1/bidsofanitem (GET)
- /api/v1/currentlywinnig (GET)
- /api/v1/itemswithuserbids (GET)

##### Bid's RestAPI

API responsible for create, delete and provide information about bids.

Access `Bid's swagger doc` : <http://localhost:5001/docs>

> To user any requests insert the Api-Key value on Authorize field

| Credentials | Value|
|------------|-------|
|Api-Key |secret-api-key |

Endpoints available:
- /v1/bid (GET/DELETE/PUT)
- /v1/bids (GET)

### Monitoring with Elastic APM

> Wait for Kibana be up

###### Access `APM app on Kibana ` : <http://localhost:5601/app/apm>

### Perfomance test with Locustio

Test the performance of Bid RestAPI with Locust

###### Access `Locust ` : <http://localhost:8089/>

## Concurrency approach

In this project to deal with the concurrency caused by many users doing bids at the same time, was necessary create a lock on **bids** variable. I used a solution provide by Python's standart library, **threading**.

This example explains why this concurrency problem happens:
1. Two users (Ross and Chandler) try to do a bid on the same item (jewel) and in the same time.
2. To different threads get the all bids on this item.
3. The first thread (Ross's bid) update **bids** variable with Ross's bid.
4. The second thread (Chandler's bid) update **bids** variable with Chandler's bid, but based on the old data that **bids** contains, and this data is all bids without Ross's bid. Because of that, the aplication loses Ross's bid.
