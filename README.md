# Personalise Concept Hierarchy for ML Course
**Objective:** Construct a learning path based on the user’s learning requirement assuming user has zero knowledge in the field of machine learning

## Folders Description
**Required Data:** Contains all the required data in PDF format<br/>
**Data Preprocessing:** Contains the code of processing, extracting and cleaning data<br/>
**Processed Data:** Contains the data which needed for building the model


## Algorithm Layout/Steps

### 1. Data Preparation
**Book Used**: Pattern Recognition and Machine Learning by Bishop
**Location**: Processed Data, Link: https://drive.google.com/open?id=1un8y8Pc9JCBLFu6h1FVq65KtWlHJrC-X
**Text Data of Book**: Book data is divided into Table of Content, Chapters Text, and Index Keywords. Text data of these stored in "**Text Data**" folder where <br/> prml_toc.txt - contains toc data of book <br/> prml_chpt - contains chapters data of book <br/> prml_index.txt - contains index keywords of book <br/><br/>
**Book Segmentation Data**: Book chapters text data is segmented into ToC sections. The data is saved in "**Book Segmentation** folder. Same data is saved in JSON as well as CSV format.<br/>
Column Description:<br/>
*Section*: Section or sub chapter or sub topic number in ToC<br/>
*Title*: Title of the section<br/>
*Content*: Content which mention in book under that section <br/>
<br/>
**Index Terms Wikipedia Data**: Gathered the wikipedia data for the index file keywords. The data is saved in "**Index Wiki Data** folder. Data is saved in JSON as well as CSV format.<br/>
Column Description:<br/>
*Topic*: Index term present in the index section of book <br/>
*Abbreviation*: Abbreviation of the index term if available in reference section <br/>
*Wiki_Title*: Most relevant wikipedia blog to the index term. It can be same as index term or can be different <br/>
*Wiki_Summary*: Wikipedia summary of the title <br/>
*Wiki_Content*: Complete text of the wikipedia page <br/>
*Wiki_HTML*: HTML content of the wikipedia page <br/>
*Wiki_Links*: Hyperlinked text present in the page <br/>
*Wiki_Sections*: Table of content of the wikipedia page <br/>

<br/>

### 2. Finding Prerequisite Relationships
Output: A binary matrix with entries 0 & 1 have dimensions nXn, where n is number of concepts. In matrix 1 represnt prerequisite relationship<br/>
<br/>

### 3. Finding Concept Hierarchy (Optional! May not be needed)
Output: Locating each concept in Table of Content and output list of sequential concepts 
Required Methods<br/>
<br/>

### 4. Building Concept Maps
Output: A Directed Graph containing each concept at its node and follow the prerequisite relationship
Required Methods<br/>
<br/>

### 5. Extracting Required Concepts
Input: Topic user wants to studdy<br/>
Output: List of sequential topics which user needs to study in order to complete the objective<br/>