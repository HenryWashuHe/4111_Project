# Quick Reference: Updated Views

## Neighborhood View Form

```
┌─────────────────────────────────────────────────────────────┐
│  NYC 311 Complaints Database - Neighborhood View            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Select Neighborhood:                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ -- Select a neighborhood --                    ▼   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│                         OR                                   │
│                                                              │
│  Search by Name:                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Enter neighborhood name (e.g., NEW YORK)           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Filter by Complaint Type (optional):                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ -- All Types --                                ▼   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────┐                                                │
│  │  Search  │                                                │
│  └──────────┘                                                │
└─────────────────────────────────────────────────────────────┘
```

### Example: Populated Neighborhood Dropdown
- BROOKLYN
- BRONX
- NEW YORK
- QUEENS
- STATEN ISLAND
- ... (all neighborhoods from database)

### Example: Complaint Type Filter
- -- All Types --
- Noise - Residential
- Heat/Hot Water
- Illegal Parking
- Street Condition
- Water System
- ... (all complaint types from database)

## Agency View Form

```
┌─────────────────────────────────────────────────────────────┐
│  NYC 311 Complaints Database - Agency View                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Select Agency:                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ -- Select an agency --                         ▼   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│                         OR                                   │
│                                                              │
│  Search by Name:                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Enter agency name (e.g., Police)                   │    │
│  └────────────────────────────────────────────────────┘    │
│  Tip: You can enter a partial name                          │
│                                                              │
│  Filter by Complaint Type (optional):                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ -- All Types --                                ▼   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌──────────┐                                                │
│  │  Search  │                                                │
│  └──────────┘                                                │
└─────────────────────────────────────────────────────────────┘
```

### Example: Populated Agency Dropdown
- Department of Buildings
- Department of Environmental Protection
- Department of Health and Mental Hygiene
- Department of Sanitation
- New York City Police Department
- ... (all agencies from database)

## Search Result Example - Neighborhood View

After selecting "BROOKLYN" and "Noise - Residential":

```
┌─────────────────────────────────────────────────────────────┐
│  Statistics for BROOKLYN                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Total Complaints: 127                                       │
│  (filtered by: Noise - Residential)                          │
│                                                              │
│  Average Completion Time: 8.5 days                           │
│                                                              │
│  Complaints by Type                                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Complaint Type              │ Count                │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ Noise - Residential         │ 127                  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Search Result Example - Agency View

After selecting "New York City Police Department" and "Noise - Residential":

```
┌─────────────────────────────────────────────────────────────┐
│  New York City Police Department                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Total Complaints Handled: 485                               │
│  (filtered by: Noise - Residential)                          │
│                                                              │
│  Average Completion Time: 12.3 days                          │
│                                                              │
│  ────────────────────────────────────────                    │
│  Performance Comparison                                      │
│  ────────────────────────────────────────                    │
│                                                              │
│    This Agency         City-Wide Average                     │
│      12.3 days              15.8 days                        │
│                                                              │
│  3.5 days faster than city average                           │
│  (for Noise - Residential complaints)                        │
│                                                              │
│  ────────────────────────────────────────                    │
│  Top Complaint Types Handled                                 │
│  ────────────────────────────────────────                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Complaint Type              │ Count                │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ Noise - Residential         │ 485                  │    │
│  │ Illegal Parking             │ 342                  │    │
│  │ Blocked Driveway            │ 201                  │    │
│  │ ...                         │ ...                  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Usage Scenarios

### Scenario 1: Browse All Neighborhoods
1. Go to `/neighborhood`
2. Click dropdown to see all neighborhoods
3. Select one
4. Click "Search"
5. View statistics

### Scenario 2: Quick Text Search
1. Go to `/neighborhood`
2. Type "BROOK" in text field
3. Click "Search"
4. System finds "BROOKLYN" (partial match)
5. View statistics

### Scenario 3: Filtered Analysis
1. Go to `/neighborhood`
2. Select "MANHATTAN" from dropdown
3. Select "Noise - Residential" from filter
4. Click "Search"
5. View noise-specific statistics for Manhattan

### Scenario 4: Agency Comparison
1. Go to `/agency`
2. Select "Department of Sanitation"
3. Leave complaint type as "All Types"
4. Click "Search"
5. Compare their 23.5 days to city average of 18.2 days
6. See breakdown of top 10 complaint types they handle

### Scenario 5: Focused Agency Analysis
1. Go to `/agency`
2. Select "Department of Buildings"
3. Select "Heat/Hot Water" from filter
4. Click "Search"
5. See how DOB handles heat complaints specifically
6. Compare to city average for heat complaints only

## API Request Examples

### Neighborhood with Dropdown
```
GET /neighborhood/search?neighborhood_id=NB00000001
```

### Neighborhood with Text Search
```
GET /neighborhood/search?neighborhood_name=BROOKLYN
```

### Neighborhood with Filter
```
GET /neighborhood/search?neighborhood_id=NB00000001&complaint_type_id=CT00000005
```

### Agency with Dropdown
```
GET /agency/search?agency_id=AG00000003
```

### Agency with Text Search
```
GET /agency/search?agency_name=Police
```

### Agency with Filter
```
GET /agency/search?agency_id=AG00000003&complaint_type_id=CT00000005
```

## Form State Persistence

When a search is performed, the form maintains state:

**Before Search:**
```html
<select name="neighborhood_id">
  <option value="">-- Select a neighborhood --</option>
  <option value="NB00000001">BROOKLYN</option>
  <option value="NB00000002">MANHATTAN</option>
</select>
```

**After Search (BROOKLYN selected):**
```html
<select name="neighborhood_id">
  <option value="">-- Select a neighborhood --</option>
  <option value="NB00000001" selected>BROOKLYN</option>
  <option value="NB00000002">MANHATTAN</option>
</select>
```

This allows users to:
- See what they searched for
- Easily modify their selection
- Re-submit with different filters

## Browser Compatibility

These forms work with:
- ✅ Chrome/Edge (native dropdown styling)
- ✅ Firefox (native dropdown styling)
- ✅ Safari (native dropdown styling)
- ✅ Mobile browsers (native pickers)

No JavaScript required for basic functionality!

## Accessibility Features

- ✅ Proper `<label>` elements with `for` attributes
- ✅ Semantic HTML structure
- ✅ Keyboard navigation support
- ✅ Screen reader friendly
- ✅ Clear visual hierarchy
- ✅ High contrast form elements

## Data Flow Diagram

```
User Action → Form Submission → Server
                                   ↓
                          Parse Parameters
                                   ↓
                     ┌──────────────┴──────────────┐
                     ↓                             ↓
            Dropdown (ID)                    Text Search
                     ↓                             ↓
              Find by ID                   Find by Name
                     └──────────────┬──────────────┘
                                    ↓
                        Optional Complaint Type Filter
                                    ↓
                          Build SQL Query with Filters
                                    ↓
                             Execute Queries
                                    ↓
                            Format Results
                                    ↓
                    Render Template with Results
                    + Maintain Form State
                                    ↓
                             Return to User
```
