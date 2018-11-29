1.General background information
  (1)File description
     url.text-> it contains five urls: 1.https://www.utoronto.ca/ 
                                        2.https://www.utoronto.ca/donors     
                                        3.http://www.eecg.toronto.edu/ (as required for AWS Deployment)
                                        4.http://www.rosi.utoronto.ca/
                                        5.https://www.utoronto.ca/faculty-staff

     crawler.py-> 1.depth is set to 1. 
                  2.You need to have redis server running before run python crawler.py.

  (2)how data is stored in and fetched out of the redis db:
     Since redis db store all data into string, so we decide to use json to convert all json readable dict to json string. When we fetch out the stored data from db, we convert them back to dict from json string.
  
  (3)Backend functionality description
     Run run_backend_test.py file and it will - run crawler.py - run pagerank.py - run pprint to print readable_page_rank
     If you want, there are some commented out codes for redis db set up which you can add them back so that you do not have to separately run crawler.py anymore, however, make sure you always have redis server running before performing any db changes. (It is unnecessary to do so if you want to use server.py to populate data).
     To run server.py locally, first you need to run crawler.py to have crawled data stored in redis db, then run python server.py.

2.Access frontend on AWS
  >>redis-server                      //Run the Redis server in the backgroud
    ctrl+z
  >>bg
  >>disown -h
  >>sudo python crawler.py            //Store the data to database    
  >>sudo nohup python server.py       //Start the website server

  Public IP address of live web server (for now)
  Public IP address is 174.129.152.66
  Public DNS is ec2-174-129-152-66.compute-1.amazonaws.com

3.Benchmark setup
  (1)Use the Apache benchmarking tool.
     step1: Use the command of "$ ab -n 1000 -c 50 http://localhost:80/?keywords=acorn"
            to send 50 concurrent identical requests with total of 1000 requests
     step2: Try send differenct number of requests from 1000 to 3000 to see 
            what is the maximum number of connections that server can handled.    
     step3: After finding the maximum number of connections,
            run the command several time with that number to get the best performance result.
     test result is shown as Lab3-performance in the folder.

  (2)Use the dstat tool with 'cdnpy' and 'vmstat' property
     to show utilization of CPU, memory usage, disk IO and network at same time.

  Website of lab3 can handle fewer connections than lab2. The max number of connection for lab2 is 5000, while 1000 is the max number of connection for lab3. According to the result from Apache benchmarking tool, the mean of time used per request for lab3 is 30.67ms, which is a little bit longer than lab2, 26.59ms per request. Lab2 also has a better result for Requests per second(RPS), which is 1880.16 versus 1630.12. Overall, the lab2 server has a better performance. The reason that causes this result may be the lab3 server connects to a relational database. Each client request needs to access the data stored inside the database, which requires more operations and lowers the performance.
