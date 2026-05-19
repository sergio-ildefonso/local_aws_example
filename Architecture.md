## Architecture


```
┌────────────────────────────────────────────────────────────────────┐
│                         USER / CLIENT                              │
│    (e.g., Browser, Mobile App, External Service accessing endpoints) │
└────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │      FLOCI LOCALE AWS       │
                     │       EMULATOR              │
                     │      (Postgres Port 5432)     │
                     │    (AWS API Port 4566)        │
                     │    (RDS Port 7001)          │
                     └─────────────────────────────┘
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    ▼                              ▼                              ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   S3 Bucket 1       │    │   S3 Bucket 2       │    │   S3 Bucket 3       │
│  my-local-bucket-1  │    │  my-local-bucket-2  │    │  my-local-bucket-3  │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                                                  │
           └──────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────┐
│  RDS PostgreSQL Database (db-4B93D755C3EE44BABD71D26E)             │
│  - Instance Class: db.t3.micro                                     │
│  - Allocated Storage: 10 GB                                        │
│  - Database Name: local_db                                         │
│  - Username: admin                                                 │
│  - Master Password: [PASSWORD]                                   │
└────────────────────────────────────────────────────────────────────┘
           │
           └───────────────────────┐
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │   IAM Role: lambda_role       │
                    │    - Can access S3 buckets  │
                    │    - Can access RDS DB      │
                    │    - Permissions: read/write│
                    └─────────────────────────────┘
                                   │
      ┌────────────────────────────┼─────────────────────────────┐
      ▼                            ▼                             ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Lambda Function 1   │    │   Lambda Function 2   │    │    Lambda Code        │
│    my-first-lambda  │    │   my-second-lambda  │    │  (index.js/app.js)    │
│    (Runtime: Node.js) │    │    (Runtime: Node.js) │    └─────────────────────┘
│    Handler: index.handler │    │    Handler: app.handler │
│    Role: lambda_role      │    │    Role: lambda_role      │
│    - Reads from S3      │    │    - Writes to S3       │
│    - Reads from RDS     │    │    - Writes to RDS      │
│    - Returns JSON       │    │    - Returns JSON       │
│    - Supports GET/POST  │    │    - Supports GET/POST  │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```


