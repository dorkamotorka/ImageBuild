#!/usr/bin/env python

import sys
import xmltodict
from urllib.request import urlopen
import os
import subprocess
import dateutil.parser
from os import path

def execute(command, cwd):
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    return proc.communicate()[0], proc.returncode

class accessDatabase:
    def __init__(self, package):
        self.url = "https://ubiquity-pi-image.sfo2.cdn.digitaloceanspaces.com/"
        self.package_tag = package
        self.home = "/home/ubuntu"

    def connects_to_url(self):
        data, code = execute('timeout 20s wget -q --spider ' + self.url, "/tmp/")
        return code == 0

    def fetch_latest_online(self):
        # try to fetch the latest package file from web
        if not self.connects_to_url():
          msg = "Could not connect to " + self.url
          print(msg)
          return 0

        try:
          file = urlopen(self.url)
          data = file.read()
          file.close()

          data = xmltodict.parse(data)["ListBucketResult"]["Contents"]
        except:
          print("Fetching latest: HTTP Error 503: Service Unavailable.")
          execute("sudo date -s \"$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z\"", "/tmp/")
          return 0

        allpackages = []
        for val in data:
          allpackages.append({'date': dateutil.parser.parse(str(val["LastModified"])), 'file': str(val["Key"]),})

        packages = []
        for val in allpackages:
          if self.package_tag in val["file"]:
            packages.append(val)

        if len(packages) == 0:
          msg = "No package file found online with package tag: "+self.package_tag
          print(msg)
          return 0

        newlist = sorted(packages, key=lambda k: k['date'])
        latest = str(newlist[len(newlist)-1]["file"])

        return latest

    def is_pkg_different_then_current(self, pkg_name):
        if not path.exists(self.home):
          print("Directory "+self.home+" does not exist")
          return -1

        # Check if package already installed in the home directory
        if os.path.exists(os.path.join(self.home, pkg_name)):
            return False

        return True

    def trigger_download(self, package_name):
        self.update_command_list(package_name)
        execute_success, message = self.execute_command_list()
        if execute_success:
          print("Successfully downloaded new distribution")
        else:
          print("There was an error downloading update: %s", message)

        return

    def execute_command_list(self):
        for command in self.commandlist:
          # print out the message of the command
          print(command[2])

          # execute the comand
          streamdata, code = execute(command[0], command[1])
          streamdata = str((str(streamdata[1000:]) + '..') if len(streamdata) > 1000 else streamdata)
          # print out the response of the command
          if len(streamdata) > 0:
            print(streamdata)

          # if there is a error in the execution, return false
          if code != 0:
            msg = "Could not exectue command: " + str(command[0]) + " because: " + stretamdata
            print(msg)
            return False, msg

        return True, "Success executing command list"

    def update_command_list(self, package_name):
        self.commandlist = [
            # delete old zip and cyacd files in home dir
            #["find . -maxdepth 1 -name '*.zip' -type f -delete",	       self.home,		"Removing old zip file..."],
            # first download to tmp and then move to home dir so package updates could not be executed with half-downloaded zip.
            # also if download is stopped mid way because of network loss, the download is automatically restarted because the file was
            # not dowloaded directly into ~/
            ["wget --no-check-certificate "+self.url+package_name,		        "/tmp/",	          	"Downloading package to tmp..."],
            ["mv "+package_name+" "+self.home,	      	                "/tmp/",	          	"Moving from tmp to home..."],
            # unzip everything to home dir and then remove src, build devel -> so only cyacd files (and others?) remain in home dir
            ["unxz "+os.path.join(self.home, package_name),	        			        self.home,		"Extracting package..."],
        ]

if __name__ == '__main__':
    ad = accessDatabase('breadcrumb')
    latest_fetched_package = ad.fetch_latest_online() 
    if latest_fetched_package == 0:
      print("Could not fetch latest package from " + ad.url)
    else:
      print("Found package: "+latest_fetched_package+", proceeding.")

    # if there was a package file fetched
    if latest_fetched_package != 0:
      # first compare it to the currently installed package
      diff = ad.is_pkg_different_then_current(latest_fetched_package)
      if diff == False:
        print("The latest package is already downloaded")
        sys.exit()
      elif diff == True:
        ad.trigger_download(latest_fetched_package)
      else:
        print("There was an error checking difference between installed and fetched files")
    else: 
        print("Failed to fetch package")
