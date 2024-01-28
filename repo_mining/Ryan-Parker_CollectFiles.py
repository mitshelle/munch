"""Ryan-Parker_CollectFiles.py: This file uses the github api to retrieve
		a list of all source files in a given repository"""

# Note: This file was taken from the github repository johnxu21/msrLab and
#           modified to only report the source files in a repository


import json
import requests
import csv

import os

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
	jsonData = None
	try:
		ct = ct % len(lsttoken)
		headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
		request = requests.get(url, headers=headers)
		jsonData = json.loads(request.content)
		ct += 1
	except Exception as e:
		pass
		print(e)
	return jsonData, ct


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
	ipage = 1  # url page counter
	ct = 0  # token counter

	try:
		# loop through all the commit pages until the last returned empty page
		while True:
			spage = str(ipage)
			commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
			jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

			# break out of the while loop if there are no more commits in the pages
			if len(jsonCommits) == 0:
				break
			# iterate through the list of commits in  spage
			for shaObject in jsonCommits:
				sha = shaObject['sha']
				# For each commit, use the GitHub commit API to extract the files touched by the commit
				shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
				shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
				filesjson = shaDetails['files']
				for filenameObj in filesjson:
					filename = filenameObj['filename']

					# Check if the file has a source code extension
					source_code_extensions = ['.java', '.kt', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.c']
					if any(filename.endswith(ext) for ext in source_code_extensions):
						dictfiles[filename] = dictfiles.get(filename, 0) + 1
						print(filename)

			ipage += 1
	except:
		print("Error receiving data")
		exit(0)


def main():
	# * This makes the data directory if not already made
	if not os.path.exists("data"):
		os.makedirs("data")


	# * Leave repo the same, in order to test against the image on the assignment
	# GitHub repo
	repo = 'scottyab/rootbeer'
	# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
	# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
	# repo = 'mendhak/gpslogger'


	# ! Must remember to remove tokens before commiting
	# put your tokens here
	# Remember to empty the list when going to commit to GitHub.
	# Otherwise they will all be reverted and you will have to re-create them
	# I would advise to create more than one token for repos with heavy commits
	lstTokens = [""] # 


	dictfiles = dict()
	countfiles(dictfiles, lstTokens, repo)
	print('Total number of files: ' + str(len(dictfiles)))


	# * Creating name and path to file
	file = repo.split('/')[1]
	fileOutput = 'data/file_' + file + '.csv'

	# * Set up the output file
	rows = ["Filename", "Touches"]
	fileCSV = open(fileOutput, 'w')
	writer = csv.writer(fileCSV)
	writer.writerow(rows)


	bigcount = None
	bigfilename = None
	for filename, count in dictfiles.items():
		rows = [filename, count]
		writer.writerow(rows)
		if bigcount is None or count > bigcount:
			bigcount = count
			bigfilename = filename
	fileCSV.close()
	print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')


if __name__ == "__main__":
	main()