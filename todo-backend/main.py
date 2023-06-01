from fastapi import FastAPI
import requests
from flask import Flask
import json
 
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'
    
url = 'https://api.github.com/users/'
user = 'MeepMutyala'
token = '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'
userStats = {}

def health():
    return {"status": "ok"}

def sumAll(resp, attr):
    sum = 0
    for item in resp:
        sum+=item[attr]
    return sum

def sumForked(resp, attr):
    sum = 0
    for item in resp:
        if not item['fork']:
            sum+=item[attr]
    return sum

def sumNotForked(resp, attr):
    sum = 0
    for item in resp:
        if item['fork']:
            sum+=item[attr]
    return sum

def countNotForked(resp):
    sum = 0
    for item in resp:
        if item['fork']:
            sum+=1
    return sum

def countForked(resp):
    sum = 0
    for item in resp:
        if not item['fork']:
            sum+=1
    return sum

def setAdder(resp):
    thisSet = set()
    for item in resp:
        stringer = str(item["language"])
        thisSet.add(stringer)
    return thisSet

def setForked(resp):
    thisSet = set()
    for item in resp:
        if item['fork']:
            stringer = str(item["language"])
            thisSet.add(stringer)
    return thisSet

def setNotForked(resp):
    thisSet = set()
    for item in resp:
        if not item['fork']:
            stringer = str(item["language"])
            thisSet.add(stringer)
    return thisSet


@app.route('/<username>')
def stats(username):
    response = requests.get(url+username+'/repos', auth=(user,token))
    response = response.json()

    userStats['totalRepos'] = str(len(response))
    userStats['totalStargazers'] = str(sumAll(response, "stargazers_count"))
    userStats['totalForks'] =  str(sumAll(response, "forks_count"))
    userStats['averageRepoSize'] = str(sumAll(response, "size")/len(response))
    userStats['languages'] = list(setAdder(response))
    print(response)
    return userStats

@app.route('/<username>/forked=<forked>')
def statsForked(username, forked):
    if forked:
        response = requests.get(url+username+'/repos', auth=(user,token))
        response = response.json()
        userStats['totalStargazers'] = str(sumForked(response, "stargazers_count"))
        userStats['totalForks'] =  str(sumForked(response, "forks_count"))
        userStats['averageRepoSize'] = str(sumForked(response, "size")/countForked(response))
        userStats['totalRepos'] = str(countForked(response))
        userStats['languages'] = list(setForked(response))
        print(response)
        return userStats
    else:
        response = requests.get(url+username+'/repos', auth=(user,token))
        response = response.json()
        userStats['totalStargazers'] = str(sumNotForked(response, "stargazers_count"))
        userStats['totalForks'] =  str(sumNotForked(response, "forks_count"))
        userStats['averageRepoSize'] = str(sumNotForked(response, "size")/countNotForked(response))
        userStats['totalRepos'] = str(countNotForked(response))
        userStats['languages'] = list(setNotForked(response))
        print(response)
        return userStats

if __name__ == '__main__':
    app.run()