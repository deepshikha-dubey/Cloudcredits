import os
import sys
import hashlib
import json

# Initialize Repo
def init():
    if not os.path.exists(".myvcs"):
        os.mkdir(".myvcs")
        os.mkdir(".myvcs/commits")
        with open(".myvcs/index.json","w") as f:
            json.dump({}, f)
        print("Repository Initialized")
    else:
        print("Already Initialized")  

# Add Files  
def add(filename):
    if not os.path.exists(filename):
        print("File not found")            
        return
    with open(filename, "r") as f:
        content = f.read()

    file_hash = hashlib.sha1(content.encode()).hexdigest()

    with open(".myvcs/index.json", "w") as f:
        index = json.load(f)

    index[filename] = file_hash

    with open(".myvcs/index.json", "w") as f:   
        json.dump(index, f)

    print(f"{filename} added")   

# Commit Changes
def commit(message):
    with open(".myvcs/index.json", "r") as f:
        index = json.load(f)
    commit_id = hashlib.sha1(message.encode()).hexdigest()

    commit_data = {
        "message" : message,
        "files" : index
    }
  
    with open(f".myvcs/commits/{commit_id}.json", "w") as f:
        json.dump(commit_data, f)
    print("Commit saved:", commit_id)

# Show Log
def log():
    commits = os.listdir(".myvcs/commits")
    for commit_file in commits:
        with open(f".myvcs/commits/{commit_file}", "r") as f:
            data = json.load(f)
            print("Commit:", commit_file)
            print("Message:", data["message"])
            print("-" * 20)

# CLI Support
    if __name__ == "__main__":
       command = sys.argv[1]
       if command == "init":
           init()
       elif command == "add":
           add(sys.argv[2]) 
       elif command == "commit":
           commit(sys.argv[2])
       elif command == "log":
           log()    
                
                     
