# AlertVisionV2

- Updated version of older project AlertVision with messaging queues and new advancments.

## Tech Stack

**Languages**: Python, Go, Javascript

**Frameworks/Technologies**: React.js, FastAPI, AWS S3, Docker Compose, OpenAI API

**Message Brokers**: RabbitMQ


## What Does This Project Do?

- This project is an expansion of a previous project done before where live camera feeds or surveillance clips are analyzed in the backend for human detection and detected frames are email to user and stored in Amazon S3.

- The architecture has been changed which is reflected upon ths project. Instead of using clips of footage, it has been switched into using public youtube live streams that are accessible. Backend includes the use of FastAPI for processing requests concurrently, and RabbitMQ as the message broker. MongoDB is used to stored detection data from the analyzed feeds for later retrieval form FastAPI for GPT-5 summaries in the frontend.


## Architecture Flow

User submits a POST request that contains a URL to be analyze -> URL is placed into a RabbitMQ messaging queue -> RMQ notifies workers -> worker picks up message and performs live feed analysis -> object/human detection frames are stored to S3 and emailed to user and detection data is stored in MongoDB for later retrieval.

Frontend of the application allows for users to submit the URL and be able to view the status analyzed views (what URLs have been processed, which ones are in progress, and which ones are currently in the queue) and the live stream is streamed in the frontend for the user to be able to see.
