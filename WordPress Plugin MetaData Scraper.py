from os import listdir
from os.path import isfile, join, isdir
import tkinter as tk
from tkinter import filedialog
import xlsxwriter

#Author: Kyle Wilson
#Last updated: 8.6.2017

#PROGRAM ABSTRACT
#Purpose:
#This program is designed to crawl through a WordPress Plugin directory and pull
#information about the plugins.

#Background Knowledge:
#A WordPress plugin has a PHP file that contains a large comment block at the beginning
#that contains useful metadata. This program uses this fact to pull the information.

#Function Description:
#Get path of a plugin directory -> Find and read the plugin's php file ->
#Pull the PHP comment block (contains metadata) out of the php file ->
#Display the relevant info

#get list of paths for WP plugins
def getPath(pluginDirPath): 
    onlydirs = [join(pluginDirPath,o) for o in listdir(pluginDirPath) if isdir(join(pluginDirPath,o))]
    return onlydirs

#outputs the content of the PHP file
def readFiles(path):
    #find all files in directory
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    filesToRead = [] #this list will contain only the PHP file we should read
    toReturn = [] #the array we will return with content of files

    #pick out php files
    for file in onlyfiles:
        if(file[-4:] == ".php"):
           filesToRead.append(file)

    #if there are multiple PHP files there is a problem
    if(len(filesToRead) > 1):
        print("FILE ERROR: Too many PHP files")
        filesToRead = handleError(filesToRead)
        print("")
        print("")
    
    #loop through appropriate file(s) and return their content
    for myFile in filesToRead:
        with open(path + '\\' + myFile) as f:
           content = f.readlines()
        content = [x.strip() for x in content]
    for line in content:
        toReturn.append(line)
    
    return toReturn

#returns PHP comment block line by line in a list
def pullInfo(pageContent):
    startIndex = 0 #beginning index of metadata comment
    endIndex = 0 #end index of metadata comment

    #find starting and ending indicies for the PHP comment block
    for x in range(0, len(pageContent)):
        if(pageContent[x] == '/*' and startIndex == 0):
            startIndex = x
            #print("Starting index: " + x)
        if(pageContent[x] == '*/' and endIndex == 0):
            endIndex = x
            #print("Ending index: " + x)
            break

    #isolate PHP metadata comment
    comment = []
    for i in range(startIndex, endIndex+1):
        comment.append(pageContent[i])

    #break apart comment line by line
    toReturn = []
    for line in comment:
        toReturn.append(line)
    return toReturn

#request user intervention for finding correct PHP file to scan
def handleError(fileArray):
    #display all possible answers
    for i in range(0, len(fileArray)):
        print(str(i) + ": " + fileArray[i])
    #error handling for user picking correct file number
    while(True):
        print("Enter the number of the correct file")
        correctFileNum = int(input())
        if(correctFileNum < len(fileArray) and correctFileNum > 0):
            #print("DEBUG 1")
            break
    #return correct file name as a list
    toReturn = []
    toReturn.append(fileArray[correctFileNum])
    return toReturn

#display data to console
def displayInfo(data):
    for x in range(0, len(data)-1):
        #Erase blank space or * from beginning of lines
        while(data[x][:1] == " " or data[x][:1] == "*"):
            data[x] = data[x][1:]
        #find relevant data and print it
        if(data[x][:12] == "Plugin Name:" or data[x][:8] == "Version:" or data[x][:7] == "Author:"):
            print(data[x])

#write to file
def formatData(data):
    toReturn = []
    for x in range(0, len(data)-1):
        #Erase blank space or * from beginning of lines
        while(data[x][:1] == " " or data[x][:1] == "*"):
            data[x] = data[x][1:]
        #find relevant data and print it
        if(data[x][:12] == "Plugin Name:" or data[x][:8] == "Version:" or data[x][:7] == "Author:"):
            toReturn.append(data[x]+"\n")
    toReturn.append("\n\n")
    return toReturn

#run program
def run(plugin_path):
    #loop through all subdirectories in plugin dir
    toPrint = []
    for i in range(0, len(getPath(plugin_path))):
        toPrint.extend(formatData(pullInfo(readFiles(getPath(plugin_path)[i]))))
        #displayInfo(pullInfo(readFiles(getPath(plugin_path)[i])))
    f = open('report.txt', 'w')
    for x in toPrint:
        f.write(x)
    f.close()

#main
print("Select Plugin Directory")
root=tk.Tk()
root.withdraw()
plugin_path = filedialog.askdirectory()

run(plugin_path)
