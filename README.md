# mturks_assistant
A series of .ipynb notebooks used to manage large scale multiphase data scraping using Mechanical Turks

## This series of notebooks is used to quickly clean and process MTurk data, with the goal of minimizing the effort of manually checking/accepting/rejecting HITs. This is originally designed for lead gathering, converting a broad list of search-areas into an explicit list of warm leads. Due to the complexity of this process and the resulting difficulty in ensuring quality control from malicious or low quality Turks, this is treated as a multi-phase data-gathering project with data cleaning and quality control exercised at each phase.

As I revise the data pipeline I will try to make it as generalizeable as possible, but the initial use case of gathering email addresses is probably obvious.

## Motivation 
For really big projects, checking HITs is a hassle -- checking a HIT is effectively the same as doing the HIT yourself. Checking just a few HITs as a proxy of the Turks' work is not an effective quality control method because there can be so many Turks doing just a few HITs. For larger projects you want to use lower pricing, but at lower pricing, the quality of the Turks' work is generally worse.

This quality control process can be automated. Using HIT redundancy, one can compare the output of the same HIT from different Turks. The more redundancy, the more trustworthy the result. If there is variation in the results, you may need to check them. You can use a trustworthiness score for each HIT output, where the more information we can use to automatically infer HIT quality, the more time you can save. Furthermore, some HITs can be easily identified as valid or not via some anchor text like "@" in an email address or "." in a website url. It depends on the HIT. MTurk reliability can also be inferred, used to further inform the HIT trustworthiness score.

## How it works
The notebooks create directories based on the project name and clearly identify the steps that they correspond to. The main work that you must do to use the tool should be to input the file names of the raw MTurk outputs, and give a name to the current scraping project that the notebooks will use in the local directory. Redundant HITs are collated and analyzed, and Mturks are scored, to create a trustworthiness index with which you the reviewer can use to prioritize, check, and reject or accept unreliable HITs.

Use excel not csv because excel can be edited both by notebooks and manually. This works in google colab as well. 

The 7 folders created by the notebooks serve the following purpose:

# 1
MTurks empty project spreadsheet to fill up. 
(here, list of universities)

# 2 
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(here, it will be a redundant, messy list of links to universities' directory of clubs)

# 3 
The cleaned output files from the Mturk-scrape which is the input of the next Mturk scrape (inserted here by the notebook).
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
With multiple files they should be manually assembled in excel/google sheets.
(here, it will be a list of club directories for universities)

# 4
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(here, it will be a redundant, messy list of clubs that match a certain criteria with the link to their information page)

# 5
The cleaned output files from the Mturk-scrape which is the input of the next Mturk scrape (inserted here by the notebook). 
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
With multiple files they should be manually assembled in a new excel file.
(here, it will be a list of clubs that match a certain criteria, and the link to their information page)

# 6
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(here, it will be a redundant, messy list of university club's contact information)

# 7 
The cleaned output files from the Mturk-scrape. 
(here, it will be a list of contact information for each of the student organizations you might want to connect with).
With multiple files they should be manually assembled in a new excel file.




