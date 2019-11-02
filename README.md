# Project Title

REST API testing

### Prerequisites

```
python3
```

### Installing


```
pip install python3
```

## Running the tests

```
python3 -m pytest -sv --html report.html
```

### Break down into end to end tests

```
Each test verifies the whether the REST API is working as per the Swagger specification or not.
```
### Bugs found so far

get products API

```
Swagger says this API returns 404 but couldn't reproduce this error as its returning an empty list correctly so not sure when we get 404 error.
The JSON response keys are incorrect.
price should be product_price
id should be product_code
```
get product API

```
The JSON response keys are incorrect.
price should be product_price
id should be product_code
```
put product API

```
The JSON response keys are incorrect.
price should be product_price
id should be product_code
```
post product API

```
This doesn't return any JSON object on success response.
```

delete product API

```
This doesn't return any JSON object on success response.
```

## Deployment

Given a sample circleci config which can be used to test and deploy

## Authors

* **Swaroopa Mooda** - *Initial work*

## Acknowledgments

* Stackoverflow :)
