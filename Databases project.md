### One paragraph description of project
*Highlight interesting and challenging parts*
We want to make a database that tracks new york city agencies that allows users to see which agencies are slow or fast at fixing 311 complaints and if the speed differs across neighborhoods. The entity sets we identified are: Complaint type, complaint, agency, address (with attribute neighborhood), result (resolved or not), status (is it being handled).
The relationship sets we identified are: Agency assigned to complaint (one to many), complaint filed for address (many to one), complaint is of type complaint type (many to one), agency handles complaint type (many to many), complaint has status status (one to many), complaint has outcome result (one to many). Below is a preliminary E-R diagram. We will do the front-end version.

![[Untitled Diagram.drawio(1).png]]


## Data plan
We will use the data from the dataset "311 Service Requests from 2010 to Present" provided by new york city open data. Link here: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/about_data

## Description of user interaction plan
How the users can interact with the application: The user can input a neighborhood and the application will return some statistics about that neighborhood, such as average speed taken for requests in general... They can also input an agency and get their average completion speed. Entities involved are address, complaint, agency. 
(possible idea: input an unresolved complaint; application returns whether it is taking longer than expected) (do we need a backend for this or can we just do it with SQL)

## Description of contingency plan
If one student drops, the project doesn't encompass the user interaction plan.