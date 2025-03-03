from core.ai_agent import ai
from core.train import webscrap


def main():
    # promt=input("Enter the promt: ")
    # ai.ai_agent(promt)
    webscrap()
    
    pass
    




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program Terminated")