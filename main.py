import os, requests, threading
from colorama import Fore, init

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

init(convert=True)

def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class SPB:
    def title(self):
        os.system(f'cls && title [SPB] StrawPoll Botter  ^|  Made by Plasmonix' if os.name == "nt" else "clear")
        print(center(f"""\n\n
███████╗██████╗ ██████╗ 
██╔════╝██╔══██╗██╔══██╗               ~ StrawPoll Botter ~
███████╗██████╔╝██████╔╝     
╚════██║██╔═══╝ ██╔══██╗    github.com/Plasmonix ~ discord.gg/Plasmonix
███████║██║     ██████╔╝ 
╚══════╝╚═╝     ╚═════╝  \n\n
              """).replace('█', Fore.LIGHTBLUE_EX+"█"+Fore.RESET).replace('~', Fore.LIGHTBLUE_EX+"~"+Fore.RESET).replace('-', Fore.LIGHTBLUE_EX+"-"+Fore.RESET))

    def getFormData(self):
        self.url = "https://www.strawpoll.me/" + self.pollId
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        self.page = requests.get (self.url, headers = self.headers).text
        self.ind = self.page.find ("\"field-options-")
        self.checkboxID = self.page [self.ind:]
        self.checkboxID = self.checkboxID [self.checkboxID.find ("value=\"") + len ("value=\""):]
        self.checkboxID = self.checkboxID [:self.checkboxID.find ("\"")]
        self.checkboxID = str (int (self.checkboxID) + self.option - 1)
        
        if (self.page.find (self.checkboxID) == -1):
            print(f' {Fore.LIGHTRED_EX}!{Fore.RESET} Could not find option.')
            quit()

        for _ in range(self.threads): 
            try:
                threading.Thread(target=self.addVotes, args=(self.url, self.checkboxID, self.headers,)).start()
            except Exception as err:
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {err}.')

    def addVotes(self, url, checkboxID, headers):
            self.lock = threading.Lock()
            while True:
                try:
                    self.page = requests.get (url, headers = headers, timeout = 10).text
                    self.secToken1 = self.page [self.page.find ("security-token"):]
                    self.secToken1 = self.secToken1 [self.secToken1.find ("value=\"") + len ("value=\""):]
                    self.secToken1 = self.secToken1 [:self.secToken1.find ("\"")]
                    
                    self.secToken2 = self.page [self.page.find ("field-authenticity-token"):]
                    self.secToken2 = self.secToken2 [self.secToken2.find ("name=\"") + len ("name=\""):]
                    self.secToken2 = self.secToken2 [:self.secToken2.find ("\"")]
                   
                    self.fieldName = self.page [self.page.find ("\"field-options-"):]
                    self.fieldName = self.fieldName [self.fieldName.find ("name=\"") + len ("name=\""):]
                    self.fieldName = self.fieldName [:self.fieldName.find ("\"")]
                    
                    self.page = requests.post (url, data = {"security-token": self.secToken1, self.secToken2: "", self.fieldName: checkboxID}, headers = self.headers, timeout = 10).text
                    self.successString = "\"success\":\"success\""
                    
                    if (self.page.find (self.successString) != -1):
                        self.lock.acquire()
                        print(f' {Fore.LIGHTGREEN_EX}+{Fore.RESET} Vote Successful {self.secToken1}')
                        self.lock.release()
                    
                    else:
                        self.lock.acquire()
                        print(f' {Fore.LIGHTRED_EX}!{Fore.RESET} Vote Unsuccessful {self.secToken1}')
                        self.lock.release()
                
                except requests.exceptions.RequestException:
                    self.lock.acquire()
                    print(f' {Fore.LIGHTRED_EX}!{Fore.RESET} Ratelimit {self.secToken1}')
                    self.lock.release()
        
    def main(self):
        self.title()
        try:
            self.pollId = input(f'\n {Fore.LIGHTBLUE_EX}>{Fore.RESET} Poll ID: ')
            if self.pollId == '':
                print(f' {Fore.LIGHTRED_EX}!{Fore.RESET} Poll ID is required.')
                os.system('pause >nul')
                quit()
            
            self.option = int(input(f' {Fore.LIGHTBLUE_EX}>{Fore.RESET} Option: '))
            if self.option == '':
                print(f' {Fore.LIGHTRED_EX}!{Fore.RESET} Poll Option is required.')
                os.system('pause >nul')
                quit()
            
            self.threads = int(input(f' {Fore.LIGHTBLUE_EX}>{Fore.RESET} Threads: '))            
            self.title()
            self.getFormData()

        except ValueError:
             print(f'{Fore.LIGHTRED_EX}!{Fore.RESET} Value must be an integer.')
             os.system('pause >nul')
             quit()

if __name__ == '__main__':
    n = SPB()
    n.main()
