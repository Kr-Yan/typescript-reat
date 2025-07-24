# For file I/O (input/output) operations
import json
from pathlib import Path
from typing import List
from app.models.user import UserWithPassword

class DataService:
    def __init__(self):
        # Load users from JSON file
        self.data_file= Path(__file__).parent.parent /"data" /"users.json"

    def load_users(self) -> List[UserWithPassword]:
        try:

            if self.data_file.exists():
                with open(self.data_file,'r') as f: #read file in the path
                    user_data=json.load(f)
                    #convert json file to UserWithPassword objects
                    return [UserWithPassword(**user) for user in user_data] #dictionary unpack operator-> map a json file to a defined object
            else:
                print(f"Users file not found: {self.data_file}")
                return []
        except Exception as e:
            print(f"Error loading users: {e}")
            return []
        
    def save_users(self, users: List[UserWithPassword]):
        try:
            user_dicts=[]
            for user in users:
                user_dict=user.model_dump() #convert an object to a dictionary
                user_dicts.append(user_dict)
            
            self.data_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.data_file,'w') as f : #write in file
                json.dump(user_dicts, f, indent=2, default=str) #Overwrites the entire file, so everytime we save, we need to dump entire thing

            print(f"Saved{len(users)} users to {self.data_file}")

        except Exception as e:
            print(f"Error saving users:{e}")

#Create a global instance
data_service=DataService()
            

        
        

