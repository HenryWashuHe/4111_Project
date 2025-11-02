# NYC 311 Complaints Database - Flask Application

This Flask application provides an interface to explore and track NYC 311 complaints data stored in a PostgreSQL database on Google Cloud Platform.

## Features

### 1. Neighborhood View (`/neighborhood`)
View comprehensive statistics for any neighborhood:
- **Average completion time** for complaints (in days)
- **Total complaint count** for the neighborhood
- **Breakdown by complaint type** with counts for each type

**Usage:**
- Navigate to `/neighborhood`
- Enter a neighborhood name (e.g., "NEW YORK", "BROOKLYN")
- View statistics and complaint type distribution

**SQL Query Examples:**
```sql
-- Get neighborhood statistics
SELECT 
    AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days
FROM complaint c
JOIN address a ON c.address_id = a.address_id
WHERE a.neighborhood_id = :neighborhood_id
  AND c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL

-- Get complaint counts by type
SELECT 
    ct.complaint_topic,
    COUNT(*) as count
FROM complaint c
JOIN address a ON c.address_id = a.address_id
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
WHERE a.neighborhood_id = :neighborhood_id
GROUP BY ct.complaint_topic
ORDER BY count DESC
```

### 2. Agency View (`/agency`)
Compare agency performance against city-wide benchmarks:
- **Average completion time** for the agency
- **City-wide average** for comparison
- **Performance comparison** (faster/slower than average)
- **Total complaints handled**

**Usage:**
- Navigate to `/agency`
- Enter an agency name or partial name (e.g., "Police" will find "New York City Police Department")
- View performance metrics and comparison

**SQL Query Examples:**
```sql
-- Get agency performance
SELECT 
    AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days,
    COUNT(*) as total_complaints
FROM complaint c
WHERE c.agency_id = :agency_id
  AND c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL

-- Get city-wide benchmark
SELECT 
    AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days
FROM complaint c
WHERE c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL
```

### 3. User Profile View (`/user`)
Manage user profiles and track complaints of interest:
- View all users in the system
- See individual user profiles with their tracked complaints
- Search for complaints to add to tracking list
- Add notes to tracked complaints
- Remove complaints from tracking

**Features:**
- **User List** (`/user`): Browse all users
- **User Profile** (`/user/<user_id>`): View a specific user's tracked complaints
- **Complaint Search** (`/complaint/search`): Search complaints by description or type
- **Track Complaint**: Add complaints to a user's watchlist with optional notes
- **Untrack Complaint**: Remove complaints from tracking

**Usage:**
1. Navigate to `/user` to see all users
2. Click on a user to view their profile
3. Use "Search Complaints to Track" to find complaints
4. Click "Track" on any complaint and add an optional note
5. View all tracked complaints on the user's profile page
6. Click "Untrack" to remove a complaint from the watchlist

**SQL Query Examples:**
```sql
-- Get user's tracked complaints
SELECT 
    c.complaint_id,
    c.description,
    c.created_at,
    c.closed_at,
    ct.complaint_topic,
    a.agency_name,
    s.name as status_name,
    tb.added_at,
    tb.note
FROM tracked_by tb
JOIN complaint c ON tb.complaint_id = c.complaint_id
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
JOIN agency a ON c.agency_id = a.agency_id
JOIN status s ON c.status_id = s.status_id
WHERE tb.user_id = :user_id
ORDER BY tb.added_at DESC

-- Search for complaints
SELECT 
    c.complaint_id,
    c.description,
    ct.complaint_topic,
    a.agency_name,
    s.name as status_name,
    c.created_at
FROM complaint c
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
JOIN agency a ON c.agency_id = a.agency_id
JOIN status s ON c.status_id = s.status_id
WHERE UPPER(c.description) LIKE UPPER(:query)
   OR UPPER(ct.complaint_topic) LIKE UPPER(:query)
ORDER BY c.created_at DESC
LIMIT 50

-- Track a complaint
INSERT INTO tracked_by (user_id, complaint_id, added_at, note)
VALUES (:user_id, :complaint_id, CURRENT_TIMESTAMP, :note)

-- Untrack a complaint
DELETE FROM tracked_by 
WHERE user_id = :user_id AND complaint_id = :complaint_id
```

## Database Schema

The application uses the following tables:

- **agency**: Agency information (agency_id, agency_name)
- **complaint_type**: Types of complaints (complaint_type_id, complaint_topic)
- **status**: Complaint status (status_id, name, is_terminal)
- **neighborhood**: NYC neighborhoods (neighborhood_id, name)
- **address**: Address information (address_id, neighborhood_id, street1, street2, postal_code)
- **app_user**: User profiles (user_id, name, email_address, created_at)
- **complaint**: Main complaint records (complaint_id, description, created_at, closed_at, agency_id, complaint_type_id, address_id, status_id)
- **handle_by_default**: Default agency for complaint types (complaint_type_id, agency_id)
- **tracked_by**: User complaint tracking (user_id, complaint_id, added_at, note)

## Configuration

Before running the application, update the database credentials in `server.py`:

```python
DATABASE_USERNAME = "your_username"
DATABASE_PASSWRD = "your_password"
DATABASE_HOST = "34.139.8.30"
```

## Running the Application

```bash
python server.py
```

Then navigate to `http://localhost:8111` in your browser.

## Implementation Notes

- All SQL queries are **explicit** and use **no ORM** (Object-Relational Mapper)
- Queries use SQLAlchemy's `text()` function for parameterized queries to prevent SQL injection
- All timestamps are handled in UTC
- Completion time is calculated as the difference between `closed_at` and `created_at` in days
- User tracking allows multiple users to track the same complaint
- Complaint search supports partial matching on description and complaint type

## API Routes

### Neighborhood Routes
- `GET /neighborhood` - Display neighborhood search form
- `GET /neighborhood/search?neighborhood_name=<name>` - View neighborhood statistics

### Agency Routes
- `GET /agency` - Display agency search form
- `GET /agency/search?agency_name=<name>` - View agency performance

### User Routes
- `GET /user` - List all users
- `GET /user/<user_id>` - View user profile and tracked complaints
- `GET /complaint/search?query=<search>` - Search for complaints
- `POST /user/<user_id>/track/<complaint_id>` - Track a complaint (with optional note)
- `POST /user/<user_id>/untrack/<complaint_id>` - Untrack a complaint

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database connection and query execution (text-based, no ORM)
- **PostgreSQL**: Database system (hosted on GCP)
- **Jinja2**: HTML templating
