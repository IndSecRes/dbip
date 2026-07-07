# DBIP API Documentation

## Overview
DBIP provides a RESTful API for intelligence processing.

## Endpoints

### Health Check
- `GET /health` - Check service health

### Intelligence Pipeline
- `GET /intelligence/test` - Test the pipeline
- `GET /intelligence/pipeline/info` - Get pipeline information

### Processing
- `POST /intelligence/submit` - Submit data for processing

## Authentication
API Key required for all endpoints.

## Rate Limiting
- Development: 100 requests/minute
- Staging: 500 requests/minute
- Production: 1000 requests/minute