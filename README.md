# serverless
A playground to test out the serverless functions.

## crawler-bs4
It scrapes the content of url given in the GET request.

### Technology Stack
- Serverless framework
- Beautiful Soup 4 for scraping
- AWS Lambda
- AWS API Gateway

### Test locally in serverless framework:

```
$ sls invoke local -f main --path events/sample.json
```

### Deploy to AWS:
```
$ sls deploy
```
