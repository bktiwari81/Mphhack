import subprocess;
import sys,getopt;
import os;
def main(argv):
    #var gitreponame;
    gituri = ''
    gitproject = ''
    try:
       opts, args = getopt.getopt(argv,"hu:p:",["ifile=","ofile="])
    except getopt.GetoptError:
       print 'gitPullCMD.py -u <gitURI> -p <gitProjectName> \n for authenticated gitrepo, follow uri pattern: "https://username:password@myrepository.biz/file.git"'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'gitPullCMD.py -u <uri> -p <ProjectName> \n for authenticated gitrepo, please follow uri pattern: "https://username:password@myrepository.biz/file.git"'
          sys.exit()
       elif opt in ("-u", "--ifile"):
          gituri = arg
       elif opt in ("-p", "--ofile"):
          gitproject = arg
        
    subprocess.call(["git","init"])
    print 'Git Repo Intialized...Git clone to be started';
    subprocess.call(["git", "clone",gituri])
    print 'Git Clone done...lets get inside the folder';
    #subprocess.call(["chmod o+w",""])
    #subprocess
    #subprocess.call(["cd", gitproject])
    #folderpath = subprocess.call(["pwd"])
    os.chdir(gitproject)
    path = os. getcwd()    
    print 'inside folder:'+path;
    print 'starting npm install....'
    subprocess.call(["npm","install"])
    print 'Hurrey!!!! done!!!'
if __name__== '__main__':
    main(sys.argv[1:]);
