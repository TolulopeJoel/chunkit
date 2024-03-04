# Chunkit API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
    - [List Chunks](#list-chunks)
    - [Create Chunk](#create-chunk)
    - [List/Upload Files](#listupload-files)
4. [Request and Response Formats](#request-and-response-formats)
    - [Request](#request)
    - [Response](#response)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)
8. [Status Codes](#status-codes)
9. [Contact Information](#contact-information)

## Introduction

Welcome to the ChunkIt API

## Authentication

To use this API, you need to include your API token in the headers of your requests.

## Endpoints

### List Chunks

- **URL:** `/chunks/<int:file_id>/`
- **Method:** `GET`
- **Description:** Retrieve a list of chunks for a specific file.
- **Parameters:**
  - `file_id` (int): ID of the file for which to retrieve chunks.
- **Example Request:**
  ```
  GET /chunks/389/
  ```
- **Example Response:**
  ```json
  {
    "uploaded_file": {
      "id": 389,
      "file": "https://example.com/file.pdf",
      "name": "How to teach your child",
      "type": "pdf",
      "size": "296076",
      "uploaded_at": "2023-12-01T13:42:57.219011Z",
      "user": {
        "id": "3e44683c-7bcc-499d-8d2c-c6747681f31a",
        "email": "toluisjoel@gmail.com",
      }
    },
    "chunks": [
      {
        "chunk_id": 23,
        "position": 1,
        "chunk_file": "https://example.com/chunks/yfi"
      },
      {
        "chunk_id": 24,
        "position": 2,
        "chunk_file": "https://example.com/chunks/r4r"
      }
    ]
  }
  ```

### Create Chunk

- **URL:** `/chunks/`
- **Method:** `POST`
- **Description:** Upload a new chunk for a file.
- **Parameters:**
  - `uploaded_file_id` (int): ID of the file for which to create a chunk.
  - `num_chunks` (int): The sequence number of the chunk.
- **Example Request:**
```
POST /chunks/
{
  "uploaded_file_id": 123,
  "num_chunks": 2,
}
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "File successfully split into chunks.",
  "data": {
    "uploaded_file": {
        "id": 389,
        "file": "https://example.com/file.pdf",
        "name": "How to teach your child",
        "type": "pdf",
        "size": "296076",
        "uploaded_at": "2023-12-01T13:42:57.219011Z",
        "user": {
          "id": "3e44683c-7bcc-499d-8d2c-c6747681f31a",
          "email": "toluisjoel@gmail.com"
        }
    },
    "chunks": [
      {
        "chunk_id": 23,
        "position": 1,
        "chunk_file": "https://example.com/chunks/yfi"
      },
      {
        "chunk_id": 24,
        "position": 2,
        "chunk_file": "https://example.com/chunks/r4r"
      }
    ]
  }
}
```


### List/Upload Files

- **URL:** `/uploaded-files/`
- **Method:** `GET` (List Files) / `POST` (Upload File)
- **Description:** List all uploaded files or upload a new file.
- **Parameters (POST):**
  - `file` (File): The file to be uploaded.
  - `name` (str): The desired name for the file.
- **Example Request (List Files):**
  ```
  GET /uploaded-files/
  ```
- **Example Request (Upload File):**
  ```
  POST /uploaded-files/
  FormData: {
     "file": <file_data>,
     "name": "example" 
  }
  ```
- **Example Response (List Files):**
  ```json
  [
    {
      "id": 1,
      "name": "example.jpeg",
      "type": "jpeg",
      "size": "81224",
      "file": "https://example.com/file.jpg",
      "uploaded_at": "2023-10-30T23:16:22.180488Z",
      "user": {
        "id": "3e44683c-7bcc-499d-8d2c-c6747681f31a",
        "email": "toluisjoel@gmail.com"
      }
    },
    {
      "id": 13,
      "name": "analogy.mp4",
      "type": "mp4",
      "size": "761224",
      "file": "https://example.com/file.mp4",
      "uploaded_at": "2023-11-01T23:16:22.180488Z",
      "user": {
        "id": "3e44683c-7bcc-499d-8d2c-c6747681f31a",
        "email": "toluisjoel@gmail.com"
      }
    },
    ...
  ]
  ```

## Request and Response Formats

### Request

- **Headers:**
  - `Authorization: Bearer <api_key>`
- **Body (POST):**
  - `file` (File): The file to be uploaded.

### Response

- **JSON Format:**
  - Fields may include `id`, `uploaded_file_id`, `num_chunks`, `name`, etc., depending on the endpoint.

## Error Handling

- **Status Code 400: Bad Request**
  - Invalid request parameters or missing required fields.
- **Status Code 401: Unauthorized**
  - Invalid or missing API key.
- **Status Code 404: Not Found**
  - Resource not found.
- **Status Code 500: Internal Server Error**
  - Unexpected server error.

## Rate Limiting

No rate limiting is currently implemented.

## Examples

*[Include practical examples of using each endpoint with both successful and error scenarios]*

## Status Codes

- **200 OK:** Successful request.
- **201 Created:** Successfully created a new resource.
- **400 Bad Request:** Invalid request parameters.
- **401 Unauthorized:** Invalid or missing API key.
- **404 Not Found:** Resource not found.
- **500 Internal Server Error:** Unexpected server error.

## Contact Information

For support or inquiries, please contact toluisjoel@gmail.com .