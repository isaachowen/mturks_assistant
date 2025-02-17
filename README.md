# atomized_webscrape_data_pipeline_with_mturks
### A system to automate labor-intensive webscraping leveraging Amazon Mechanical Turks and a data quality management "state machine." 


![Lead gathering MTurks Assistant Data Flow](https://user-images.githubusercontent.com/31664870/133171898-261ab115-5002-44f8-a4bb-017f26fc29e9.jpg)

Amazon Mechanical Turk Website 
Explanation of a Human Intelligence Task (HIT) 

## Summary
I would like to make this project widely generalizable, but this is an implementation for a specific web scraping use case.

The end-to-end project assembles a list of email addresses for an email mass marketing campaign. Gather large quantities of focused, quality leads at a very low price.
It takes a list of thousands of American universities and a desired marketing demographic and outputs a relevant, filtered list of email addresses for students and clubs across those universities. 
The time-consuming process of gathering that granular data across highly varied website formats is done en-masse by an "army" of Mechanical Turks working concurrently over the course of a few hours relying on automated validation of their work.
This project is estimated to have saved ~160 hours of manual research and data entry work, and gathered ~3,200 targeted leads for ~$1,000, costing $0.31 per lead (including email address, name, club name, relevant topics of interest).

Webscraping is difficult. It can be difficult to automate using scripts that crawl through a website if the website structure is not well understood. This is case for gathering information across thousands of different university websites. Performing the work manually is often the only realistic way of gathering that information because of the ad-hoc human judgement required to navigate a website (Prior to the advent of LLM-based agents. This project was built before the release of ChatGPT.)

Mechanical Turks Crowdsources Simple Tasks That Require Human Judgement
[Amazon Mechanical Turks](https://www.mturk.com/) is an attractive tool for cheaply performing tasks that require ad-hoc human insight at a massive scale, like basic research tasks. 
You define a simple task (called a [Human Intelligence Task, or HIT](https://blog.mturk.com/tutorial-understanding-hits-and-assignments-d2be35102fbd)) for a remote gig worker to complete, and offer a small fee for that tasks' completion (as little as $0.01 per task). Mechanical Turks volunteer to perform one or more instances of that task at the set price.
For example, a task employed in this project is "google this university and paste the link to their homepage in the form." I paid a Mechanical Turk $0.03 to perform that task.
HITs work better when the task is simple, clearly defined, and appropriately priced for the amount of effort.
The simpler the task, the smaller the price of an individual HIT.

HIT validation is essential and should be automated
Due to the nature of this system, you should not trust that a HIT was performed correctly. 
The quality of the work performed by Mechanical Turks varies widely, and bad HITs can be accepted or rejected.
Manually verifying the work removes the benefit of using Mechanical Turks, because the verifying a task requires you to perform the HIT yourself.
Thus, automating the validation of HITs should be done where possible.

Improve HIT success by minimizing HIT complexity
One key assumption I made was that defining one HIT per university, "Gather all student email addresses from the club directory for ABC university where the club topic is related to XYZ topic." was too complex a task for a Mechanical Turk, and would be too complex to efficiently verify. 
Because of this impracticality, the research process is broken into a pipeline of steps, where each step of the research is a Turk Project with its maximally simplified HIT.
Due to the simple nature of the HIT outputs, it was a straightforward process of validating the HIT quality at each step. 
I chained 3 Mechanical Turk projects together with an automated validation process of the HITs.

The HIT Pipeline With Validation Steps
This repo contains a series of Jupyter notebook scripts that perform the complementary cleaning and validation of the HIT outputs gathered by the Mechanical Turks. It forwards validated HITs forward to the next step of the pipeline, rejects and reruns invalid HITs, and flags HITs where the validation outcome is uncertain. Only the "uncertain" flagged HITs require manual verification. I want to minimize the amount of manual effort I need to spend verifying HITs.

This quality control process can be partially automated with this workbook.
Using HIT redundancy, one can compare the output of the same HIT from different Turks.
The less variation across redundant HITs, the more trustworthy the resulting outcome. If each redundant HIT has different information, some of the Mechanical Turks might have made mistakes or given a spam result hoping for a free HIT fee.
So if there is inconsistency/variation in the results, you need to manually check them. 

MTurk reliability can also be inferred, used to further inform the HIT trustworthiness score, and potentially reject all their work in case they are malicious or sloppy.
The more information we can use to automatically infer HIT quality, the more time you can save searching for and rejecting low quality HITs.
I implemented a "trustworthiness" score for each HIT that we use to prioritize which HITs to manually check, and automatically forward trusted HITs.
Furthermore, some HITs can be easily identified as invalid based on simple string checking with regex, depending on the specific HIT.

![Lead gathering MTurks Assistant basic concept](https://user-images.githubusercontent.com/31664870/132401504-9fe6bc29-4832-4edd-b8e5-4c3e5d99bb9e.jpg)

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


