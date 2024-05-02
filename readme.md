# Data Pipeline Project with AWS

# Summary

This project consists of a data pipeline that moves data from a source database to a cloud data warehouse.   
Initially the architecture will contemplate a mysql database, but it could be later improved to support other database engines.   
The target storage will be in the AWS cloud, and some parts could change with time.

This document will grow as new components get designed and included to the project.

# Architecture

                   Scheduler
                      ↓
   AniList API    ->   MySQL   ->  Extraction Job Python   ->    S3    ->   Redshift
      ↓                          ↓                               ↓           ↓
   Data Fetch              Data Storage                    Data Extraction   Data Loading


# Installation

# Data sources

# Cloud setup

# Deployment

# Testing

# License