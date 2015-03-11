#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup

class AppleJobsScraper(object):
    def __init__(self):
        self.search_request = {
            "searchString":"",
            "jobType":0,
            "sortBy":"req_open_dt",
            "sortOrder":"1",
            "language":None,
            "autocomplete":None,
            "delta":0,
            "numberOfResults":0,
            "pageNumber":None,
            "internalExternalIndicator":0,
            "lastRunDate":0,
            "countryLang":None,
            "filters":{
                "locations":{
                    "location":[{
                            "type":0,
                            "code":"USA",
                            "countryCode":None,
                            "stateCode":None,
                            "cityCode":None,
                            "cityName":None
                    }]
                },
                "languageSkills":None,
                "jobFunctions":None,
                "retailJobSpecs":None,
                "businessLine":None,
                "hiringManagerId":None},
            "requisitionIds":None
        }

    def scrape(self):
        jobs = self.scrape_jobs()
        for job in jobs:
            print job

    def scrape_jobs(self, max_pages=3):
        jobs = []
        pageno = 0
        self.search_request['pageNumber'] = pageno

        while pageno < max_pages:
            payload = { 
                'searchRequestJson': json.dumps(self.search_request),
                'clientOffset': '-300'
            }

            r = requests.post(
                url='https://jobs.apple.com/us/search/search-result',
                data=payload,
                headers={
                    'X-Requested-With': 'XMLHttpRequest'
                }
            )

            s = BeautifulSoup(r.text)
            if not s.requisition:
                break

            for r in s.findAll('requisition'):
                job = {}
                job['jobid'] = r.jobid.text
                job['title'] = r.postingtitle and \
                    r.postingtitle.text or r.retailpostingtitle.text
                job['location'] = r.location.text
                jobs.append(job)

            # Next page
            pageno += 1
            self.search_request['pageNumber'] = pageno

        return jobs

if __name__ == '__main__':
    scraper = AppleJobsScraper()
    scraper.scrape()
