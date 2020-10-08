# address-parser microservice
A REST endpoint consuming an address string and returning a json with address fields:

```
curl -X POST "http://127.0.0.1:5000/parse" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"address\": \"5760 Teredo St., Sechelt, BC, Canada, VON 3A0\"}"
    {
        "city": "Sechelt",
        "state": "BC",
        "street_address": "5760, Teredo St.",
        "postcode": "VON 3A0",
        "country": "Canada",
    },
```

## Use Locally

1. Install libpostal
2. Instal deps with `pipenv install && pipenv shell`
3. Run flask application `export FLASK_APP=api.py && flask run`
4. Test at http://127.0.0.1:5000/swagger-ui/

## Deploying on AWS Lambda
Libpostal requires 2GB on disk and in memory for the model, so the AWS Lambda deployment consists of 2 steps:
1. Getting libpostal files on shared EFS
2. Configuring pypostal from Lambda

### Getting libpostal files on shared EFS
1. Create EFS, Amazon Linux 2 AMI with attached EFS:
* Use an instance with 4GB memory.
* Make sure VPC has NFS inbound rule and DNS resolution
2. Install libpostal and copy data files (`datadir`) and library files (*.so and pkgconfig) from `/usr/local/lib` to EFS
### Configuring library from Lambda and Lambda itself
3. Build [pypostal from master](https://github.com/openvenues/pypostal) for Lambda

```docker build -t pypostal . && docker create -ti --name dummy pypostal bash && docker cp dummy:/postal/postal ./ && docker rm dummy```

4. Deploy Lambda with zappa in the same region:
* don't forget to add Lambda's pypostal
* Max out memory
* point to libpostal files on EFS:

```
LD_LIBRARY_PATH /mnt/efs/libpostal_lib/lib

LIBPOSTAL_DATA_DIR /mnt/efs/libpostal_model/libpostal

PKG_CONFIG_PATH /mnt/efs/libpostal_lib/lib/pkgconfig
```

* Add EFS to Lambda:

Use the same VPC

configure subnets for public access

```curl -X POST "https://fe5k5zd4k4.execute-api.us-west-2.amazonaws.com/dev/parse" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"address\": \"5760 Teredo St., Sechelt, BC, Canada, VON 3A0\"}"```