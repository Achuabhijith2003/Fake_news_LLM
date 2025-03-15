# from core.ai_agent import ai
from core.train import get_links
from DB.db import get_data


def main():
    choices=input("Select the Options: \n1.Train the data \n")  
    if choices=='1': 
        url=input("Enter the URL without https:// or http://:")
        get_links(url)
    elif choices=='2':
        get_data("This is a query document about hawaii")
    else: 
        print("Invalid")
    
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program Terminated")