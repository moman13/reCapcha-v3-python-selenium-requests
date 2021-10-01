from seleniumwire import webdriver
from time import sleep
import requests


class Main:
    __pluginUrl = "https://chrome.google.com/webstore/detail/browsec-vpn-free-vpn-for/omghfjlpggmjjaagoclmmobgdodcjboh"
    __userApiKey = "e074efc8a829d7369bad7fff8256ae9b"
    __siteKey = "6Le48QAaAAAAAId_ao_tJuFtMhPEoRr8h3BmlS7H&amp"
    __websiteUrl = "https://www.olx.ua/account/?ref%5B0%5D%5Baction%5D=myaccount&ref%5B0%5D%5Bmethod%5D=index"
    __recapchaToken = "CAPCHA_NOT_READY"
    __action = "register"
    __recapchaId = ""
    __itterationNumber = 1
    __displayAllProcess = True
    __showBrowserWindow = True
    __userData = [["soguny@ryteto.me", "Sony76gu"], ["kyliqyle@musiccode.me", "Qube3Dua"], ["mupivyqe@musiccode.me", "MyMusic80th"], ["jinuroku@musiccode.me", "jino333Z"]]
    __numberOfAccounts = 4
    __numberOfSuccess = 0
    __currentUrl = ""

    def __openWebsite(self, driver):
        try:
            driver.get(self.__websiteUrl)
            if (self.__displayAllProcess):
                print("website was opened")
        except Exception as ex:
            print(ex)


    def __takeRecapchaId(self):
        self.__recapchaId = requests.get(f"http://rucaptcha.com/in.php?key={self.__userApiKey}&method=userrecaptcha&version=v3&min_score=0.9&pageurl=\
                      {self.__websiteUrl}&googlekey={self.__siteKey}action={self.__action}").text
        self.__recapchaId = self.__recapchaId[ 3 : len(self.__recapchaId) ]
        if (self.__displayAllProcess):
            print("recapcha id was taken")


    def __takeRecapchaToken(self):

        while (self.__recapchaToken == "CAPCHA_NOT_READY"):

            self.__recapchaToken = requests.get(f"http://rucaptcha.com/res.php?key={self.__userApiKey}&action=get&id={self.__recapchaId}").text

            self.__recapchaToken = self.__recapchaToken[ 3 : len(self.__recapchaToken) ]
            if (self.__displayAllProcess):
                print("recapcha token was taken")

    def __sendToken(self, driver):
        try:
            __elementForSendToken = driver.find_element_by_id("g-recaptcha-response")
            driver.execute_script(f"arguments[0].innerHTML = '{self.__recapchaToken}';", __elementForSendToken)
            if (self.__displayAllProcess):
                print("token was sent")
        except Exception as ex:
            print(ex)

    def __sendRequests(self):
        requests.post("https://www.olx.ua/account/?ref%5B0%5D%5Baction%5D=myaccount&ref%5B0%5D%5Bmethod%5D=index#login",\
                      data = {"friction-token": self.__recapchaToken})
        if (self.__displayAllProcess):
            print("requests were sent")

    def __getUserLogin(self):
        if (self.__displayAllProcess):
            print("userlogin was taken")
        return self.__userData[self.__numberOfSuccess][0]

    def __getUserPass(self):
        if (self.__displayAllProcess):
            print("userpass was taken")
        return self.__userData[ self.__numberOfSuccess ][ 1 ]


    def __sendGoodRequest(self):
        requests.get(f"http://rucaptcha.com/res.php?key={self.__userApiKey}8&action=reportgood&id={self.__recapchaId}")


    def __sendBadRequest(self):
        requests.get(f"http://rucaptcha.com/res.php?key={self.__userApiKey}&action=reportbad&id={self.__recapchaId}")
    # функция которая осуществляет ввод логин пароля и клик по кнопке
    def __sendUserData(self, driver, userlogin, userpass):
        try:
            driver.find_element_by_id("userEmail").send_keys(f"{userlogin}")
            driver.find_element_by_id("userPass").send_keys(f"{userpass}")
            driver.find_element_by_id("se_userLogin").click()
        except Exception as ex:
            print(ex)
    # функция которая осуществляет вход на сайт
    def __userLogin(self, driver, userlogin, userpass):
        try:
            self.__openWebsite(driver)
            sleep(10)
            self.__takeRecapchaId()
            self.__takeRecapchaToken()
            sleep(5)
            self.__sendToken(driver)
            self.__sendRequests()
            self.__sendUserData(driver, userlogin, userpass)
            sleep(10)
            self.__currentUrl = driver.current_url
            # если вошел в аккаунт
            if (self.__currentUrl != self.__websiteUrl):
                self.__sendGoodRequest()
                print("Good request was sent")
                return True
            # если не вошел в аккаунт:
            self.__sendBadRequest()
            print("Bad request was sent")
            return False
        except Exception as ex:
            print(ex)

    def main(self):
        __driver = webdriver.Chrome(executable_path="chromedriver.exe")


        for i in range(self.__numberOfAccounts):
            # если False то не получилось войти, если True то получилось войти по умолчанию False что означает что вход еще не был выполнен
            __tryToLogin = False
            # пока не вошел
            while (not __tryToLogin):
                __currentLogin = self.__getUserLogin()
                __currentPass = self.__getUserPass()
                __tryToLogin = self.__userLogin(__driver, __currentLogin, __currentPass)
                # если получилось войти
                if (__tryToLogin):
                    self.__numberOfSuccess += 1
                    print(f"Logged into account: {__currentLogin}")
                    print(f"{self.__itterationNumber} itteration has been end")
                    print("--------------------------------------------------")
                else:
                    print("Bad token was taken")
                    print(f"{self.__itterationNumber} itteration has been end")
                    print("--------------------------------------------------")
                self.__itterationNumber += 1
        __driver.close()
        __driver.quit()

if __name__ == "__main__":
    print("start program")
    main = Main()
    main.main()
    print("program end")
