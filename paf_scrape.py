import numpy as np
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def football_matches(page_url, collect_matches):
    day_name_today = datetime.datetime.now().strftime('%A')
    current_categories = []

    options = Options()
    #options.headless = True
    options.add_argument('window-size=1920x1080')

    driver_path = 'C:/Users/PUL/Downloads/chromedriver_win32/chromedriver'
    
    driver = webdriver.Chrome(driver_path, options=options)
    
    driver.get(page_url)
    
    try:
        # Wait for page to load
        ele = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modal-portal"]/div/aside/div/div/button[1]')))
    except TimeoutException:
        print("Loading took too much time!")
    
    # accept cookies
    accept = driver.find_element_by_xpath('//*[@id="modal-portal"]/div/aside/div/div/button[1]')
    accept.click()
    time.sleep(3)

    # Switch to iframe
    iframe = driver.find_element_by_xpath('//*[@id="__next"]/main/div/iframe')
    driver.switch_to.frame(iframe)
    
    # Open different categories
    categories = driver.find_elements_by_class_name('CollapsibleContainer__CollapsibleWrapper-sc-1bmcohu-0.fkFtEG.KambiBC-betty-collapsible.KambiBC-collapsible-container.KambiBC-mod-event-group-container')
    for i, category in enumerate(categories):

        category_name = category.find_element_by_class_name('CollapsibleContainer__Title-sc-1bmcohu-7').text
        # Skip category if already gone through it
        if category_name in current_categories:
            continue
        current_categories.append(category_name)
        #print(f'Category: {category_name}')

        # Click category if not opened already
        cat_matches = category.find_elements_by_class_name('KambiBC-event-item__link')
        if len(cat_matches) == 0:
            try:
                category.click()
                time.sleep(0.5)
            except:
                pass

        # First category is live, skip it
        if i != 0:
            # Open league if not opened already
            leagues = category.find_elements_by_class_name('KambiBC-betoffer-labels.KambiBC-betoffer-labels--with-title')
            for league in leagues:
                l = league.find_elements_by_class_name('CollapsibleContainer__RightComponentSlot-sc-1bmcohu-11.iOtder')
                try:
                    if len(l) == 0:
                        league.click()
                        time.sleep(0.5)
                except:
                    pass
        
        # Get matches
        matches = category.find_elements_by_class_name('KambiBC-event-item__event-wrapper')
        for match in matches:
            try:  
                
                # Get time
                clock = match.find_element_by_class_name('KambiBC-event-item__match-clock-container').text
                c = clock.split('\n')
                t = c[0]
                if len(c) > 1:
                    t = c[1]
                    day = c[0]
                    # Skip if match not today
                    if day != day_name_today[:3]:
                        continue

                # Get team names
                teams = match.find_elements_by_class_name('KambiBC-event-participants__name')
                team1 = teams[0].text
                team2 = teams[1].text
                
                # Get odds
                odds = match.find_elements_by_class_name('OutcomeButton__Odds-sc-1anyy32-5.hLbRHz')
                odds1 = odds[0].text
                odds_draw = odds[1].text
                odds2 = odds[2].text
                
                # Get score if it exists
                score = match.find_elements_by_class_name('KambiBC-event-result__points')
                live = ''
                if len(score) != 0:
                    live = 'Live! '

                #print(f'{live}Time: {t}. Odds: {team1}: {odds1},  draw: {odds_draw}, {team2}: {odds2}.')
                collect_matches[0].append(category_name)
                collect_matches[1].append(team1)
                collect_matches[2].append(team2)
                collect_matches[3].append(odds1)
                collect_matches[4].append(odds2)
                collect_matches[5].append(odds_draw)

            except IndexError:
                print("List index out of range")
            
    driver.quit()
'''
page_url = 'https://www.paf.com/en/betting#/filter/football/all/all/all/matches'
collect_matches = [[], [], [], [], [], []]
football_matches(page_url, collect_matches)
print(collect_matches)
'''
