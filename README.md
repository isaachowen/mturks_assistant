# Fanned out multiphase webscrape pipeline with Mechanical Turks and automated validation
This is a system to cheaply and quickly assemble contacts for an email marketing campaign. It automates labor-intensive webscraping using Amazon Mechanical Turks and a data quality management pipeline. 
Granular contact information is gathered across highly varied website formats en-masse by an "army" of Mechanical Turks completing thousands of small tasks concurrently over a few hours.
This instance of the project saved ~160 hours of manual research and data entry work, and gathered ~3,200 targeted leads for ~$1,000, costing $0.31 per lead (including email address, name, club name, relevant topics of interest).
It took a list of thousands of American universities and a desired marketing demographic and outputs a list of email addresses for students and clubs across those universities. 

## Traditional automated webscraping requires well-understood website format.
If there are many different websites of interest containing data you want to scrape, writing scripts that crawl through all the different websites is not practical.
Performing the work manually is often the most practical way of gathering that information because of the ad-hoc human judgement required to navigate a website's UI (LLM-based agents may have solved this problem).

## Mechanical Turks crowdsources simple tasks that require human judgement
[Amazon Mechanical Turks](https://www.mturk.com/) is a tool for cheaply performing tasks that require ad-hoc human insight at scale. 
A "requester" defines a simple task (called a [Human Intelligence Task, or HIT](https://blog.mturk.com/tutorial-understanding-hits-and-assignments-d2be35102fbd)), and offer a small payment for that tasks' completion (as little as $0.01 per task). 
For example, a task employed in this project is "google this university and paste the link to their homepage in the form." I paid a Mechanical Turk $0.03 to perform that task.

Remote gig workers, called "Mechanical Turks" may then volunteer to perform one or more instances of that HIT, based on the difficulty of the task and the payment amount.
The completed HIT can then be accepted or rejected by the requester.
HITs work better when the task is simple, clearly defined, and appropriately priced for the amount of effort.
Simpler tasks are generally cheaper, more complex tasks are more expensive.

## HITs should be defined to be automatically validated
Due to the nature of this system, the quality of work performed by Turks varies widely. You can avoid paying for a bad HIT by rejecting it. You can then relist the rejected HIT instance for another Turk to pick up.
Verifying the work essentially requires you to perform the HIT yourself, so automating the validation of HITs should be done where possible.

## Automate HIT validation by implementing a sequence of 3 "fanout" HIT tasks
It is not possible to automate the validation HITs that are too complex. 
Validating a single HIT encapsulating the entire webscraping campaign would be prohibitively expensive, time consuming and complex.
Similarly, verifying one HIT per university, where the task is to gather all relevant emails for a university, would also be impossible to automate.

To make possible the automation of validating HITs, the web scraping campaign is broken into a pipeline of simplified webscrape steps that where each step of the research is an easy-to-validate HIT.
Simplifying the webscrape campaign into a series of simpler HITs also allows for a cheaper cost-per-hit.
I chained 3 webscrape HITs together into a "fanout" to enable simple automated automated validation of each of the 3 webscrape HITs.

The three HITs were:
1. For <university name>, locate and paste in the student club directory url
2. For the club directory at <university name>, enter all club names and urls that would be interested in XYZ topic
3. For the <club name> club at url <club url>, enter all available email addresses for officers and members

![Lead gathering MTurks Assistant basic concept](https://user-images.githubusercontent.com/31664870/132401504-9fe6bc29-4832-4edd-b8e5-4c3e5d99bb9e.jpg)
![Fan Out Diagram](_fanout_diagram.jpeg)

## The HIT Fanout + Validation Pipeline
This repo contains a series of scripts that build the pipeline of directories that hold the perform the complementary cleaning and validation of the HIT outputs at the three stages of the pipeline. It forwards validated HITs forward to the next step of the pipeline, rejects and reruns invalid HITs, and flags HITs where the validation outcome is uncertain. Only the "uncertain" flagged HITs require manual verification. I want to minimize the amount of manual effort I need to spend verifying HITs.

![Lead gathering MTurks Assistant Data Flow](https://user-images.githubusercontent.com/31664870/133171898-261ab115-5002-44f8-a4bb-017f26fc29e9.jpg)
![Pipeline Diagram](_pipeline_diagram.jpeg)


## How validation works
The more information we can use to automatically infer HIT quality, the more time you can save searching for and manually validating unvalidated HITs.
- Simple string parsing and regex
    - Some HITs can be easily identified as invalid based on simple string checking with regex, depending on the specific HIT.
- I implemented a "trustworthiness" score for each HIT that we use to prioritize which HITs to manually check, and automatically forward trusted HITs.
- HIT redundancy and cross validation
    - By using HIT redundancy, having n Turks perform the same HIT instance n times, you can get multiple outputs for the same HIT instance that can be cross-referenced. 
    - The less variation across redundant HITs, the more trustworthy the resulting output. If the n redundant HITs produce different outputs across the n Turks, some subset of the Turks are producing bad outputs.
    - The more variation of the results, the more that HIT instance demands your attention. This allows you to filter out the HITs you want to automatiacally approve, and filter on the subset of hits that require your manual attention, in a prioritized order based on the variation within the HIT instance.
    - The variation can be measured by entropy or a simpler metric.

Furthermore, MTurk reliability can be inferred from the HIT ID and percentage of rejected work, which could further inform the HIT trustworthiness/variation score, and potentially flag a bad Turk's HITs for automatic rejection, or blocking the Turk.

## How to use the tool
- The notebooks create a project directory and create subdirectories to identify the steps that they correspond to.
- Determine the fanout set of questions you want to use.
- Input the file names of the raw MTurk outputs, and give a name to the current scraping project that the notebooks will use in the local directory.
- Redundant HITs are collated and analyzed, and Mturks are scored, to create a trustworthiness index with which you the reviewer can use to prioritize, check, and reject or accept unreliable HITs. You can also reject or block unreliable Turks.
- Use excel not csv because excel can be edited both by notebooks and manually. This works in google colab as well. 

## The pipeline directories
These directories are created inside of the project directory and represent the most granular view of the pipeline.

#### 1_request_data__unis
The raw input file(s) for the MTurk project, placed here by the user. 
(for me, a list of universities)

#### 2_hits__club_lists
The raw output file(s) of the Mturk-based scrape placed here by the user.
(for me, it will be a redundant, messy list of links to universities' directory of clubs)

#### 3_hits__club_lists_labeled
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook).
(for me, it will be lists of club directories for universities)

#### 4_request_data__club_lists
Use this folder to copy in the file(s) from 3. For each file Then manually inspect and where necessary, modify the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 1 for another batch of gathering.
With multiple files, they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be lists of club directories for universities)

#### 5_hits__clubs
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of clubs that match a certain criteria with the link to their information page)

#### 6_hits__clubs_labeled
The cleaned output file(s) from the Mturk-scrape (inserted here by the notebook). 
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

#### 7_request_data__clubs
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 4 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file, which is the input of the next Mturk scrape.
(for me, it will be a list of clubs that match a certain criteria, and the link to their information page)

#### 8_hits__leads
The raw output file(s) of the Mturk-based scrape (placed here by the user).
(for me, it will be a redundant, messy list of university club's contact information)

#### 9_hits__leads_labeled
The cleaned output file(s) from the Mturk-scrape. 
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

#### 10_leads
You will need to manually inspect the cleaned output file based on the HITs' scores, and the quality of their output.
Note the rejected HITs and HITs that will need to be repeated, this list is fed back to folder 7 for another batch of gathering.
With multiple files they should be manually assembled in a new excel file.
(for me, it will be a list of contact information for each of the student organizations you might want to connect with)

#### 11_leads_accumulator
Manually assemble all leads in an excel sheet or csv to be fed into your CRM or mass email system.

### Enable convenient git commits for the local repo. 
Within the repo, after pip installing requirements in your python virtual environment, run the following:
```
git config --local diff.ipynb.textconv "nbdime diff"
git config --local difftool.ipynb.cmd "nbdime difftool"
git config --local merge.tool nbdime
git config --local mergetool.nbdime.cmd "nbdime merge"


git config --local filter.nbstripout.clean "nbstripout"
git config --local filter.nbstripout.smudge cat
git config --local filter.nbstripout.required true
```
