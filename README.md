# address-parser microservice
A REST endpoint consuming an address string and returning a json with address fields:

    curl -X POST "http://127.0.0.1:5000/parse" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"address\": \"5760 Teredo St., Sechelt, BC, Canada, VON 3A0\"}"
    {
        "city": "Sechelt",
        "state": "BC",
        "street_address": "5760, Teredo St.",
        "postcode": "VON 3A0",
        "country": "Canada",
    },

## Use Locally

1. Install libpostal
2. Instal deps with `pipenv install && pipenv shell`
3. Run flask application `export FLASK_APP=api.py && flask run`
4. Test at http://127.0.0.1:5000/swagger-ui/

## Deploying on AWS Lambda
Libpostal requires 2GB on disk and in memory for the model, so the AWS Lambda deployment consists of 3 steps:
1. Installing libpostal on shared EFS
2. Configuring library from Lambda and Lambda itself

### Installing libpostal on shared EFS
*I used Ubuntu image, but probably Lambda's Linux image would be more convenient.*
1. Create EFS, Ubuntu 18 EC2 with attached EFS:
* Use an instance with 4GB memory.
* Make sure VPC has inbound rule for NFS so EFS mount works
2. Install libpostal and copy data files (`datadir`) and library files (*.so and pkgconfig) from `/usr/local/lib` to EFS
### Configuring library from Lambda and Lambda itself
3. Build [tweaked pypostal](https://github.com/uzadude/pypostal/tree/datadir) for Lambda https://towardsdatascience.com/how-to-install-python-packages-for-aws-lambda-layer-74e193c76a91
4. Deploy Lambda with zappa in the same region:
* don't forget to add Lambda's pypostal
* Max out memory
* point to libpostal files on EFS:

LD_LIBRARY_PATH /mnt/efs/libpostal_lib/lib

LIBPOSTAL_DATA_DIR /mnt/efs/libpostal_data/libpostal

PKG_CONFIG_PATH /mnt/efs/libpostal_lib/lib/pkgconfig

* Add EFS to Lambda:
Use the same VPC
configure subnets for public access
