# AWS Cost Explorer with Service Tag Exporter

## Overview

This application is designed to provide cost exploration and service tag exporting functionalities for AWS resources. It allows users to retrieve daily costs for specific AWS services based on provided tags and export service tags for various AWS services.

## Features

### Cost Exploration
- Provides daily costs for AWS services based on provided tags.
- Utilizes AWS Cost Explorer API for cost retrieval.
- Supports scheduled cost updates.

### Service Tag Exporting
- Exports service tags for AWS services based on predefined tag lists.
- Utilizes AWS Resource Groups Tagging API for tag retrieval.
- Exposes an endpoint to retrieve service tags in JSON format.

## Getting Started

1. Clone the repository: `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure the application using environment variables or a `.env` file (refer to `config.py` for required variables).
4. Run the application: `python app.py`

## Configuration

The application requires the following configuration options:

- `MODE`: Specifies the mode of operation (`cost_provisioning` or `tag_provisioning`).
- `PERSISTENT_FILE`: Path to the persistent file for storing metrics data.
- `TAGS_DISCOVERY_URL`: URL for discovering service tags (used in cost provisioning mode).
- `SCHEDULE_MINUTE`: Minute interval for scheduled cost updates.
- `SCHEDULE_HOUR`: Hour for scheduled cost updates.

## Usage

### Cost Exploration
- Access the `/metrics/` endpoint to retrieve daily costs in Prometheus format.
- Trigger cost updates manually by accessing the `/trigger` endpoint.

### Service Tag Exporting
- Access the `/service_tags` endpoint to retrieve service tags in JSON format.

## Health Check
- Access the `/health` endpoint to perform a health check on the application.

## Dependencies
- `Flask`: Web framework for building the API endpoints.
- `APScheduler`: Library for scheduling tasks.
- `Prometheus Client`: Library for exposing metrics in Prometheus format.
- `boto3`: SDK for AWS services.

## Authors
- Christos Andrikos
