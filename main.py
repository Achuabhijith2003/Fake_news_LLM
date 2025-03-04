from core.ai_agent import ai
from core.train import webscrap,get_links


def main():
    choices=input("Select the Options: \n1.Train the data \n")  
    if choices=='1': 
        url=input("Enter the URL include https:// :")
        get_links(url)
    else: 
        print("Invalid")
    
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program Terminated")