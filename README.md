# API for Primary Results
Author: Megan Brown

This repo contains code for running a small API to return
primary results based on a local file `primary_results.json`.

## Installation
Requirements for this package beyond the standard Python library are
`flask`, `flask_restful`, and `pandas`.
To install, run:
```
pip install Flask flask-restful pandas
```

## Running the app
To run the app, download this GitHub repo by running
```
git clone git@github.com:mabrownnyu/cta_walkthrough.git
cd cta_walkthrough
python app.py
```

## Endpoints
`/county`
| Parameter | Type | Required | Description |
| - | - | - | - |
| State | string | True | US State to get county results from (case sensitive) |
| County | string | True | US County to get primary results from (case sensitive) |

`/state`
| Parameter | Type | Required | Description |
| - | - | - | - |
| State | string | True | US State to get county results from (case sensitive) |

`/all`
No parameters


## Examples
### County Endpoint
To test the county endpoint, in your local browser, navigate to http://127.0.0.1:5000/county?state=Pennsylvania&county=Chester. This should return:
```
{
    "data": {
        "Democrats": "McGovern",
        "Republicans": "McCloskey"
    }
}
```

### State Endpoint
To test the state endpoint, in your local browser, navigate to http://127.0.0.1:5000/county?state=Pennsylvania. This should return:
```
{
    "data": {
        "Chester": {
            "Democrats": "McGovern",
            "Republicans": "McCloskey"
        }
    }
}
```

### All Endpoint
To test the all endpoint, in your local browser, navigate to http://127.0.0.1:5000/all. This should return:
```
{
    "data": {
        "Pennsylvania": {
            "Chester": {
                "Democrats": "McGovern",
                "Republicans": "McCloskey"
            }
        }
    }
}
```

## Potential Next Steps
1. Working on more general purpose code so the code traversing the JSON is not repeated
2. Thinking more deeply about the payloads returned, specifically what variable names would be useful for the client/end user and what formats would be more useful (e.g. the nested JSONs as shown or a record-oriented response JSON)
3. Consider loading the data into a pandas dataframe to take advantage of the lightweight querying/aggregating capabilities.
4. More robust error responses/possibly fuzzy matches or query suggestions based on misspellings
5. Error handling for fields missing in the JSON (e.g. if a county is in the JSON but had no reported election results)
6. Formatting the endpoints to work like <state>/<county> rather than through query parameters. 
