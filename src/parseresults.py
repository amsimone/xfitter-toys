#!/bin/python3
### Parse the content of fittedresults 

import glob,re,os
import numpy as np
import pandas as pd
import io
import f90nml
import shutil
import pprint

def replacedata(inputfile, itoy, toydata):
    print(inputfile)
    with open(inputfile) as f:
        content = f.read()

    # Find the last occurrence of "&End" 
    end_index = content.rfind("&End")
    if end_index == -1:
        raise ValueError("No &End found in file")

    # Extract the header and data
    header = content[:end_index+len("&End")]
    data = content[end_index+len("&End"):]

    # Remove lines starting with "!" or "*" from data
    data = "\n".join(line for line in data.split("\n") if not line.startswith("!") and not line.startswith("*"))

    # Search for the line containing the column names
    column_names = None
    for line in header.split("\n"):
        if 'ColumnName' in line:
            column_names = line
            break
    column_names = column_names.strip().split('=')[1].split(',')

    ## Cleanup column names and remove quotation marks
    column_names = [element.strip() for element in column_names if element.strip()]
    column_names = [element.strip('"').strip("'") for element in column_names]

    # parse data into dataframe
    mdf = pd.read_csv(io.StringIO(data),delim_whitespace=True)
    mdf.columns=column_names
    print(mdf.columns)
    #replace data with pseudodata
    mdf.Sigma = toydata

    # Create output folder to store toys                                                                                                 
    outfolder = 'output_toys/'+str(itoy)+'/'
#    if os.path.exists(outfolder):
#        shutil.rmtree(outfolder)
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    # save toy to output file
    outfilename = inputfile.split('/')[-1].split('.')[0]
    #outfilename = outfolder+"/"+outfilename+'_'+str(itoy)+'.txt'
    outfilename = outfolder+"/"+outfilename+'.txt'
    print(outfilename)
    with open(outfilename, "w", encoding="utf-8") as file:
        file.write(header+'\n')
        mdf.to_csv(file, index=False,header=False,sep='\t')
    file.close()

    # Print the results                                                                                                
    #print("Header:")
    #print(header)
    #print("Data:")
    #print(data)
    #print(column_names)

# Dictionary to store pseudodata for each toy and dataset
toys = {}

# Get a list of all files starting with "fittedresults"
files = glob.glob('toys_output/fittedresults*.txt')

itoy=1
# Loop over each file and open it
for file in files:
    with open(file, 'r') as f:        
        # Do something with the file
        #        print(f.read())
        contents = f.read()
        print('processing toy - ', file)

        # Split the contents into sections based on the tags
        sections = re.split(r'BEGINDATASET|ENDDATASET', contents)

        # Remove any empty sections
        sections = [section.strip() for section in sections if section.strip()]

        # Remove first  section (contains number of plots)
        sections = sections[1:]

    # Process each section
    for section in sections:
        print('New section:')

        #Read Datasetname, Datasetindex, Datasetfile
        datasetindex = section.split('\n')[0]
        print('Datasetindex=',datasetindex, itoy)
        datasetname = section.split('\n')[1]
        print('Datasetname=',datasetname, itoy)
        datasetfile = section.split('\n')[2].split('=')[1].strip()
        print('Datasetfile=',datasetfile, itoy)
        
        #convert content to dataframe
        df = pd.read_csv(io.StringIO(section), skiprows=3,delim_whitespace=True)
#        print(df.data)
        
        #Read cross-sections and put them back to dictionary
        #        toys[(datasetname, itoy)] = df.data 

        replacedata(datasetfile, itoy, df.data)

    # Increase the toy counter
    itoy += 1

