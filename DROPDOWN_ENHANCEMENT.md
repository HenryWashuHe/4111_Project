# Enhancement: Dynamic Dropdowns and Filters

## Summary
Updated the Neighborhood and Agency views to include dynamic dropdowns populated directly from the database, allowing users to select options via dropdown menus or text search, with optional filtering by complaint type.

## Changes Made

### 1. Server-side Changes (`server.py`)

#### Neighborhood View (`/neighborhood`)
**Before:** Static search form
**After:** 
- Fetches all neighborhoods from database dynamically
- Fetches all complaint types from database dynamically
- Passes data to template

#### Neighborhood Search (`/neighborhood/search`)
**Enhanced with:**
- Support for dropdown selection (`neighborhood_id` parameter)
- Support for text search (`neighborhood_name` parameter) - backward compatible
- Optional complaint type filter (`complaint_type_id` parameter)
- Dynamically builds SQL queries based on selected filters
- Returns dropdown data and selected values to maintain form state

**New Query Features:**
```sql
-- Filter statistics by complaint type when selected
WHERE a.neighborhood_id = :neighborhood_id
  AND c.complaint_type_id = :complaint_type_id  -- Optional filter
  AND c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL
```

#### Agency View (`/agency`)
**Before:** Static search form
**After:**
- Fetches all agencies from database dynamically
- Fetches all complaint types from database dynamically
- Passes data to template

#### Agency Search (`/agency/search`)
**Enhanced with:**
- Support for dropdown selection (`agency_id` parameter)
- Support for text search (`agency_name` parameter) - backward compatible
- Optional complaint type filter (`complaint_type_id` parameter)
- Dynamically builds SQL queries based on selected filters
- Returns dropdown data and selected values to maintain form state
- **NEW:** Added "Top Complaint Types Handled" breakdown table

**New Query Features:**
```sql
-- Filter statistics by complaint type when selected
WHERE c.agency_id = :agency_id
  AND c.complaint_type_id = :complaint_type_id  -- Optional filter
  AND c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL

-- New breakdown query
SELECT ct.complaint_topic, COUNT(*) as count
FROM complaint c
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
WHERE c.agency_id = :agency_id
GROUP BY ct.complaint_topic
ORDER BY count DESC
LIMIT 10
```

### 2. Template Changes

#### `neighborhood.html`
**Added:**
- Dropdown selector for neighborhoods (populated from database)
- Text search field (alternative to dropdown)
- Dropdown filter for complaint types (optional)
- Proper form sections with labels
- "OR" divider between dropdown and text search
- Maintains selected values after search
- Enhanced CSS for better form layout

**Form Structure:**
```
1. Neighborhood Dropdown (all from DB)
2. OR
3. Text Search Field
4. Complaint Type Filter (optional)
5. Search Button
```

#### `agency.html`
**Added:**
- Dropdown selector for agencies (populated from database)
- Text search field (alternative to dropdown)
- Dropdown filter for complaint types (optional)
- Proper form sections with labels
- "OR" divider between dropdown and text search
- Maintains selected values after search
- Enhanced CSS for better form layout
- **NEW:** Table displaying top 10 complaint types handled by the agency

**Form Structure:**
```
1. Agency Dropdown (all from DB)
2. OR
3. Text Search Field
4. Complaint Type Filter (optional)
5. Search Button
```

## Key Features

### 1. **Database-Driven Dropdowns**
- All dropdown options come directly from the database
- No hardcoded values
- Automatically reflects current database state
- SQL queries: `SELECT DISTINCT ... FROM table ORDER BY name`

### 2. **Dual Input Methods**
- Users can choose dropdown OR text search
- Dropdown takes precedence if both provided
- Text search supports partial matching (for agencies)
- Backward compatible with existing links

### 3. **Optional Filtering**
- Filter results by specific complaint type
- Applies to all statistics and breakdowns
- "All Types" option to see unfiltered data
- Filter selections are preserved after search

### 4. **Form State Persistence**
- Selected dropdown values are maintained after search
- Uses `selected` attribute in HTML
- Improves user experience for iterative searches

### 5. **Enhanced Data Presentation**
- Agency view now shows top complaint types breakdown
- Better visual hierarchy with form sections
- Improved CSS with form grouping
- Larger, more readable form controls

## SQL Queries Added/Modified

### New Queries for Dropdowns
```sql
-- Get all neighborhoods
SELECT DISTINCT neighborhood_id, name 
FROM neighborhood 
ORDER BY name

-- Get all agencies
SELECT DISTINCT agency_id, agency_name 
FROM agency 
ORDER BY agency_name

-- Get all complaint types
SELECT DISTINCT complaint_type_id, complaint_topic 
FROM complaint_type 
ORDER BY complaint_topic
```

### Modified Queries with Optional Filters
```sql
-- Example: Neighborhood average speed with optional type filter
SELECT AVG(EXTRACT(EPOCH FROM (c.closed_at - c.created_at)) / 86400) as avg_days
FROM complaint c
JOIN address a ON c.address_id = a.address_id
WHERE a.neighborhood_id = :neighborhood_id
  AND c.complaint_type_id = :complaint_type_id  -- Added conditionally
  AND c.closed_at IS NOT NULL
  AND c.created_at IS NOT NULL
```

### New Query: Agency Complaint Breakdown
```sql
SELECT ct.complaint_topic, COUNT(*) as count
FROM complaint c
JOIN complaint_type ct ON c.complaint_type_id = ct.complaint_type_id
WHERE c.agency_id = :agency_id
  AND c.complaint_type_id = :complaint_type_id  -- Optional filter
GROUP BY ct.complaint_topic
ORDER BY count DESC
LIMIT 10
```

## User Experience Improvements

1. **Easier Navigation**: Dropdowns allow browsing all available options
2. **Faster Selection**: No need to remember exact names
3. **Type-Ahead**: Modern browsers provide autocomplete in dropdowns
4. **Focused Analysis**: Filter by complaint type for specific insights
5. **Clear Visual Design**: Form sections clearly delineated
6. **Maintained Context**: Selected values persist after search

## Technical Details

### Query Building Approach
```python
# Build filter dynamically based on parameters
query_params = {"neighborhood_id": neighborhood_id}
complaint_type_filter = ""

if filter_complaint_type:
    complaint_type_filter = "AND c.complaint_type_id = :complaint_type_id"
    query_params["complaint_type_id"] = filter_complaint_type

# Use f-string to inject filter into SQL
query = f"""
    SELECT ...
    WHERE a.neighborhood_id = :neighborhood_id
      {complaint_type_filter}
      AND ...
"""
cursor = g.conn.execute(text(query), query_params)
```

### Template Context Structure
```python
context = {
    # Dropdown data
    "neighborhoods": [...],           # or "agencies": [...]
    "complaint_types": [...],
    
    # Selected values (for maintaining form state)
    "selected_neighborhood_id": "NB00000001",
    "selected_complaint_type_id": "CT00000003",
    
    # Results
    "neighborhood_name": "BROOKLYN",
    "avg_speed": 15.3,
    "complaint_type_breakdown": [...],
    "total_complaints": 42
}
```

## Testing Instructions

### Test Neighborhood View
1. Navigate to `/neighborhood`
2. **Test Dropdown**: Select a neighborhood from dropdown, click Search
3. **Test Text Search**: Clear dropdown, enter neighborhood name, click Search
4. **Test Filter**: Select neighborhood + complaint type, click Search
5. **Verify**: Check that statistics update correctly for filtered results

### Test Agency View
1. Navigate to `/agency`
2. **Test Dropdown**: Select an agency from dropdown, click Search
3. **Test Text Search**: Clear dropdown, enter agency name, click Search
4. **Test Filter**: Select agency + complaint type, click Search
5. **Verify**: Check complaint breakdown table appears
6. **Verify**: Check that statistics reflect the filter

### Edge Cases to Test
- Select "-- Select a neighborhood --" (no selection) → should show error
- Enter non-existent neighborhood/agency name → should show error
- Select complaint type but no neighborhood/agency → should show error
- Change filter and re-submit → should update results
- Use browser back button → form state should be preserved

## Performance Considerations

- Dropdown queries run on every page load (both initial and search results)
- Queries use `SELECT DISTINCT` which may be slower on large tables
- Consider adding indexes on `name` columns if performance becomes an issue
- Limit agency complaint breakdown to top 10 to avoid large result sets

## Future Enhancements

1. **AJAX-based filtering**: Update results without page reload
2. **Search within dropdown**: Searchable dropdowns for large lists
3. **Multi-select filters**: Allow selecting multiple complaint types
4. **Date range filters**: Filter by complaint creation/closure date
5. **Status filters**: Filter by complaint status (open/closed)
6. **Neighborhood groups**: Group by borough or region
7. **Export filtered results**: Download as CSV
8. **Save searches**: Bookmark specific filter combinations
9. **Comparison mode**: Compare two neighborhoods or agencies side-by-side
10. **Visualizations**: Add charts for breakdowns (pie/bar charts)
