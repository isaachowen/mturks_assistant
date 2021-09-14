# mturks_assistant
### A series of .ipynb notebooks used to manage large scale multiphase data scraping using Mechanical Turks
This series of .ipynb notebooks is used to quickly clean and process data gathered with Mechanical Turks Data Collection projects, with the goal of minimizing the effort of manually checking/accepting/rejecting HITs. This method is originally designed for lead gathering, converting a broad list of search-areas into a list of specific leads. Due to the complexity of this process and the resulting difficulty in ensuring quality control from malicious or low quality MTurks, this is treated as a multi-phase data-gathering project with automated data cleaning and quality control exercised at each phase. As I revise the data pipeline I will try to make it as generalizeable as possible, but the initial use case is for gathering email addresses.

## Motivation 
For arbitrarily large MTurk projects, using a cheaper HIT compensation scheme is attractive. However at lower pricing, the quality of the Turks' work is generally worse (also, Master Turks are less likely to take low-priced HITs compared to non-masters). Manually checking HITs as a proxy of the Turks' work is not an effective quality control method because there can be so many Turks doing just a few HITs (the process of checking a HIT is the same as doing the HIT yourself, thus defeating the purpose of outsourcing the work in the first place). Ideally, the work of manually checking HITs should be minimized as much as possible, while maintaining reasonable quality control on the HITs, and being able to efficiently reject bad HITs and block malicious workers. We want to drastically reduce the search time for bad HITs.

This quality control process can be partially automated with this workbook. Using HIT redundancy, one can compare the output of the same HIT from different Turks. The more redundancy (aka less entropy) there is for a certain HIT, the more trustworthy the resulting outcome. If there is inconsistency/variation in the results, you may need to check them. MTurk reliability can also be inferred, used to further inform the HIT trustworthiness score, or reject all their work in case they are malicious. The more information we can use to automatically infer HIT quality, the more time you can save searching for and rejecting low quality HITs. We use a "trustworthiness" score for each HIT that we use to prioritize which HITs we need to manually check, and automatically process trustworthy HITs. Furthermore, some HITs can be easily identified as invalid based on simple string checking with regex, depending on the specific HIT.

## Business Outcome
Gather large quantities of focused, quality leads at a very low price. Will populate this with my own data soon.

## How it works
Based on a particular scraping project, the notebooks create a project directory and create subdirectories to identify the steps that they correspond to. The main work that you must do to use the tool should be to input the file names of the raw MTurk outputs, and give a name to the current scraping project that the notebooks will use in the local directory. Redundant HITs are collated and analyzed, and Mturks are scored, to create a trustworthiness index with which you the reviewer can use to prioritize, check, and reject or accept unreliable HITs.

Use excel not csv because excel can be edited both by notebooks and manually. This works in google colab as well. 

The 7 directories created inside of a project directory serve the following purpose:

### 1_mIn_unis
The raw input file(s) for the MTurk project, placed here by the user. 
(for me, a list of universities)

### 2_mOut_dirs
The raw output file(s) of the Mturk-based scrape placed here by the user.
(for me, it will be a redundant, messy list of links to universities' directory of clubs)

### 3_notebookProcessed_dirs
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook).
(for me, it will be lists of club directories for universities)

### 4_manualCleaned_mIn_dirs
Use this folder to copy in the file(s) from 3. For each file Then manually inspect and where necessary, modify the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 1 for another batch of gathering.
With multiple files, they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be lists of club directories for universities)

### 5_mOut_clubs
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of clubs that match a certain criteria with the link to their information page)

### 6_notebookProcessed_clubs
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook). 
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

### 7_manualCleaned_mIn_clubs
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 4 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

### 8_mOut_leads
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of university club's contact information)

### 9_notebookProcessed_leads
The cleaned output file(s) from the Mturk-scrape. 
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

### 10_manualCleaned_leads
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 7 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file.
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

### 11_allLeads
Manually assemble all leads in an excel sheet or csv to be fed into your CRM or mass email system.

![Lead gathering MTurks Assistant basic concept](https://user-images.githubusercontent.com/31664870/132401504-9fe6bc29-4832-4edd-b8e5-4c3e5d99bb9e.jpg)
![Lead gathering MTurks Assistant Data Flow](https://user-images.githubusercontent.com/31664870/133171898-261ab115-5002-44f8-a4bb-017f26fc29e9.jpg)

