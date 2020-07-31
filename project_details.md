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

* Due to availability of time (so that I can achieve stretch goals), I've merged the Task-2 and Task-3 which is to update document, package, file and snippets class. I will be adding the new feature to all the formats
  parsers, builders and writers. 
   * adding attribute text support for all the formats in package, files and snippets class. ( NEW FEATURE IN 2.2 specs. )
       
 **( Will be adding details of new tasks after completing the previous ones )**

## Timeline

| Weeks | Description of work |
|---|---|
| Week 1 | Made relationship class (parsing & building) available for rdf/xml format. (PRESENT STATE: DEBUGGING) (NOT RUNNING) (REVIEW NEEDED)|
| Week 2 | Relationship working in rdf, tagvalue. |
| Week 3 | Relationship Completely in working condition in every format. ( shows some inconsistency in writing because of different issues ).    |
| EVALUATION 1 | **PASSED** |
| Week 4 |  Package Attribution Text in completely working condition in all formats for parsers, builders and writers. |
| Week 5 | **STARTED**            |
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
|----|----FIRST EVALUATION COMPLETED SUCCESSFULLY------- |
|Day 22| added attribution_text in package.py |
|Day 23| added attribution_text in rdf, tagvalue parsers & builders. |
|Day 24| raised an ISSUE on spdx/specs regarding attributionText in JSON format. (related to its data format & name)|
|Day 25| package attribution text now working in parsers and builders of all formats.|
|Day 28| wrote tests for package attribution text in test_builder.py file.|
|Day 29| added package_attribution_text.py in all formats in parsers, builders and writers.|
|Day 31| added parsers & builders for file_attribution_text in all formats. |



