# CommunityBridge Project 2020

## *Short Project Description* 

I will be working on updating the python tool for SPDX to work with new as well maintain consistency with old features.
My foremost work will be to achieve the deliverables I wrote in my proposal for CommunityBridge (they may slightly differ in accordance with the mentors.)
I will be providing the details about my work for every week in SPDX python tool. Starting from July 1, I have started to write code and 
achieve my tasks on time.
NOTE : Using BLACK linter for formatting python code.  
### Tasks
* The first task is to add 'Relationship' class in the tool, so that all the parsers i.e. rdf/xml parser, json parser, yaml parser can now also  
  parse the relationship attribute in the format provided.

* Starting with adding attribute text in package, files and snippets. ( NEW FEATURE IN 2.2 specs. )
       
 **( Will be adding details of new tasks after completing the previous ones )**

## Timeline

| Weeks | Description of work |
|---|---|
| Week 1 | Made relationship class (parsing & building) available for rdf/xml format. (PRESENT STATE: DEBUGGING) (NOT RUNNING) (REVIEW NEEDED)|
| Week 2 | Relationship working in rdf, tagvalue. |
| Week 3 | Relationship Completely in working condition in every format. ( shows some inconsistency in writing because of different issues ).    |
| EVALUATION 1 | **TO Be Done** |
| Week 4 |  **STARTED**           |
| Week 5 |             |
| Week 6 |             |
| Week 7 |             |
| Week 8 |             |
| Week 9 |             |
| Week 10 |             |
| Week 11 |             |
| Week 12 |             |

## Project Team
- Alexios Zavras - Mentor (Primary)
- Gary O'Neall - Mentor
- Julian Schauder - Mentor
- Rohit Lodha - Mentor
- Yash Varshney - Mentee
 
## Daily_work update (for self):
Creating this to keep track of my own work .
( Will clean and make new after every successful evaluation. )

| Day | Work Done |
|---|---|
|Day 1| Made relationship.py file and added relevant info in document.py also (about relationship). Also added Relationship & relationship_comment in lexers/tagvalue.py|
|Day 2| Made project_details.md file and started adding RelationshipParser in spdx/parsers/rdf.py (TBC left note ).|
|Day 3| Created methods in rdf parsers for relationship, relationship_comment.|
|Day 4| Added relation_subject and related_spdx_element in parsers, also understood the role of builders.|
|Day 5| changed the parser in rdf.py (have to amend relationship to string type), which now contains relatedspdx element and the relation_subjec.|
|Day 6| added rdfbuilder and tagvaluebuilder for relationship, also modified parse_rdf.py to introduce relationship.(NOT WORKING)|
|Day 7| Debugging, also removed the relationship_type class in relationship.py file (was making things complicated). STILL NOT WORKING.|
|Day 8| Waiting for the response & reviews from mentors.|
|Day 9| Left debugging for last (waiting for mentors review). Added relationship to tagvaluebuilders.|
|Day 10| added relationship in jsonyamlxml.py file.|
|Day 11| added builders for relationship in jsonyamlxmlbuilders.py (NOT WORKING)|
|Day 12| added relationship writer for rdf, tagvalue, jsonyamlxml.|
|Day 13| added tests for relationships in tests.test_builder.py , also coding for eval 1 is complete, DEBUGGING phase begins.|
|----|----FIRST EVALUATION------- |
|Day 22| added attribution_text in package.py |
|Day 23| added attribution_text in rdf, tagvalue parsers & builders. |



