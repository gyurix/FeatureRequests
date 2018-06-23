# Feature Requests

## Requirements
You need to have a database set up for using this application.

If you don't have a database set up yet, then you can set up a PostgreSQL by following these steps:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04


## Installation
1. Install Python 3, git, nano and screen: `apt-get install -y python3-dev python3-pip git screen nano`
2. Clone the repository: `git clone https://github.com/gyurix/FeatureRequests.git`
3. Navigate to the cloned repository: `cd FeatureRequests`
4. Add execution access to the install script: `chmod 770 install.sh`
5. Run the installation script: `./install.sh`
6. Edit the configuration according to your needs: `nano app/config.py`

## Starting / Stopping / Status check
- Start the application using `./start.sh`
- Stop the application using `./stop.sh`
- Check application status using `./status.sh`
- Open application screen using `screen -x feature_requests`
- Minimize application screen using `CTRL+A & CTRL+D`



# Original task
This is a project that we use for testing potential team members on their technical skills.

## Feature Request App
Build a web application that allows the user to create "feature requests".

A "feature request" is a request for a new feature that will be added onto an existing piece of
software. Assume that the user is an employee at IWS who would be entering this information after
having some correspondence with the client that is requesting the feature.  The necessary fields
are:

* **Title:** A short, descriptive name of the feature request.
* **Description:** A long description of the feature request.
* **Client:** A selection list of clients (use "Client A", "Client B", "Client C")
* **Client Priority:** A numbered priority according to the client (1...n). Client Priority numbers
should not repeat for the given client, so if a priority is set on a new feature as "1", then all
other feature requests for that client should be reordered.
* **Target Date:** The date that the client is hoping to have the feature.
* **Product Area:** A selection list of product areas (use 'Policies', 'Billing', 'Claims',
'Reports')

## Tech Stack Requirements
The following are requirements on the tech stack. This stack demonstrates mastery of tools our team favors.

* OS: Ubuntu
* Server Side Scripting: Python 2.7+ or 3.5+
* Server Framework: Flask or SimpleHTTPServer
* ORM: Sql-Alchemy
* JavaScript: KnockoutJS

Make sure that your instructions for accessing or otherwise running your code are extremely clear.

## Guidelines

Build your own public repo on github, and call it whatever you like. Build your solution in your
repo, and include a README.md file that contains the detailed instructions for running your web app.
Email the URL for your github repo to opsmanagers@britecore.com once you begin the project so we can review 
your progress. Prior to submission, please bring up a live hosted example. AWS has a free tier if you 
aren't certain where to host. Once your project is completed, please email opsmanagers@britecore.com.

One of the major goals in this project is to see how you fill in ambiguities in your own creative
way. There is no such thing as a perfect project here, just interpretations of the instructions
above, so be creative in your approach.

We want to be respectful of your time and set realistic expectations for submission. To help guide you, we 
have included the list below which details common practices in the best projects we receive. It is rare for 
a project to match every item in this list, but the candidates we hire typically showcase several of 
these features in their work.

--

TECHNOLOGY

1. *Open Source*. We have a strong affinity for open source technology. If your go-to technology stack includes
proprietary software, you won't be helping yourself to use it in this project.

2. *Decoupled Backend*. We are looking for candidates with a strong understanding of the entire web application stack. The best projects will completely decouple the backend and the front end and communciate via API.

3. *Test Suites with Continuous Integration*. Enterprise production requires rock solid stability. All code submitted into BriteCore repos must contain unit and regressions tests, so we favor candidates with experience writing quality tests.

4. *Automated Deployment*. Speaking of deployment, the most valuable engineers understand how their code is deployed and practice "infrastructure as code". The best projects integrated CI with a fully automated deployment to AWS, Digital Ocean, or similar.

5. *Usable, Responsive Interface*. There are many accessible CSS frameworks out there such as Bootstrap. All modern web applications should be responsive and these frameworks make it very easy to create a modern interface that adheres to established design principles and formats well on all devices.

6. *MVVM Frontend*. The modern web is highly interactive. Projects like Knockout.js make it very easy to deploy HTML bindings that interact with interface elements dependably and efficiently.

--

Thank you for your time. We are excited to review your project!

