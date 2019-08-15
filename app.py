from flask import render_template, request, url_for, redirect, Flask
from src.ScoreTfsApi import TfsApi
from src.KozmosTfsApi import KozmosTfsApi
from urllib3.exceptions import InsecureRequestWarning
import warnings
import contextlib
import requests
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
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

@app.route('/')
def hi():
    return 'Hello World!'

@app.route('/Home', methods=['POST', 'GET'])
def home():
    if request.method=="POST":
        tfs = request.form['tfs']
        collectionName = request.form['collectionName']
        projectName = request.form['projectName']
        submitName =request.form['submitName']
        toDate = request.form['toDate']
        fromDate = request.args.get('fromDate')
        return redirect(url_for('showInfo',tfs=tfs,collectionName=collectionName, projectName=projectName, submitName= submitName, toDate=toDate, fromDate=fromDate))
    return render_template("home.html")

@app.route('/showInfo', methods=['GET'])
def showInfo():
    tfs = request.args.get('tfs')
    collectionName = request.args.get('collectionName')
    projectName = request.args.get('projectName')
    submitName = request.args.get('submitName')
    toDate = request.args.get('toDate')
    fromDate = request.args.get('fromDate')
    teamName = str(projectName) + " Team"
    ScoreTfs = TfsApi(tfs_url="***", api_version='api-version=4.1-preview.1')
    KozmosTfs = KozmosTfsApi(tfs_url="***", api_version='api-version=4.1-preview.1')
    if submitName == "serviceHooks":
        if (tfs == "****"):
            SE = {}
            ScoreTFSRepoDict ={}
            #ScoreTFSProjectIDDict ={}
            DE= {}
            Scorerepos = ScoreTfs.getAllReposofProject(collection_name=collectionName,project_name=projectName)
            projectID = Scorerepos['value'][0]['project']['id']
            for repo in Scorerepos['value']:
                #liste.append(repo['project']['id'])
                ScoreTFSRepoDict[repo['id']] = repo['name']
            serviceHook = ScoreTfs.get_all_ServiceHooks(collection_name=collectionName)
            for val in serviceHook['value']:
                if projectID == val['publisherInputs']['projectId']:
                    DE[val['publisherInputs']['repository']] = val
                    #SE[val['name']] = val['type']
            return render_template("serviceHook.html",DE=DE,projectName1=projectName)
        elif (tfs == "***"):
            KozmosTSRepoDict = {}
            DE = {}
            Kozmosrepos = KozmosTfs.getAllReposofProject(collection_name=collectionName, project_name=projectName)
            projectID = Kozmosrepos['value'][0]['project']['id']
            for repo in Kozmosrepos['value']:
                KozmosTSRepoDict[repo['id']] = repo['name']
            serviceHook = KozmosTfs.get_all_ServiceHooks(collection_name=collectionName)
            for val in serviceHook['value']:
                if projectID == val['publisherInputs']['projectId']:
                    DE[val['publisherInputs']['repository']] = val
            return render_template("serviceHook.html", DE=DE, projectName1=projectName)
    elif submitName ==  "serviceEndpoint":
        if (tfs == "****"):
            SE = {}
            serviceHook = ScoreTfs.get_all_ServiceEndPoints(collection_name=collectionName,project_name=projectName)
            for val in serviceHook['value']:
                SE[val['name']] = val['type']
            return render_template("serviceEndpoint.html",SE=SE,projectName1=projectName)
        elif (tfs == "****"):
            SE = {}
            serviceHook = KozmosTfs.get_all_ServiceEndPoints(collection_name=collectionName,project_name=projectName)
            for val in serviceHook['value']:
                SE[val['name']] = val['type']
            return render_template("serviceEndpoint.html",SE=SE,projectName1=projectName)
    elif submitName == "members":
        if (tfs == "****"):
            SE = {}
            Members = ScoreTfs.getMembers(collection_name=collectionName,projectID=projectName,teamID=teamName)
            for val in Members['value']:
                SE[val['identity']['displayName']] = val['identity']['uniqueName']
            return render_template("security.html",SE=SE,projectName1=projectName)
        elif (tfs == "****"):
            SE = {}
            Members = KozmosTfs.getMembers(collection_name=collectionName,projectID=projectName,teamID=teamName)
            for val in Members['value']:
                SE[val['identity']['displayName']] = val['identity']['uniqueName']
            return render_template("security.html",SE=SE,projectName1=projectName)
    elif submitName == "commits":
        if (tfs == "****"):
            DE = {}
            Scorerepos = ScoreTfs.getAllReposofProject(collection_name=collectionName, project_name=projectName)
            projectID = Scorerepos['value'][0]['project']['id']
            for repo in Scorerepos['value']:
                ID = repo['id']
                repoName = repo['name']
                commitsAll= ScoreTfs.getMetricCommit(collection_name=collectionName, repoID= ID, toDate=toDate,
                                         fromDate=fromDate)
                for val in commitsAll['value']:
                    DE[val['commitId']] = val
            return render_template("commit.html",DE=DE ,projectName1=projectName)
        elif (tfs == "****"):
            DE = {}
            Kozmosrepos = KozmosTfs.getAllReposofProject(collection_name=collectionName, project_name=projectName)
            projectID = Kozmosrepos['value'][0]['project']['id']
            for repo in Kozmosrepos['value']:
                ID = repo['id']
                commitsAll= KozmosTfs.getMetricCommit(collection_name=collectionName, repoID= ID, toDate=toDate,
                                         fromDate=fromDate)
                for val in commitsAll['value']:
                    DE[val['commitId']] = val
            return render_template("commit.html",DE=DE ,projectName1=projectName)
    elif submitName == "releaseProperty":
        if (tfs == "****"):
            return ("Scoretfs'teki projeler için release tanımları oluşturulmaz. Score.isbank veya XLR üzerinden "
                    "projenizin sürüm akışını inceleyebilirsiniz")
        elif (tfs == "****"):
            ReleaseAllProperty = {}
            release_ids=KozmosTfs.getAllReleases(collection_name=collectionName,project_name=projectName)
            releaseIDList = []
            for release_id in release_ids['value']:
                id = release_id['id']
                name = release_id['name']
                releaseIDList.append(id)
            for i in releaseIDList:
                releaseDefs = KozmosTfs.get_releasebyID(collection_name=collectionName, project_name=projectName,definitionId=i)
                ReleaseAllProperty[releaseDefs['name']]=releaseDefs
            return render_template("releaseProperty.html",DE=ReleaseAllProperty,projectName1=projectName)
    elif submitName == "buildProperty":
        if (tfs == "****"):
            buildAllPropertyxaml = {}
            buildAllPropertyvNext = {}
            build_ids = ScoreTfs.getAllBuilds(collection_name=collectionName, project_name=projectName)
            buildIDList = []
            for build_id in build_ids['value']:
                id = build_id['id']
                buildIDList.append(id)
            for i in buildIDList:
                tfvcMappings = ScoreTfs.getPropertiesofBuilds(collection_name=collectionName, project_name=projectName,
                                                               build_id=i)
                buildAllPropertyvNext[tfvcMappings['name']] = tfvcMappings
            return render_template("buildProperty.html", vNext=buildAllPropertyvNext, projectName1=projectName)
        elif (tfs == "****"):
            buildAllPropertyxaml = {}
            buildAllPropertyvNext = {}
            build_ids=KozmosTfs.getAllBuilds(collection_name=collectionName,project_name=projectName)
            buildIDList = []
            for build_id in build_ids['value']:
                id = build_id['id']
                buildIDList.append(id)
            for i in buildIDList:
                tfvcMappings = KozmosTfs.getPropertiesofBuilds(collection_name=collectionName, project_name=projectName,build_id=i)
                try:
                    if tfvcMappings['type'] == "build":
                        buildAllPropertyvNext[tfvcMappings['name']] = tfvcMappings
                    elif tfvcMappings['type'] == "xaml":
                        buildAllPropertyxaml[tfvcMappings['name']]= tfvcMappings
                except:
                    continue
        return render_template("buildProperty.html",vNext=buildAllPropertyvNext,xaml=buildAllPropertyxaml,
                                   projectName1=projectName)
    elif submitName == "AllProjects":
        if (tfs == "****"):
            SE = {}
            AllProjects = ScoreTfs.get_all_projects(collection_name=collectionName)
            for val in AllProjects['value']:
                SE[val['name']] = val
            return render_template("projectList.html",SE=SE,collectionName1=collectionName)
        elif (tfs == "****"):
            SE = {}
            AllProjects = KozmosTfs.get_all_projects(collection_name=collectionName)
            for val in AllProjects['value']:
                SE[val['name']] = val
            return render_template("projectList.html",SE=SE,collectionName1=collectionName)
    else:
        return 'Aman Tanrıııımm'

if __name__ == '__main__':
    app.run(host="localhost", port=5000 ,debug = True)