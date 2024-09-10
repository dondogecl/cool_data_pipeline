# Anime-data dataware house and data pipeline with AWS

# Summary

This project consists of a scheduled extraction of anime, reviews, and other information from the Anilist API. The data is then saved to a local mySQL instance in the same format.
The data pipeline consists of a scheduled job that extract the latest data from the database into a file, then loads to amazon S3 and copies it to a RedShift data warehouse.

Initially the architecture will contemplate only a mysql database, but it could be later improved to support other database engines.   
The target storage will all be in the AWS cloud, but in the future I plan to add support for the same components from GCP (GCS, BigQuery).

Finally, all the installation and deployment in the cloud will be done with IaC, Terraform is the contemplated option for this.

*Note: This document will grow as new components get designed and included to the project.*


# Architecture

```
    AniList API-->MySQL

    Scheduler--> MySQL --> Extraction Job Python --> S3 --> Redshift
                                                                          
   
```



# Installation
- API fetcher
- MySQL schema
- Extraction jobs (local)
- AWS setup
    - S3
    - Redshift
    - Groups and users
    - Security rules

# Data sources
- Anilist API

# Cloud setup


# Deployment

Example for the environment variables needed to make the process work:

```

# [aws_boto_credentials]
AWS_ACCESS_KEY=<my_key>
AWS_SECRET_KEY=<my_secret>
BUCKET_NAME=<my_bucket_name>
AWS_ACCOUNT_ID=<my_account_id>

# [mysql_config]
MYSQL_HOSTNAME=127.0.0.1
MYSQL_PORT=3306
MYSQL_USERNAME=<my_user>
MYSQL_PASSWORD=<my_db_pass>
MYSQL_DATABASE=<my_db_name>

# [aws_creds]
DWH_DATABASE=<my_db_name>
DWH_USERNAME=<my_user>
DWH_PASSWORD=<my_pass>
DWH_HOSTNAME=<endpoint/workgroup_for_rs>
DWH_PORT=5439
DWH_IAM_ROLE=<RedshiftLoaderRoleExample>
DWH_ACCESS_KEY=<example_access_key>
DWH_SECRET_KEY=<example_secret_has_to_be_hard_to_guess>
DWH_REGION=<us-east-2_for_example>

```


# Testing

Create quality tests using pytest/dbt.

# License

