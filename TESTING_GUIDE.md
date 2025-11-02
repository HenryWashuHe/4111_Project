# Quick Testing Guide

## Before Running

1. **Update Database Credentials** in `server.py` (lines 33-34):
   ```python
   DATABASE_USERNAME = "your_username_here"
   DATABASE_PASSWRD = "your_password_here"
   ```

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install flask sqlalchemy psycopg2-binary
   ```

## Running the Application

```bash
cd webserver
python server.py
```

The server will start on `http://localhost:8111`

## Testing Each View

### 1. Test Neighborhood View

1. Navigate to: `http://localhost:8111/neighborhood`
2. Enter a neighborhood name based on your data (examples from notebooks):
   - "NEW YORK"
   - "BROOKLYN"
   - "QUEENS"
   - Or check your `neighborhood` table for available names
3. Click "Search"
4. Verify you see:
   - Total complaints
   - Average completion time (in days)
   - Table of complaint types with counts

**Sample Query to Find Available Neighborhoods:**
```sql
SELECT name FROM neighborhood ORDER BY name;
```

### 2. Test Agency View

1. Navigate to: `http://localhost:8111/agency`
2. Enter an agency name (partial match works):
   - Try: "Police", "Fire", "Sanitation", etc.
   - Or check your `agency` table for available agencies
3. Click "Search"
4. Verify you see:
   - Total complaints handled
   - Agency's average completion time
   - City-wide average benchmark
   - Performance comparison text

**Sample Query to Find Available Agencies:**
```sql
SELECT agency_name FROM agency ORDER BY agency_name;
```

### 3. Test User Profile View

#### Step 3a: View User List
1. Navigate to: `http://localhost:8111/user`
2. Verify you see a table of all users with:
   - Name
   - Email
   - Member Since date
   - "View Profile" link

#### Step 3b: View Individual User Profile
1. Click on any user's "View Profile" link
2. Verify you see:
   - User information (ID, email, member since)
   - "Track New Complaint" button
   - List of tracked complaints (may be empty initially)

#### Step 3c: Search for Complaints
1. From user profile, click "➕ Track New Complaint"
   - Or navigate to: `http://localhost:8111/complaint/search`
2. Select a user from the dropdown
3. Enter a search term (e.g., "noise", "water", "heat")
4. Click "Search"
5. Verify you see matching complaints with:
   - Complaint ID
   - Type
   - Description
   - Agency
   - Status
   - Created date
   - "Track" button

#### Step 3d: Track a Complaint
1. From search results, click "Track" on any complaint
2. Enter an optional note in the prompt (or leave blank)
3. You'll be redirected to the user's profile
4. Verify the complaint now appears in their tracked list

#### Step 3e: Untrack a Complaint
1. From a user's profile with tracked complaints
2. Click "Untrack" on any complaint
3. Confirm the prompt
4. Verify the complaint is removed from the list

## Sample Test Data

Based on your notebooks, here are some test values:

### Users (from hehe.ipynb):
- US0000000001 - Ava Chen
- US0000000002 - Liam Patel
- US0000000003 - Noah Garcia
- (... more users up to US0000000010)

### Neighborhoods:
- Check your data, but likely includes: NEW YORK, BROOKLYN, QUEENS, BRONX, etc.

### Agencies:
- Your data includes agencies like "New York City Police Department", etc.

## Troubleshooting

### Connection Issues
If you get database connection errors:
1. Verify credentials in `server.py`
2. Check GCP database is running and accessible
3. Verify IP whitelist includes your current IP

### No Results Found
If searches return no results:
1. Check your database has data:
   ```sql
   SELECT COUNT(*) FROM complaint;
   SELECT COUNT(*) FROM neighborhood;
   SELECT COUNT(*) FROM agency;
   ```
2. Verify table names match (e.g., `app_user` vs `user`)
3. Check column names match your schema

### Template Errors
If you see template errors:
1. Verify all HTML files are in `webserver/templates/`
2. Check file names match route calls
3. Ensure proper Jinja2 syntax

## SQL Queries to Verify Data

Run these in your database to verify you have data:

```sql
-- Check total complaints
SELECT COUNT(*) FROM complaint;

-- Check neighborhoods
SELECT neighborhood_id, name FROM neighborhood;

-- Check agencies
SELECT agency_id, agency_name FROM agency LIMIT 5;

-- Check users
SELECT user_id, name, email_address FROM app_user;

-- Check tracked complaints
SELECT * FROM tracked_by;

-- Check complaint types
SELECT complaint_type_id, complaint_topic FROM complaint_type;

-- Sample complaint with all relations
SELECT 
    c.complaint_id,
    c.description,
    ct.complaint_topic,
    a.agency_name,
    s.name as status,
    n.name as neighborhood
FROM complaint c
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
JOIN agency a ON c.agency_id = a.agency_id
JOIN status s ON c.status_id = s.status_id
LEFT JOIN address addr ON c.address_id = addr.address_id
LEFT JOIN neighborhood n ON addr.neighborhood_id = n.neighborhood_id
LIMIT 5;
```

## Expected Behavior

### Neighborhood View
- Empty neighborhood names show error message
- Non-existent neighborhoods show "not found" error
- Valid neighborhoods display statistics and table
- Neighborhoods with no complaints show 0 total

### Agency View
- Partial name matching works (case-insensitive)
- Shows comparison to city average
- Indicates if agency is faster or slower than average
- Empty agency names show error message

### User Profile View
- All users visible in list
- User profiles show tracked complaints
- Search supports partial matching on description and type
- Can track same complaint to multiple users
- Untrack requires confirmation
- Notes are optional when tracking

## Navigation Testing

Test all navigation links work:
- Home page → All three views
- Each view → Back to home
- Each view → Links to other views
- User list → Individual profiles
- User profile → Back to list
- Complaint search → Back to profile

## Common Issues and Fixes

1. **"text" is not defined** - This is a false positive from linter; `text` is imported from sqlalchemy with `from sqlalchemy import *`

2. **"click" could not be resolved** - This is for command-line arguments, comes with Flask

3. **Database connection timeout** - Check GCP firewall rules and IP whitelist

4. **No data showing** - Verify you ran the seed scripts from the notebooks

5. **Template not found** - Ensure all HTML files are in `webserver/templates/` directory
