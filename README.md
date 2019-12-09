# Personalise Concept Hierarchy for ML Course
**Objective:** Construct a personalise concept hierarchy based on the user’s learning requirement for the machine learning course

## Folders Description
**Required Data:** Contains all the required data in PDF format<br/>
**Data Preprocessing:** Contains the code of processing, extracting and cleaning data


## Algorithm has 3 parts
**1. Data Preparation**<br/>
Output:<br/>
1. List of Required Unique Concepts<br/>
2. Abbreviation and Acronym for each concept<br/>
3. Corpus of Wikipedia Data corresponding to each concept<br/>
4. Universal Table of Content<br/>
5. Corresponding book’s textual data for each section of ToC<br/>
<br/>

**2. Finding Prerequisite Relationships**<br/>
Output: A binary matrix with entries 0 & 1 have dimensions nXn, where n is number of concepts. In matrix 1 represnt prerequisite relationship<br/>
<br/>

**3. Finding Concept Hierarchy**<br/>
Output: Locating each concept in Table of Content and output list of sequential concepts 
Required Methods<br/>
<br/>

**4. Building Concept Maps**<br/>
Output: A Directed Graph containing each concept at its node and follow the prerequisite relationship
Required Methods<br/>
<br/>

**5. Extracting Required Concepts**<br/>
Input: Topic user wants to studdy<br/>
Output: List of sequential topics which user needs to study in order to complete the objective<br/>