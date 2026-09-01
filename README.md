# Chess Lessons Platform

Full-stack video learning platform with a backend-focused architecture built using FastAPI, PostgreSQL, SQLAlchemy, Next.js, and S3-compatible object storage.

The project implements authentication, role-based administration, video catalog management, free and paid content access, purchase workflows, view tracking, media uploads, and an FFmpeg-based HLS processing prototype.

## Highlights

- FastAPI REST API with modular routers and service layer
- PostgreSQL persistence with SQLAlchemy and Alembic migrations
- JWT authentication with bcrypt password hashing
- User and administrator roles
- Free and paid video access control
- Purchase lifecycle and Kaspi Pay integration
- DigitalOcean Spaces / S3-compatible object storage
- Private video uploads and public thumbnails
- Presigned URL generation support for private objects
- FFmpeg and ffprobe media processing
- HLS generation prototype
- Video duration extraction
- View tracking and administrative analytics
- Request logging, centralized error handling, CORS, and rate limiting
- Next.js 14 + React + TypeScript frontend
- Docker-based backend environment

## Architecture

```mermaid
flowchart LR
    U[User] --> FE[Next.js Frontend]
    FE --> API[FastAPI API]

    API --> AUTH[JWT Authentication]
    API --> VIDEO[Video API]
    API --> PAYMENT[Purchase & Payment API]
    API --> ADMIN[Admin API]

    AUTH --> DB[(PostgreSQL)]
    VIDEO --> DB
    PAYMENT --> DB
    ADMIN --> DB

    ADMIN --> STORAGE[DigitalOcean Spaces]
    STORAGE --> ORIGINAL[Private Video Objects]
    STORAGE --> THUMB[Thumbnail Objects]

    ADMIN --> MEDIA[Video Service]
    MEDIA --> FF[FFmpeg / ffprobe]
    FF --> HLS[HLS Playlist & Segments]

    PAYMENT --> KASPI[Kaspi Pay Integration]
```

## Backend

The backend is built with FastAPI and is split into dedicated routers for:

- authentication
- users
- videos
- categories
- payments
- administration

The application also includes middleware for request logging, rate limiting, CORS configuration, validation errors, HTTP errors, and unexpected exceptions.

Interactive API documentation is available through Swagger UI and ReDoc.

## Authentication

The authentication layer provides:

- user registration
- email/password login
- JWT access tokens
- password hashing with bcrypt
- authenticated user lookup
- active-user validation
- user and administrator roles

Protected endpoints use FastAPI dependencies to resolve the current authenticated user.

## Data Model

The primary backend entities include:

### User

Stores:

- email
- username
- hashed password
- full name
- role
- account state
- timestamps

### Category

Organizes lesson videos into categories.

### Video

Stores:

- title
- description
- thumbnail URL
- original video URL
- HLS URL
- duration
- price
- access level
- category
- active state
- timestamps

Videos can be either free or paid.

### Purchase

Tracks:

- user
- video
- amount
- payment method
- external payment ID
- payment status
- creation and completion timestamps

### VideoView

Stores individual viewing events and optional watch duration.

These events are also used by the administrative statistics API.

## Video Access

The public video API supports:

- video listing
- category filtering
- access-level filtering
- pagination
- video details
- category-specific listings

Streaming metadata is exposed through an authenticated endpoint.

For paid videos, the backend checks whether the current user has a completed purchase before granting access.

Successful access creates a video-view record that can later be included in analytics.

## Object Storage

Media storage is implemented using boto3 against DigitalOcean Spaces through its S3-compatible API.

### Video uploads

Uploaded videos are:

- validated by file extension
- limited to 500 MB
- assigned UUID-based object names
- stored as private objects
- tagged with original filename metadata

### Thumbnail uploads

Thumbnail images are:

- validated independently
- limited to 5 MB
- stored under dedicated object keys
- uploaded with public-read access

The storage layer also supports:

- presigned GET URLs
- object deletion
- object existence checks

## Media Processing

`VideoService` contains FFmpeg/ffprobe-based media processing functionality.

### HLS generation

The implemented workflow currently:

1. downloads the source video into temporary storage;
2. creates a temporary HLS workspace;
3. invokes FFmpeg;
4. generates a playlist and transport-stream segments;
5. cleans up temporary input files;
6. produces the expected HLS playlist URL.

The FFmpeg configuration generates 10-second HLS segments.

### Video metadata

`ffprobe` is used to inspect media metadata and extract video duration.

### Thumbnail generation

The service also contains FFmpeg-based thumbnail extraction from a configurable video timestamp.

## Current HLS Status

The HLS pipeline is currently a prototype rather than a completed distributed media-processing system.

FFmpeg generation of `.m3u8` and `.ts` files is implemented, but uploading the generated HLS artifacts to DigitalOcean Spaces is still marked as unfinished in the current service implementation.

The frontend already contains an HLS-capable video player, while the remaining backend storage integration is a natural next step for the media pipeline.

## Payments

The backend models paid lesson access as a purchase lifecycle.

The payment flow includes:

1. checking that the requested video exists and requires payment;
2. preventing duplicate completed purchases;
3. creating a pending purchase;
4. requesting a payment URL;
5. receiving payment-provider webhook events;
6. validating the webhook signature;
7. transitioning the purchase to completed or failed;
8. storing the external payment ID.

Users can also retrieve their purchase history and inspect individual purchase states.

The current implementation contains a Kaspi Pay integration layer and HMAC-SHA256 webhook signature verification.

## Admin API

Administrator endpoints support platform-management operations including video upload and statistics.

The video upload flow combines:

- category validation
- file validation
- DigitalOcean Spaces upload
- optional thumbnail upload
- FFmpeg HLS processing
- duration extraction
- database persistence

Administrative statistics aggregate:

- total users
- total videos
- revenue
- recent purchases
- purchases per video
- revenue per video
- views per video

## Frontend

The web interface is built with:

- Next.js 14
- React 18
- TypeScript
- Zustand
- Axios
- Tailwind CSS
- Radix UI components

Application routes include dedicated areas for:

- authentication
- video browsing
- categories
- free content
- payments
- user profile
- administration

The project also includes a custom video-player component with HLS playback support and fallback handling.

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- python-jose
- bcrypt / Passlib
- httpx
- requests

### Media

- FFmpeg
- ffprobe
- HLS

### Storage

- boto3
- DigitalOcean Spaces
- S3-compatible object storage

### Frontend

- Next.js 14
- React 18
- TypeScript
- Zustand
- Axios
- Tailwind CSS
- Radix UI
- hls.js

### Infrastructure

- Docker
- Docker Compose
- PostgreSQL 15
- Redis 7

Redis is provisioned by the current Docker Compose configuration; the primary application code is centered on PostgreSQL and does not currently depend on Redis for its core request flow.

## Project Structure

```text
chesslessons-si/
├── alembic/              # Database migrations
├── app/                  # Next.js application routes
│   ├── admin/
│   ├── auth/
│   ├── categories/
│   ├── free/
│   ├── payment/
│   ├── profile/
│   └── videos/
├── components/           # React UI components
│   └── video/
├── hooks/                # Frontend hooks
├── lib/                  # Frontend helpers
├── middleware/           # FastAPI middleware
├── public/               # Frontend static assets
├── routers/              # FastAPI route modules
│   ├── admin.py
│   ├── auth.py
│   ├── categories.py
│   ├── payments.py
│   ├── users.py
│   └── videos.py
├── scripts/              # Database/admin utilities
├── services/             # Backend service layer
│   ├── payment_service.py
│   ├── storage_service.py
│   └── video_service.py
├── stores/               # Frontend state
├── styles/
├── types/
├── utils/                # Security and database utilities
├── main.py               # FastAPI application
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── database.py
├── auth_utils.py
├── requirements.txt
├── package.json
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── alembic.ini
```

The repository also contains a `backend/` directory with a backend-oriented project layout and supporting development configuration.

## Local Development

### Backend prerequisites

- Python 3.11+
- PostgreSQL
- FFmpeg

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/chess_lessons
SECRET_KEY=change-me

DO_SPACES_ENDPOINT=https://fra1.digitaloceanspaces.com
DO_SPACES_KEY=your-key
DO_SPACES_SECRET=your-secret
DO_SPACES_BUCKET=your-bucket

KASPI_PAY_API_KEY=your-api-key
KASPI_PAY_MERCHANT_ID=your-merchant-id
KASPI_PAY_SECRET=your-webhook-secret

FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

Apply migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API documentation:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

## Frontend Development

Install dependencies:

```bash
pnpm install
```

Start Next.js:

```bash
pnpm dev
```

The frontend runs on:

```text
http://localhost:3000
```

## Makefile

The repository provides helper commands for common backend operations:

```bash
make install
make dev
make upgrade-db
make create-admin
make init-db
make docker-up
make docker-down
make docker-logs
```

## Docker

The backend stack can be started with:

```bash
docker compose up --build
```

The current Compose configuration provisions:

- FastAPI application
- PostgreSQL 15
- Redis 7

The API is exposed on port `8000`.

The Docker image is based on Python 3.11 and includes FFmpeg and the PostgreSQL client.

## Security

The project includes several application-level security controls:

- JWT authentication
- bcrypt password hashing
- private object storage for videos
- role-based administrator access
- paid-content authorization
- upload file validation
- upload size limits
- filename sanitization
- CORS configuration
- request rate limiting
- webhook signature validation

Secrets and storage credentials are loaded from environment variables and should not be committed to source control.

## Engineering Focus

The project goes beyond basic CRUD by combining several backend concerns in one application:

- authenticated REST API design
- relational data modeling
- paid-content authorization
- payment-state management
- object-storage integration
- media file validation
- FFmpeg process orchestration
- temporary-file handling
- HLS media generation
- event/view persistence
- administrative aggregation queries
- frontend/backend integration

## Purpose

Chess Lessons Platform demonstrates the architecture of a paid video-learning product with a strong backend focus.

It combines API development, authentication, PostgreSQL persistence, object storage, payment workflows, authorization, media processing, analytics, and a modern TypeScript frontend in a single project.
