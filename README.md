# extract-transfer-load
This stack involves 3 services:

### Database
Simple postgres database - nothing special

### Transfer
* Flask web server with 2 endpoint:  
  1. /heartbeat - healthceck, will insert a value to the datbase upon completion
  2. /sendfile - gets a JSON of the following format:
  ```json
  {
      "files":
      {
          "filename.extension":"<true/false>"
      }
  }
  ```
  The JSON will have a dictinary named files who's value is another dictionary where the key is the file and the value is whether the file is corrupted or not (true - corruted, false - not corrupted)  

  ### Loader
* Stress tool to generate a lot of fake data and send it to the server.
* config JSON:  
  ```JSON
  {
    "MaxNumberOfFiles": 25,
    "MaxFileCharCount":5,
    "MaxNumberOfParallelRequests":5,
    "CorruptionRate":10,
    "Timeout":40    
  }
  ```
1. MaxNumberOfFiles - the maximum number of files to send in each request. That number is randomly generated   
2.  MaxFileCharCount - Max number of characters in the e file
3. MaxNumberOfParallelRequests - Number of process that will send the requests.
4. CorruptionRate - The corruption probability for each requests. Will affect only 1 file in the list of file
5. Timeout - The requst timeout in seconds

* Command line arguement:
1. --log - log level for printing
2. --url - the URL to send the requests to 

## How to run it?
Using docker-compose issue the following command   
```
docker-compose up --build
```