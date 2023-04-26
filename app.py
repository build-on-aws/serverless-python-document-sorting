import os
import glob
import boto3
import hashlib

# get list of files in directory
def get_files():
    files = glob.glob("docs/*.pdf")
    return files

# iterate through textract response, printing the text
def get_text(response):
    result = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            result.append(item["Text"])
        if item["BlockType"] == "WORD":
            result.append(item["Text"])
    return result
        
# with boto3, use textract to analyze the document
def analyze_document(bytes):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={
            'Bytes': bytes
        },
        FeatureTypes=["TABLES", "FORMS"]
    )
    return response

# read the bytes of a file
def read_file(file):
    with open(file, 'rb') as f:
        return f.read()

# create an md5 hash of byte array
def md5_hash(bytes):
    return hashlib.md5(bytes).hexdigest()




def main():
    # iterate through list of files
    files = get_files()

    # create a dictionary of files and their md5 hashes
    md5_dict = {}
    duplicates = []

    print("your files")
    for x in range (len(files)):
        # print each file name to the console
        print(files[x])
        # check for json version of the document
        if os.path.isfile(files[x]+ '.json'):
            print("json file already exists")
            with open(files[x]+ '.json', 'r', encoding='utf-8') as f:
            
                #result =get_text(f.read())
                res = f.read()
                # if the md5 hash of the text is in the dictionary, 
                # add the file to the duplicate list
                if md5_hash(res.encode('utf-8')) in md5_dict:
                    duplicates.append(files[x])
                else:
                    # add the md5 hash to the dictionary
                    md5_dict[md5_hash(res.encode('utf-8'))] = files[x]
                    #save the result in a text file
                    with open(files[x]+ '.txt', 'w') as f:
                        f.write(str(res))
                    f.close()
                   
        else:
            bytes = read_file(files[x])
            response = analyze_document(bytes)
            # write response in a a json file
            with open(files[x]+ '.json', 'w') as f:
                f.write(str(response))
                f.close()
                print("json response saved")
                result = get_text(response)
                if md5_hash(str(bytes).encode('utf-8')) in md5_dict:
                    print("DEBUG: Duplicates found")
                    duplicates.append(files[x])
                else:
                    md5_dict[md5_hash(str(bytes).encode('utf-8'))] = files[x]
                    #save the result in a text file
                    print("DEBUG: Duplicates NOT found")
                    with open(files[x]+ '.txt', 'w') as f:
                        f.write(str(result))

    print("---------------------------------------------")
    print(duplicates)

if __name__ == "__main__":
    main()