import csv
import os

def get_csv_files(directory):
    csv_files = []
    for directoryname in sorted(os.listdir(directory)):
        #print(filename)
        if os.path.isdir(os.path.join(directory, directoryname)):
            for filename in sorted(os.listdir(os.path.join(directory, directoryname))):
                if filename.endswith(".csv"):
                    csv_files.append((directoryname,filename))
    return csv_files

def read_csv(csv_path):
    with open(csv_path,encoding='utf-16') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t') 
        csv_dict = []   
        for row in csv_reader:
            timestamp = row[2][3:-3]
            csv_dict.append((row[0],timestamp))
    csv_dict.pop(0)
    return csv_dict

def get_csv_path(csv_file, directory):
    csv_path = os.path.join(directory, csv_file[0])
    csv_path = os.path.join(csv_path, csv_file[1])
    return csv_path
