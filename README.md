Prerequisites:
===
1. Python 3+
2. Don't remove dataset.csv file if you want to load the initial data

Installation:
===
- Unzip the source code zip file
- Open terminal and run `cd adjust-code-challenge`
- Run command `virtualenv -p python3 .`
- Activate the virtualenv using command `source bin/activate`
- Upon activating install dependencies using `pip install -r requirements.txt`
- `cd <place holder>` and run `python manage.py runserver`

REST Endpoint:
==
- There two rest endpoints 
	- Loading the dataset that was provides as part of challenge:
		- Url : `http://localhost:8000/load`
	- Common API as per problem statement
		- URL : `http://localhost:8000/metrics`
		- Request Type : `GET`
		- Params e.g.,:
			- `sort = col1,col2,...` Use (+,-) for asc and desc respectively
			- `where = {"col":value1,...}` For filtering columns based on the values provided
			- `group = gcol1,gcol2,...` Group by columns
			- `agg=acol1,acol2,` Use **+ for Sum, - for Avg and * for Count**
		- Is generic implementation of the API can be used to as rest end point for other Models with minimal changes


Common API Endpoints:
===
1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
	- URL : `http://`