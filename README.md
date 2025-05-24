# Pet Vision App

## Overview

This is a simple Flask application that will accept an arbitrary ID and an image URL and return the predicted pet type and breed using the BLIP-vqa-base

## Installation

### Prerequisites

*   Python 3.x
*   Dependencies are listed in `requirements.txt`.

### Steps

1.  Clone the repository:

    ```bash
    git clone https://github.com/jtdelia/pet-vision.git
    cd pet-vision
    ```

2.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running Locally

1.  Set up your environment variables (if any).
2.  Run the application:

    ```bash
    python main.py
    ```

    The application should be accessible at `http://localhost:8000`.


## Send a request

```
 curl --header "Content-Type: application/json" \\n  --request POST \\n  --data '{"id":"1234","image_url":"https://animalsbreeds.com/wp-content/uploads/2014/11/Pembroke-Welsh-Corgi-2.jpeg"}' \\n  https://localhost:8000/inference
 ```

The result should be
```
 {
  "id": "1234",
  "petType": "dog",
  "petBreed": "corgi"
}
```

## Configuration

The application can be configured using environment variables.  

`PORT`: The port the application will run on.  Defaults to 8080.
