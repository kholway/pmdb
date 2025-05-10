# pmdb: Personal Movie Database
A simple database and api for tracking movies you want to watch as a group, say, for a family movie night!

Truly, a project for me to practice setting up a CRUD API, and beyond.

## Development 
### Tech Stack
The project uses FastAPI, Pydantic, and SQLAlchemy. The project currently uses
an SQLite database.

### Approach
I'm attempting a test-driven development, where possible.

### Organization
- `app.database` - SQLAlchemy database wiring
- `app.deps` - FastAPI dependencies
- `app.models` - SQLAlchemy data models
- `app.schemas` - Pydantic models
- `app.routers` - API routes
- `app.main` - drives the application