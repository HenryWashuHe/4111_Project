# Flask Application Routes Overview

## Route Structure

```
/                               [GET]  - Home page with links to all views
│
├── /neighborhood              [GET]  - Neighborhood search form
│   └── /neighborhood/search   [GET]  - Display neighborhood statistics
│                                      Query param: ?neighborhood_name=<name>
│
├── /agency                    [GET]  - Agency search form
│   └── /agency/search         [GET]  - Display agency performance
│                                      Query param: ?agency_name=<name>
│
├── /user                      [GET]  - List all users
│   ├── /user/<user_id>        [GET]  - Display user profile
│   │   ├── /user/<user_id>/track/<complaint_id>     [POST] - Track complaint
│   │   └── /user/<user_id>/untrack/<complaint_id>   [POST] - Untrack complaint
│   │
│   └── /complaint/search      [GET]  - Search complaints to track
│                                      Query param: ?query=<search_term>
│
├── /another                   [GET]  - Legacy test page
├── /add                       [POST] - Legacy test form submission
└── /login                     [GET]  - Demo error page (returns 401)
```

## Data Flow Diagrams

### Neighborhood View Flow
```
User
  │
  ├─→ GET /neighborhood
  │     └─→ Show search form
  │
  └─→ GET /neighborhood/search?neighborhood_name=BROOKLYN
        │
        ├─→ SQL: SELECT neighborhood_id FROM neighborhood WHERE name = 'BROOKLYN'
        │
        ├─→ SQL: Calculate AVG completion time for neighborhood
        │     SELECT AVG(closed_at - created_at) FROM complaint
        │     JOIN address ON complaint.address_id = address.address_id
        │     WHERE address.neighborhood_id = :neighborhood_id
        │
        ├─→ SQL: Get complaint counts by type
        │     SELECT complaint_topic, COUNT(*)
        │     FROM complaint JOIN complaint_type
        │     GROUP BY complaint_topic
        │
        └─→ Render neighborhood.html with statistics
```

### Agency View Flow
```
User
  │
  ├─→ GET /agency
  │     └─→ Show search form
  │
  └─→ GET /agency/search?agency_name=Police
        │
        ├─→ SQL: SELECT agency_id FROM agency 
        │        WHERE agency_name LIKE '%Police%'
        │
        ├─→ SQL: Calculate agency's AVG completion time
        │     SELECT AVG(closed_at - created_at), COUNT(*)
        │     FROM complaint WHERE agency_id = :agency_id
        │
        ├─→ SQL: Calculate city-wide AVG (benchmark)
        │     SELECT AVG(closed_at - created_at)
        │     FROM complaint
        │
        ├─→ Calculate: Performance difference
        │     difference = agency_avg - citywide_avg
        │
        └─→ Render agency.html with comparison
```

### User Profile & Tracking Flow
```
User
  │
  ├─→ GET /user
  │     │
  │     ├─→ SQL: SELECT * FROM app_user ORDER BY name
  │     └─→ Render user_list.html
  │
  ├─→ GET /user/US0000000001
  │     │
  │     ├─→ SQL: SELECT * FROM app_user WHERE user_id = 'US0000000001'
  │     │
  │     ├─→ SQL: SELECT complaints with details
  │     │     FROM tracked_by JOIN complaint JOIN complaint_type
  │     │     WHERE tracked_by.user_id = 'US0000000001'
  │     │
  │     └─→ Render user_profile.html
  │
  ├─→ GET /complaint/search?query=noise
  │     │
  │     ├─→ SQL: SELECT complaints WHERE description LIKE '%noise%'
  │     │        OR complaint_topic LIKE '%noise%'
  │     │
  │     └─→ Render complaint_search.html with results
  │
  ├─→ POST /user/US0000000001/track/CO000001
  │     │
  │     ├─→ SQL: Check if already tracking
  │     │     SELECT 1 FROM tracked_by
  │     │     WHERE user_id = 'US0000000001' AND complaint_id = 'CO000001'
  │     │
  │     ├─→ SQL: Insert tracking record (if not exists)
  │     │     INSERT INTO tracked_by (user_id, complaint_id, added_at, note)
  │     │     VALUES ('US0000000001', 'CO000001', CURRENT_TIMESTAMP, :note)
  │     │
  │     └─→ Redirect to /user/US0000000001
  │
  └─→ POST /user/US0000000001/untrack/CO000001
        │
        ├─→ SQL: DELETE FROM tracked_by
        │     WHERE user_id = 'US0000000001' AND complaint_id = 'CO000001'
        │
        └─→ Redirect to /user/US0000000001
```

## Database Query Patterns

### Aggregation Queries
Used in: Neighborhood View, Agency View
```sql
-- Pattern: Calculate average duration
SELECT AVG(EXTRACT(EPOCH FROM (closed_at - created_at)) / 86400) as avg_days
FROM complaint
WHERE conditions...

-- Pattern: Count by category
SELECT category_column, COUNT(*) as count
FROM table JOIN related_table
WHERE conditions...
GROUP BY category_column
ORDER BY count DESC
```

### Join Queries
Used in: User Profile, Complaint Search
```sql
-- Pattern: Multi-table join for complete data
SELECT 
    main_table.id,
    main_table.data,
    related1.name,
    related2.status
FROM main_table
JOIN related1 ON main_table.fk1 = related1.id
JOIN related2 ON main_table.fk2 = related2.id
WHERE conditions...
ORDER BY sort_column
```

### Search Queries
Used in: All search forms
```sql
-- Pattern: Case-insensitive partial match
SELECT columns
FROM table
WHERE UPPER(column) LIKE UPPER(:search_term)
LIMIT max_results
```

### Insert/Delete Queries
Used in: Track/Untrack functionality
```sql
-- Pattern: Safe insert with conflict check
-- First check:
SELECT 1 FROM table WHERE pk_columns...

-- Then insert:
INSERT INTO table (columns...)
VALUES (values...)

-- Or delete:
DELETE FROM table WHERE pk_columns...
```

## HTML Template Structure

```
templates/
├── index.html              - Home page with card-based navigation
├── neighborhood.html       - Neighborhood search & statistics display
├── agency.html            - Agency search & performance comparison
├── user_list.html         - Table of all users
├── user_profile.html      - Individual user with tracked complaints
├── complaint_search.html  - Complaint search with track functionality
├── another.html           - Legacy test page
└── (not modified)
```

## CSS Styling Approach

All templates use inline CSS with:
- **Consistent color scheme**:
  - Blue (#007bff) for Neighborhood
  - Green (#28a745) for Agency  
  - Purple (#6f42c1) for User/Profile
- **Responsive containers**: max-width: 900-1200px, centered
- **Card-based layouts**: Rounded corners, shadows, hover effects
- **Tables**: Striped rows, hover highlighting
- **Forms**: Clean input fields, styled buttons
- **Navigation**: Consistent nav links across all pages

## Security Features

1. **Parameterized Queries**: All user input uses `:param` syntax
2. **SQL Injection Prevention**: SQLAlchemy's `text()` with parameter binding
3. **XSS Prevention**: Jinja2 auto-escaping in templates
4. **Confirmation Prompts**: JavaScript confirms for destructive actions (untrack)
5. **Input Validation**: Required fields, trim whitespace, check for empty strings

## Performance Considerations

1. **LIMIT clauses**: Complaint search limited to 50 results
2. **Indexed columns**: Assumes PKs and FKs are indexed
3. **Selective JOINs**: Only joins tables needed for display
4. **Connection pooling**: SQLAlchemy engine handles connections
5. **Cursor closing**: All cursors explicitly closed after use

## Future Enhancement Ideas

1. **Pagination**: For large result sets
2. **Sorting**: Click column headers to sort tables
3. **Filtering**: Additional filters on searches (date range, status)
4. **Charts**: Visualize statistics with Chart.js or similar
5. **Export**: Download results as CSV
6. **User Authentication**: Login system for actual user accounts
7. **Real-time Updates**: WebSocket for live complaint status
8. **Advanced Search**: Multiple criteria, boolean operators
9. **Bookmarking**: Save favorite searches
10. **Email Notifications**: Alert users when tracked complaints update
