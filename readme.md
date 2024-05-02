# Anime-data dataware house and data pipeline with AWS

# Summary

This project consists of a scheduled extraction of anime, reviews, and other information from the Anilist API. The data is then saved to a local mySQL instance in the same format.
The data pipeline consists of a scheduled job that extract the latest data from the database into a file, then loads to amazon S3 and copies it to a RedShift data warehouse.

Initially the architecture will contemplate only a mysql database, but it could be later improved to support other database engines.   
The target storage will all be in the AWS cloud, but in the future I plan to add support for the same components from GCP (GCS, BigQuery).

Finally, all the installation and deployment in the cloud will be done with IaC, Terraform is the contemplated option for this.

*Note: This document will grow as new components get designed and included to the project.*


# Architecture

```mermaid
graph TD;
   
   AniList API    -->   MySQL;
   Scheduler --> MySQL;
   Scheduler --> Extraction Job Python;
   Extraction Job Python   -->    S3;
   S3    -->   Redshift;
                                                                          
   
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


# Testing


# License