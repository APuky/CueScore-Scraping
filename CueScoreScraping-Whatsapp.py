#Getting data from matches using urls and match number, and sending periodical updates to Whatsapp
#This was made for the IRONMAN tournament which has races to 30 and where matches can take up to 6 hours.
#It's good to see the swings in a match this long and to see the data in the end without having to watch a livestream or keep track of the data yourself.


import requests
from bs4 import BeautifulSoup
import time
import traceback

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##THINGS TO CHANGE##
########################################################################################
URL_cuescore = "LINK TO TOURNAMENT CUESCORE PAGE"
matchno = "MATCH NUMBER"
race_to = "RACE TO AS AN INTEGER EXAMPLE: 4"
contact = "GROUP NAME OR NUMBER ON WHATSAPP"
########################################################################################

lastA = 0
lastB = 0

playerA_streak = 0
playerB_streak = 0

playerA_streaks = []
playerB_streaks = []

playerA_streak_start = ''
playerB_streak_start = ''

largest_lead_A = [0, '']
largest_lead_B = [0, '']

leads_A = 0
leads_B = 0

message_counter = 0
first_frame = True
hill = False

def sendMessage(message, select_input):
    print(message)
    for x in list(message):
        select_input.send_keys(x)
    time.sleep(1)
    select_input.send_keys(Keys.ENTER)
    time.sleep(5)


def getWhatsAppBrowser(message, *args):
    options = Options()
    ##THINGS TO CHANGE##
    ###############################################################################
    options.binary_location = r'PATH\TO\BROWSER BINARY' ##EXAMPLE: r'C:\Program Files\Mozilla Firefox\firefox.exe'
    fp = webdriver.FirefoxProfile(r'PATH\TO\BROWSER PROFILE') ##EXAMPLE: r'C:\Users\User\AppData\Roaming\Mozilla\Firefox\Profiles\z5fvolnv.default-release'
    driver = webdriver.Firefox(fp, options=options, executable_path=r'PATH\TO\BROWSER DRIVER') ##EXAMPLE: r'C:\Users\User\Desktop\geckodriver.exe'
    ##https://github.com/mozilla/geckodriver/releases
    ###############################################################################
    ## You can use whichever browser you'd like as long as there is a driver that selenium can use. This example is set up for Firefox.
    ## The PROFILE PATH is needed so that you don't have to manually scan the WhatsApp Web QR code to login everytime a message needs to be sent.
    ## This further means that you need to manually login into WhatsApp with firefox before you run this code, otherwise it will NOT WORK.
    ## Your phone has to be connected to the internet during the execution of this code as WhatsApp on desktop will NOT WORK if your phone cannot be reached.
    
    ## Even with all these steps, there is a chance that WhatsApp will not send/receive or be able to display the messages sent by the code.
    
    driver.get("https://web.whatsapp.com/")
    driver.implicitly_wait(10)

    select_contact = driver.find_element(By.CSS_SELECTOR, "[data-testid='chat-list-search']")
    select_contact.click()
    
    for x in contact:
        select_contact.send_keys(x)
    time.sleep(1)
    select_contact.send_keys(Keys.ENTER)
    time.sleep(3)

    driver.implicitly_wait(5)

    select_input = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")))
    select_input.click()
    select_input.clear()
    
    sendMessage(message, select_input)
    
    if not args:
        driver.close()
    else:
        if largest_lead_A[0] == 0:
            sendMessage(f'{playerA} was never in the lead :(', select_input)

            sendMessage(f'{playerB} largest lead: {largest_lead_B[0]}, {largest_lead_B[1]}', select_input)
            
            sendMessage(f'{playerA} longest streak: {longest_streak_A[0]}, {longest_streak_A[1]} --> {longest_streak_A[2]}', select_input)

            sendMessage(f'{playerB} longest streak: {longest_streak_B[0]}, {longest_streak_B[1]} --> {longest_streak_B[2]}', select_input)
            
        elif largest_lead_B[0] == 0:
            sendMessage(f'{playerB} was never in the lead :(', select_input)
            
            sendMessage(f'{playerA} largest lead: {largest_lead_A[0]}, {largest_lead_A[1]}', select_input)
            
            sendMessage(f'{playerA} longest streak: {longest_streak_A[0]}, {longest_streak_A[1]} --> {longest_streak_A[2]}', select_input)
            
            sendMessage(f'{playerB} longest streak: {longest_streak_B[0]}, {longest_streak_B[1]} --> {longest_streak_B[2]}', select_input)
            
        else:
            
            sendMessage(f'{playerA} took the lead {leads_A} times.', select_input)
            
            sendMessage(f'{playerA} largest lead: {largest_lead_A[0]}, {largest_lead_A[1]}.', select_input)
            
            sendMessage(f'{playerB} took the lead {leads_B} times.', select_input)
            
            sendMessage(f'{playerB} largest lead: {largest_lead_B[0]}, {largest_lead_B[1]}', select_input)
            
            sendMessage(f'{playerA} longest streak: {longest_streak_A[0]}, {longest_streak_A[1]} --> {longest_streak_A[2]}', select_input)
            
            sendMessage(f'{playerB} longest streak: {longest_streak_B[0]}, {longest_streak_B[1]} --> {longest_streak_B[2]}', select_input)
            
            driver.close()
        


while True:
    try:
        r = requests.get(URL_cuescore)
        soup = BeautifulSoup(r.content, 'html5lib')
        
        match = soup.find('tr', attrs={'data-matchno':str(matchno)})
    
        playerA = match.find('td', attrs={'class':'playerA'})['title'].strip()
        scoreA = int(match.find('td', attrs={'class':'scoreA'}).div.input['value'])
    
        playerB = match.find('td', attrs={'class':'playerB'})['title'].strip()
        scoreB = int(match.find('td', attrs={'class':'scoreB'}).div.input['value'])
    
        if (scoreA == 29 or scoreB==29) and not hill:
            
            getWhatsAppBrowser(f'Hill! {scoreA} : {scoreB}')
            hill = True
            
            
        #### Save current streak if changed
        if scoreA > lastA:
            if playerA_streak_start == '':
                playerA_streak_start = f'{playerA} {lastA} : {scoreB} {playerB}'
                
            playerA_streak += 1
            
            if first_frame:
                
                getWhatsAppBrowser(f'The match has started! {playerA} is first on the boards! {scoreA} : {scoreB}')
                
                first_frame = False
            
            #End other players streak and save streak, start and end
            if playerB_streak > 0:
                end_of_streak_B = f'{playerA} {lastA} : {scoreB} {playerB}'
                streak_B = int(end_of_streak_B.split(':')[1].strip().split(' ')[0]) - int(playerB_streak_start.split(':')[1].strip().split(' ')[0])
                temp_list = [streak_B, playerB_streak_start, end_of_streak_B]
                playerB_streaks.append(temp_list)
                
                playerB_streak_start = ''
                playerB_streak = 0
                
            #### If change in the lead, send message
            if scoreA == (scoreB+1):
                leads_A += 1
                
                getWhatsAppBrowser(f'{playerA} takes the lead! {scoreA} : {scoreB}')
                message_counter = 0
            message_counter += 1
    
            
        
        if scoreB > lastB:
            if playerB_streak_start == '':
                playerB_streak_start = f'{playerA} {scoreA} : {lastB} {playerB}'
                
            playerB_streak += 1
            
            if first_frame:
                getWhatsAppBrowser(f'The match has started! {playerB} is first on the boards! {scoreA} : {scoreB}')
                
                first_frame = False
            
            # End other players streak and save streak, start and end
            if playerA_streak > 0:
                end_of_streak_A = f'{playerA} {scoreA} : {lastB} {playerB}'
                streak_A = int(end_of_streak_A.split(':')[0].strip().split(' ')[2]) - int(playerA_streak_start.split(':')[0].strip().split(' ')[2])
                temp_list = [streak_A, playerA_streak_start, end_of_streak_A]
                playerA_streaks.append(temp_list)
                
                playerA_streak_start = ''
                playerA_streak = 0
        
            #### If change in the lead, send message
            if scoreB == (scoreA+1):
                leads_B += 1
                
                getWhatsAppBrowser(f'{playerB} takes the lead! {scoreA} : {scoreB}')
                message_counter = 0
            message_counter += 1
        
        #### If no lead changes, send message after every n(message_counter) frames
        if message_counter == 5:
            
            getWhatsAppBrowser(f'{playerA} {scoreA} : {scoreB} {playerB}') 
            message_counter = 0
            
        lastA = scoreA
        lastB = scoreB
        
        if lastA-lastB > largest_lead_A[0]:
            largest_lead_A = [lastA-lastB, f'{playerA} {scoreA} : {scoreB} {playerB}']
        
        if lastB-lastA > largest_lead_B[0]:
            largest_lead_B = [lastB-lastA, f'{playerA} {scoreA} : {scoreB} {playerB}']
            
            
        
        #### END OF MATCH - STATISTICS
        if scoreA == race_to or scoreB == race_to:
            if scoreA == race_to:
                end_of_streak_A = f'{playerA} {scoreA} : {scoreB} {playerB}'
                temp_list = [playerA_streak, playerA_streak_start, end_of_streak_A]
                playerA_streaks.append(temp_list)
                playerA_streak_start = ''
                playerA_streak = 0
                
            elif scoreB ==race_to:
                end_of_streak_B = f'{playerA} {scoreA} : {scoreB} {playerB}'
                temp_list = [playerB_streak, playerB_streak_start, end_of_streak_B]
                playerB_streaks.append(temp_list)
                playerB_streak_start = ''
                playerB_streak = 0
            
            highestA = 0
            indexA = 0
            for streak in playerA_streaks:
                if streak[0] > highestA:
                    highestA = streak[0]
                    indexA = playerA_streaks.index(streak)
            highestB = 0
            indexB = 0
            for streak in playerB_streaks:
                if streak[0] > highestB:
                    highestB = streak[0]
                    indexB = playerB_streaks.index(streak)        
            
            longest_streak_A = playerA_streaks[indexA]
            longest_streak_B = playerB_streaks[indexB]
            
            getWhatsAppBrowser(f'END OF MATCH: {playerA} {scoreA} : {scoreB} {playerB}', "end")
            
                
            
            break
        print(f'Working fine at score {scoreA} : {scoreB}')
        time.sleep(20)
    except Exception:       
        getWhatsAppBrowser(traceback.format_exc())
        break



