from .downloader import download_lcemp, download_proton

class Launcher:

    def __init__(self):
        print("LCEMP Launcher starting...")

    def start(self):
        print("Launcher started!")
        print("Downloading latest Proton release")
        #download_proton("10-32")
        download_lcemp("1.0.1")


    