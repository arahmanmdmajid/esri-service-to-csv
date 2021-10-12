# Reads the following properties from services and writes them to a comma-delimited file:
#  ServiceName, Folder, Type, Status, Min Instances, Max Instances, KML,
#  WMS, Max Records, Cluster, Cache Directory, Jobs Directory, Output Directory

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# For HTTP calls
import httplib, urllib, json, requests

# For system tools
import sys

# For reading passwords without echoing
import getpass

def main(argv=None):
    
    # Ask for admin/publisher user name and password
    username = raw_input("Enter user name: ")
    password = getpass.getpass("Enter password: ")

    # Ask for server name & port
    serverName = raw_input("Enter server name: ")
    serverPort = 6443

    # Get the location and the name of the file to be created
    resultFile = raw_input("Output File: ")

    # Get a token
    token = getToken(username, password, serverName, serverPort)

    # Get the root info
    serverURL = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/"

    # This request only needs the token and the response formatting parameter 
    params = {'token': token, 'f': 'json'}

    # Connect to URL and post parameters
    response = requests.post(serverURL, data=params)

    # Read response
    if (response.status_code != 200):
        print "Could not read folder information."
        return
    else:
        # Deserialize response into Python object
        dataObj = json.loads(response.text)

        #Store the Folders in a list to loop on
        folders = dataObj["folders"]

        #Remove the System and Utilities folders
        folders.remove("System")
        #folders.remove("Utilities")

        #Add an entry for the root folder
        folders.append("")

        #Create the summary file of services
        serviceResultFile = open(resultFile,'w')
        serviceResultFile.write("ServiceName,Folder,Type,Status,Min Instances,Max Instances,FeatureService,kml,wms,Max Records,Cluster,Cache Directory,Jobs Directory,Output Directory" + "\n")

        #Loop on the found folders and discover the services and write the service information
        for folder in folders:
            
            # Determine if the loop is working on the root folder or not
            if folder != "":
                folder += "/"

            # Build the URL for the current folder
            folderURL = serverName + ":"+ str(serverPort) +"/arcgis/admin/services/" + folder
            params = {'token': token, 'f': 'json'}

            # Connect to URL and post parameters    
            response = requests.post(folderURL, data=params)

            # Read response
            if (response.status_code != 200):
                print "Could not read folder information."
                return
            else:
                # Deserialize response into Python object
                dataObj = json.loads(response.text)

                # Loop through each service in the folder   
                for item in dataObj['services']:

                    if item["type"] == "GeometryServer":# and folder == "":
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])
                       
                        
                        
                        servResponse = requests.post(sUrl, data=params)
                        
                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        # Build the Service URL to test the running status
                        

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Obtain the data from the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["clusterName"]) + "," + "NA" + "," + "NA" + "," + "NA" +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    elif item["type"] == "SearchServer":# and folder == "":
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])
                       
                        
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)


                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)
                        
                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["clusterName"]) + "," + "NA" + "," + str(jsonOBJ["properties"]["jobsDirectory"]) + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    elif item["type"] == "ImageServer":
                        
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        # Build the Service URL to test the running status
                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Extract the WMS properties from the response
                        wmsProps = [imageWMS for imageWMS in jsonOBJ["extensions"] if imageWMS["typeName"] == 'WMSServer']#.items()[0][1] == 'WMSServer']

                        if len(wmsProps) > 0:
                            wmsStatus = str(wmsProps[0]["enabled"])
                        else:
                            wmsStatus = "NA"

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + wmsStatus +"," + "NA" + "," + str(jsonOBJ["clusterName"]) + "," + str(jsonOBJ["properties"]["cacheDir"]) + "," + "NA," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file               
                        serviceResultFile.write(ln)
                        
                        
                    elif item["type"] == "GlobeServer":
                 
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        #Build the Service URL to test the running status
                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["properties"]["maxRecordCount"]) + "," + str(jsonOBJ["clusterName"]) + "," + str(jsonOBJ["properties"]["cacheDir"]) + "," + "NA" + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    elif item["type"] == "GPServer":
             
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        # Build the Service URL to test the running status
                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["clusterName"]) + "," + "NA" + "," + str(jsonOBJ["properties"]["jobsDirectory"]) + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)                        
                        
                    elif item["type"] == "GeocodeServer":

                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["clusterName"]) + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    elif item["type"] == "GeoDataServer":
     
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])
                            
                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Build the line to write to the output file
                        ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "NA" + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["properties"]["maxRecordCount"]) + "," + str(jsonOBJ["clusterName"]) + "," + "NA" + "," + "NA" + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    elif item["type"] == "MapServer":
               
                        # Build the Service URL
                        if folder:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s" %(folder,item["serviceName"], item["type"])
                        else:
                            sUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servResponse = requests.post(sUrl, data=params)

                        # Get the response
                        jsonOBJ = json.loads(servResponse.text)

                        # Build the Service URL to test the running status
                        if folder:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s%s.%s/status" %(folder,item["serviceName"], item["type"])
                        else:
                            statusUrl = serverName + ":"+ str(serverPort) + "/arcgis/admin/services/%s.%s/status" %(item["serviceName"], item["type"])

                        # Submit the request to the server
                        servStatusResponse = requests.post(statusUrl, data=params)

                        # Get the response
                        jsonOBJStatus = json.loads(servStatusResponse.text)

                        # Check for Map Cache
                        isCached = jsonOBJ["properties"]["isCached"]
                        if isCached == "true":
                            cacheDir = str(jsonOBJ["properties"]["cacheDir"])
                        else:
                            cacheDir = jsonOBJ["properties"]["isCached"]

                        if len(jsonOBJ["extensions"]) == 0:
                            # Build the line to write to the output file
                            ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + "FeatServHolder" + "," + "Disabled" + "," + "Disabled" +"," + str(jsonOBJ["properties"]["maxRecordCount"]) + "," + str(jsonOBJ["clusterName"]) + "," + cacheDir + "," + "NA" + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"
                        else:
                            # Extract the KML properties from the response
                            kmlProps = [mapKML for mapKML in jsonOBJ["extensions"] if mapKML["typeName"] == 'KmlServer']#.items()[0][1] == 'KmlServer']

                            # Extract the WMS properties from the response
                            wmsProps = [mapWMS for mapWMS in jsonOBJ["extensions"] if mapWMS["typeName"] == 'WMSServer']#.items()[0][1] == 'WMSServer']

                            # Extract the FeatureService properties from the response
                            featServProps = [featServ for featServ in jsonOBJ["extensions"] if featServ["typeName"] == 'FeatureServer']#.items()[0][1] == 'FeatureServer']

                            if len(featServProps) > 0:
                                featureStatus = str(featServProps[0]["enabled"])
                            else:
                                featureStatus = "NA"

                            if len(kmlProps) > 0:
                                kmlStatus = str(kmlProps[0]["enabled"])
                            else:
                                kmlStatus = "NA"

                            if len(wmsProps) > 0:
                                wmsStatus = str(wmsProps[0]["enabled"])
                            else:
                                wmsStatus = "NA"

    
                            ln = str(jsonOBJ["serviceName"]) + "," + folder + "," + str(item["type"]) + "," + jsonOBJStatus['realTimeState'] + "," + str(jsonOBJ["minInstancesPerNode"]) + "," + str(jsonOBJ["maxInstancesPerNode"]) + "," + featureStatus + "," + kmlStatus + "," + wmsStatus +"," + str(jsonOBJ["properties"]["maxRecordCount"]) + "," + str(jsonOBJ["clusterName"]) + "," + cacheDir + "," + "NA" + "," + str(jsonOBJ["properties"]["outputDir"]) +"\n"

                        # Write the results to the file
                        serviceResultFile.write(ln)
                        
                    else:
                        print("All layers traversed")
                        
        # Close the file
        serviceResultFile.close()

def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"
    
    params = {'username': username, 'password': password, 'client': 'requestip', 'f': 'json'}
    
    url = serverName + ":"+ str(serverPort) + tokenURL
    
    # Post parameters to url
    response = requests.post(url, data=params)
      
    # Read response
    if (response.status_code != 200):
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        # Extract the token from it
        token = response.json()        
        return token['token']            
        

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
