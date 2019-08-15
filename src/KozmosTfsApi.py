import requests
from requests_ntlm import HttpNtlmAuth
from src.getaccess import GetAccess

class KozmosTfsApi(object):
    def __init__(self, tfs_url, api_version):
        self.tfs_url = tfs_url
        self.api_version = api_version
        access = GetAccess()
        self.un = access.parse_yaml('tfsaccess', 'username')
        self.pw = access.parse_yaml('tfsaccess', 'password')

    def get_all_projects(self,collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/projects?' + self.api_version+'&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getAllRepos(self,collection_name):
        tfs_api = self.tfs_url + collection_name + "/_apis/git/repositories?"+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getAllTeams(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/teams?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def get_all_ServiceEndPoints(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/serviceendpoint/endpoints?'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def get_all_ServiceHooks(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/hooks/subscriptions?$top=1000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getMembers(self, collection_name, projectID, teamID):
        tfs_api = self.tfs_url + collection_name + '/_apis/projects/' + projectID + '/teams/'+ teamID+ '/members?api-version=4.1-preview.2'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getAllReleases(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getMetricCommit(self, collection_name, repoID, toDate, fromDate):
        tfs_api = self.tfs_url + collection_name + '/_apis/git/repositories/' + str(repoID) + \
                  '/commits?searchCriteria.toDate=' + toDate + '&searchCriteria.fromDate=' + fromDate + '&$top=100000000&' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getMetricChangeset(self, collection_name, csID):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets/'+ str(csID) + \
                  '/changes?fromDate=2018-01-01&toDate=2018-07-01&$top=1000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getFirstChangeset(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?searchCriteria.toDate=2019-01-01&searchCriteria.fromDate=2018-07-01&$top=10000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getAllBuilds(self, collection_name, project_name):
        #api-version=2.0 sayesinde bir sorguda hem xaml hem de vnext döndürebiliyorum.
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions?api-version=2.0'
        return  requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getPropertiesofBuilds(self, collection_name, project_name , build_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions/' + str(build_id)+'?api-version=2.0'
        return  requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def get_XAML_Requests(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/requests?status=Completed&api-version=4.1"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def get_all_Branches(self, collection_name):
        tfs_api = self.tfs_url + collection_name + "/_apis/branches?fromDate=2018-01-01&toDate=2018-01-07&api-version=1.0$top=1000000"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getCSbyBranch(self, collection_name, branch):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?searchCriteria.versionType='+branch+'&fromDate=2018-02-01&toDate=2018-03-01&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def get_releasebyID(self, collection_name, project_name, definitionId):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions/' + \
                  str(definitionId) + '?'+self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getCommitChanges(self,collection_name, repositoryID, commitId):
        tfs_api = self.tfs_url+ collection_name + "/_apis/git/repositories/" + repositoryID + "/commits/"+commitId +"/changes?" +  self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getAllReposofProject(self,collection_name,project_name):
        tfs_api = self.tfs_url + collection_name +"/"+project_name+ "/_apis/git/repositories?$top=1000000&"+  self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()


    """"bu şekilde artifactsi alamadım
    def getPropertiesofReleases(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + \
                  '/_apis/release/definitions?%24expand=Artifacts'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()"""
