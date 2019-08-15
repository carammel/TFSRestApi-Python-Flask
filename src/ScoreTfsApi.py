import requests
from requests_ntlm import HttpNtlmAuth
from src.getaccess import GetAccess
import warnings
import contextlib

from urllib3.exceptions import InsecureRequestWarning

old_merge_environment_settings = requests.Session.merge_environment_settings

class TfsApi(object):
    @contextlib.contextmanager
    def no_ssl_verification(self):
        opened_adapters = set()

        def merge_environment_settings(self, url, proxies, stream, verify, cert):
            # Verification happens only once per connection so we need to close
            # all the opened adapters once we're done. Otherwise, the effects of
            # verify=False persist beyond the end of this context manager.
            opened_adapters.add(self.get_adapter(url))

            settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
            settings['verify'] = False

            return settings

        requests.Session.merge_environment_settings = merge_environment_settings

        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', InsecureRequestWarning)
                yield
        finally:
            requests.Session.merge_environment_settings = old_merge_environment_settings

            for adapter in opened_adapters:
                try:
                    adapter.close()
                except:
                    pass
    def __init__(self, tfs_url, api_version):
        self.tfs_url = tfs_url
        self.api_version = api_version
        self.verify=False
        access = GetAccess()
        self.un = access.parse_yaml('scoreaccess', 'username')
        self.pw = access.parse_yaml('scoreaccess', 'password')

    def get_all_projects(self,collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/projects?' + self.api_version+'&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_release_metric(self, collection_name, project_name, release_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/releases?$expand=environments&definitionId=' + release_id + '&' + self.api_version
        """print(tfs_api)"""
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_release_id(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions?' + self.api_version
        """print(tfs_api)"""
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getAllRepos(self,collection_name):
        tfs_api = self.tfs_url + collection_name + "/_apis/git/repositories?apiVersion=4.1&$top=1000000"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getAllTeams(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/teams?' + self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getMetricCommit(self,collection_name, repoID,toDate,fromDate):
        tfs_api = self.tfs_url + collection_name + '/_apis/git/repositories/' + str(repoID) + \
                  '/commits?searchCriteria.toDate='+ toDate + '&searchCriteria.fromDate=' + fromDate+ '&$top=100000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()

    def getMetricChangeset(self, collection_name, csID):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets/'+ str(csID) + \
                  '/changes?fromDate=2018-01-01&toDate=2018-07-01&$top=1000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getFirstChangeset(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?searchCriteria.toDate=2019-01-01&searchCriteria.fromDate=2018-07-01&$top=10000000&'+ self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getAllBuilds(self, collection_name, project_name):
        #api-version=2.0 sayesinde bir sorguda hem xaml hem de vnext döndürebiliyorum.
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions?api-version=2.0'
        return  requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getPropertiesofBuilds(self, collection_name, project_name , build_id):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/build/definitions/' + str(build_id)+'?api-version=2.0'
        return  requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw)).json()

    def getPropertiesofReleases(self, collection, project):
        tfs_api = self.tfs_url + collection + '/' + project + '/'+'_apis/Release/definitions?%24expand=Artifacts'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_builds(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/builds?api-version=4.1"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_XAML_Requests(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/build/requests?status=Completed&api-version=4.1"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_Branches(self, collection_name):
        tfs_api = self.tfs_url + collection_name + "/_apis/branches?fromDate=2018-01-01&toDate=2018-01-07&api-version=1.0$top=1000000"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getCSbyBranch(self, collection_name, branch):
        tfs_api = self.tfs_url + collection_name + '/_apis/tfvc/changesets?searchCriteria.versionType='+branch+'&fromDate=2018-02-01&toDate=2018-03-01&$top=1000000'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getMembers(self, collection_name, projectID, teamID):
        tfs_api = self.tfs_url + collection_name + '/_apis/projects/' + projectID + '/teams/'+ teamID+ '/members?api-version=4.1-preview.2'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_releaseDefinition(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + "/_apis/release/definitions?api-version=4.1-preview.3"
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_releases(self, collection_name, project_name, definitionId):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/release/definitions/' + definitionId +'?api-version=4.1-preview.3'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_ServiceEndPoints(self, collection_name, project_name):
        tfs_api = self.tfs_url + collection_name + '/' + project_name + '/_apis/serviceendpoint/endpoints?api-version=4.1-preview.1'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def get_all_ServiceHooks(self, collection_name):
        tfs_api = self.tfs_url + collection_name + '/_apis/hooks/subscriptions?$top=1000000&api-version=4.1'
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify= False).json()

    def getAllReposofProject(self,collection_name,project_name):
        tfs_api = self.tfs_url + collection_name +"/"+project_name+ "/_apis/git/repositories?$top=1000000&"+  self.api_version
        return requests.get(tfs_api, auth=HttpNtlmAuth(self.un, self.pw),verify=False).json()
