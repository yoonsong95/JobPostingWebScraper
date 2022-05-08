from bs4 import BeautifulSoup
from models import Job
import requests
import time
import datetime
import csv


def findIndeedJobs(jobTitle, location):
    jobs = []
    for i in range(0, 5):
        htmlText = requests.get(f"https://ca.indeed.com/jobs?q={jobTitle}&l={location}&radius=50&start={i * 10}").text
        soup = BeautifulSoup(htmlText, "lxml")
        resultContents = soup.find_all("td", class_="resultContent")

        for resultContent in resultContents:
            jobTitle = ""
            jobTitleSpans = resultContent.find("h2", class_="jobTitle").find_all("span")
            if len(jobTitleSpans) > 1:
                jobTitle = jobTitleSpans[1].text
            else:
                jobTitle = jobTitleSpans[0].text
            companyName = resultContent.find("span", class_="companyName").text
            companyLocation = resultContent.find("div", class_="companyLocation").text
            ratingNumberSpan = resultContent.find("span", class_="ratingNumber")
            companyRating = ratingNumberSpan.text if ratingNumberSpan is not None else "No Rating"

            job = Job(jobTitle, companyName, companyLocation, companyRating)
            jobs.append(job)
    return jobs


def writeJobsInTextFile(jobs, filePath):
    with open(filePath, "w") as textFile:
        for job in jobs:
            job.writeTextFile(textFile)


def writeJobsInCSVFile(jobs, filePath):
    with open(filePath, "w", newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Title", "Company", "Location", "Rating"])
        for job in jobs:
            job.writeCSVFile(writer)


if __name__ == "__main__":
    while True:
        # Find Jobs
        print("Finding jobs ...")

        # Query Inputs
        jobTitle = "Software Developer"
        location = "Toronto, ON"
        jobs = findIndeedJobs(jobTitle, location)
        
        # Write Jobs in Text File
        # timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        # filePath = f"files/jobPostsTextFiles/indeed_{jobTitle.replace(' ', '_')}_{timestamp}.txt"
        # print(f"Writing jobs to {filePath} ...")
        # writeJobsInTextFile(jobs, filePath)

        # Write Jobs in CSV File
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filePath = f"files/jobPostsCSVFiles/indeed_{jobTitle.replace(' ', '_')}_{timestamp}.csv"
        print(f"Writing jobs to {filePath} ...")
        writeJobsInCSVFile(jobs, filePath)

        # Wait
        waitMinutes = 1
        print(f"Waiting {waitMinutes} minutes ...")
        time.sleep(waitMinutes * 60)