# AlertVisionV2

- Updated version of older project AlertVision with messaging queues and new advancments.

## Tech Stack

**Languages**: Python, Go, Javascript

**Frameworks/Technologies**: React.js, FastAPI, AWS S3, Docker Compose, OpenAI API

**Message Brokers**: RabbitMQ


## What Does This Project Do?

- This project is an expansion of a previous project done before where live camera feeds or surveillance clips are analyzed in the backend for human detection and detected frames are email to user and stored in Amazon S3.

- The architecture has been changed which is reflected upon ths project. Instead of using clips of footage, it has been switched into using public youtube live streams that are accessible. Backend includes the use of FastAPI for processing requests concurrently, and RabbitMQ as the message broker. MongoDB is used to stored detection data from the analyzed feeds for later retrieval form FastAPI for GPT-5 summaries in the frontend.
