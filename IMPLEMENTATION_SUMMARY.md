# Summary of Changes to Flask Application

## Overview
Modified the Flask application in `server.py` to add three main views for interacting with the NYC 311 complaints PostgreSQL database, all using explicit SQL queries without any ORM.

## Files Modified/Created

### 1. Modified: `webserver/server.py`
Added the following routes and functionality:

#### Neighborhood View Routes:
- `GET /neighborhood` - Display neighborhood search form
- `GET /neighborhood/search` - Search and display neighborhood statistics
  - Average completion time (days)
  - Total complaint count
  - Complaint breakdown by type

#### Agency View Routes:
- `GET /agency` - Display agency search form  
- `GET /agency/search` - Search and display agency performance
  - Average completion time
  - City-wide benchmark comparison
  - Total complaints handled
  - Performance difference (faster/slower than city average)

#### User Profile Routes:
- `GET /user` - List all users in the system
- `GET /user/<user_id>` - Display user profile with tracked complaints
- `GET /complaint/search` - Search for complaints to track
- `POST /user/<user_id>/track/<complaint_id>` - Add complaint to user's tracking list
- `POST /user/<user_id>/untrack/<complaint_id>` - Remove complaint from tracking

### 2. Created: `webserver/templates/neighborhood.html`
- Search form for neighborhoods
- Display of neighborhood statistics
- Table showing complaint counts by type
- Responsive design with navigation links

### 3. Created: `webserver/templates/agency.html`
- Search form for agencies (supports partial matching)
- Display of agency performance metrics
- Comparison with city-wide benchmark
- Visual performance indicators

### 4. Created: `webserver/templates/user_list.html`
- Table of all users in the system
- Links to individual user profiles
- Quick access to complaint search functionality

### 5. Created: `webserver/templates/user_profile.html`
- User information display
- Table of tracked complaints with full details
- Ability to add notes when tracking
- Untrack functionality with confirmation
- Link to search for new complaints

### 6. Created: `webserver/templates/complaint_search.html`
- Search interface for complaints
- User selection dropdown (persisted with localStorage)
- Results table with track buttons
- Interactive note-adding via JavaScript prompt

### 7. Modified: `webserver/templates/index.html`
- Enhanced homepage with modern design
- Card-based layout for three main views
- Color-coded sections (blue for neighborhood, green for agency, purple for users)
- Maintained legacy test section at bottom

### 8. Created: `FLASK_README.md`
- Comprehensive documentation of all features
- SQL query examples for each view
- Database schema reference
- Configuration and usage instructions
- API route documentation

## Key Features Implemented

### All SQL Queries Are Explicit
- No ORM usage - all queries written in plain SQL
- Uses SQLAlchemy's `text()` function for parameterized queries
- Prevents SQL injection through proper parameter binding

### Neighborhood Statistics
```sql
-- Average completion time calculation
AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400)
```

### Agency Performance Comparison
- Calculates agency-specific metrics
- Compares against city-wide average
- Shows performance difference in days

### User Complaint Tracking
- Many-to-many relationship through `tracked_by` table
- Optional notes on tracked complaints
- Full complaint details in user profile
- Search functionality with partial matching

## Database Tables Used

1. **agency** - Agency information
2. **complaint_type** - Complaint categories
3. **status** - Complaint status tracking
4. **neighborhood** - NYC neighborhoods
5. **address** - Location data with neighborhood FK
6. **app_user** - User profiles
7. **complaint** - Main complaint records
8. **tracked_by** - User-complaint tracking relationship

## Technical Highlights

- **Parameterized Queries**: All user input properly sanitized
- **JOIN Operations**: Multi-table queries for comprehensive data
- **Aggregate Functions**: AVG, COUNT for statistics
- **Date/Time Calculations**: EXTRACT for duration calculations
- **Pattern Matching**: LIKE with UPPER for case-insensitive search
- **Transaction Management**: Proper commit() calls for INSERT/DELETE
- **Error Handling**: Checks for NULL values and missing records

## Next Steps for Users

1. Update database credentials in `server.py`:
   ```python
   DATABASE_USERNAME = "your_username"
   DATABASE_PASSWRD = "your_password"
   ```

2. Run the application:
   ```bash
   python server.py
   ```

3. Navigate to `http://localhost:8111`

4. Explore the three main views:
   - Neighborhood statistics
   - Agency performance
   - User profiles and complaint tracking

## Notes

- All completion times are calculated in days
- City-wide benchmarks are calculated on-the-fly
- User selection in complaint search is persisted using browser localStorage
- Responsive design works on various screen sizes
- All forms use appropriate HTTP methods (GET for queries, POST for mutations)
