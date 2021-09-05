# mturks_assistant
### A series of .ipynb notebooks used to manage large scale multiphase data scraping using Mechanical Turks
This series of .ipynb notebooks is used to quickly clean and process data gathered with Mechanical Turk projects, with the goal of minimizing the effort of manually checking/accepting/rejecting HITs. This method is originally designed for lead gathering, converting a broad list of search-areas into a list of specific leads. Due to the complexity of this process and the resulting difficulty in ensuring quality control from malicious or low quality MTurks, this is treated as a multi-phase data-gathering project with automated data cleaning and quality control exercised at each phase. As I revise the data pipeline I will try to make it as generalizeable as possible, but the initial use case is for gathering email addresses.

## Motivation 
For really big MTurk projects, you probably want to use lower pricing, but at lower pricing, the quality of the Turks' work is generally worse. Checking just a few HITs as a proxy of the Turks' work is not an effective quality control method because there can be so many Turks doing just a few HITs. The process of checking a HIT is effectively the same as doing the HIT yourself. The purpose of outsourcing the work is then defeated. Ideally, the work of manually checking HITs should be minimized as much as possible, while maintaining reasonable quality control on the HITs, and being able to reject bad HITs. We want to drastically reduce the search time for bad HITs.

This quality control process can be partially automated. Using HIT redundancy, one can compare the output of the same HIT from different Turks. The more redundancy there is for a certain HIT, the more trustworthy the resulting outcome. If there is inconsistency/variation in the results, you may need to check them. MTurk reliability can also be inferred, used to further inform the HIT trustworthiness score, or reject all their work in case they are malicious. The more information we can use to automatically infer HIT quality, the more time you can save searching for and rejecting low quality HITs. We use a ``trustworthiness" score for each HIT that we use to prioritize which HITs we need to manually check, and automatically process trustworthy HITs. Furthermore, some HITs can be easily identified as invalid based on the existence of some ``anchor" text like "@" in an email address or "." in a website url. This depends on the HIT.


## How it works
Based on a particular scraping project, the notebooks create a project directory and create subdirectories to identify the steps that they correspond to. The main work that you must do to use the tool should be to input the file names of the raw MTurk outputs, and give a name to the current scraping project that the notebooks will use in the local directory. Redundant HITs are collated and analyzed, and Mturks are scored, to create a trustworthiness index with which you the reviewer can use to prioritize, check, and reject or accept unreliable HITs.

Use excel not csv because excel can be edited both by notebooks and manually. This works in google colab as well. 

The 7 directories created inside of a project directory serve the following purpose:

### 1 mIn
The raw input file(s) for the MTurk project, placed here by the user. 
(for me, a list of universities)

### 2 mOut
The raw output file(s) of the Mturk-based scrape placed here by the user.
(for me, it will be a redundant, messy list of links to universities' directory of clubs)

### 3 notebookCleaned
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook).
(for me, it will be lists of club directories for universities)

### 4 manualCleaned_mIn
Use this folder to copy in the file(s) from 3. For each file Then manually inspect and where necessary, modify the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 1 for another batch of gathering.
With multiple files, they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be lists of club directories for universities)

### 5 mOut
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of clubs that match a certain criteria with the link to their information page)

### 6 notebookCleaned
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook). 
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

### 7 manualCleaned_mIn
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 4 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

### 8 mOut
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of university club's contact information)

### 9 notebookCleaned
The cleaned output file(s) from the Mturk-scrape. 
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

### 10 manualCleaned_leads
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 7 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file.
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

