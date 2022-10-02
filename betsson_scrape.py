import numpy as np
import time
import fuzzywuzzy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def football_matches(page_url, collect_matches):
    
    options = Options()
    #options.headless = True 
    options.add_argument('window-size=1920x1080') #when headless = True

    driver_path = 'C:/Users/PUL/Downloads/chromedriver_win32/chromedriver'
    
    driver = webdriver.Chrome(driver_path, options=options)
    
    driver.get(page_url)
    
    try:
        # Wait for page to load
        ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-trigger.ng-trigger-pin.obg-event-row.show-more-markets.ng-star-inserted')))
    except TimeoutException:
        print("Loading took too much time!")
    
    # accept cookies
    accept = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
    accept.click()

    while(True):
        try:
            button = driver.find_element_by_class_name('obg-show-more-less-button.ng-star-inserted')
            if "more" in button.text.lower() or "all" in button.text.lower():
                button.click()
                time.sleep(0.5)
            else:
                break
        except:
            break

    # Get two first events. Live/today or today/tomorrow.
    first = driver.find_element_by_xpath('/html/body/obg-app-root/div/obg-m-betting-layout-container/obg-m-sportsbook-layout-container/obg-m-sidenav/mat-sidenav-container/mat-sidenav-content/div/div/ng-scrollbar/div/div/div/div/section/ng-component/obg-m-category-container/obg-m-events-master-detail-tabs-container/obg-m-events-master-detail-container/div/obg-accordion-content[1]')
    second = driver.find_element_by_xpath('/html/body/obg-app-root/div/obg-m-betting-layout-container/obg-m-sportsbook-layout-container/obg-m-sidenav/mat-sidenav-container/mat-sidenav-content/div/div/ng-scrollbar/div/div/div/div/section/ng-component/obg-m-category-container/obg-m-events-master-detail-tabs-container/obg-m-events-master-detail-container/div/obg-accordion-content[2]')

    for day in [first, second]:
        matches = day.find_elements_by_class_name('ng-trigger.ng-trigger-pin.obg-event-row.show-more-markets.ng-star-inserted')
        for match in matches:
            try:    
                full_category_name = match.find_element_by_class_name('obg-event-info-category-label.ng-star-inserted')
                category_name = full_category_name.text.split("/")[1][1:]
                # Get time
                clock = match.find_element_by_class_name('obg-event-info-event-status-container.ng-star-inserted').text

                # Get team names
                teams = match.find_elements_by_class_name('obg-event-info-participant-label.ng-star-inserted')
                team1 = teams[0].text
                team2 = teams[1].text

                # Get odds
                odds = match.find_elements_by_class_name('obg-numeric-change.ng-star-inserted')
                odds1 = odds[0].text
                odds_draw = odds[1].text
                odds2 = odds[2].text
                
                #print(f'Time: {clock}. Odds: {team1}: {odds1},  draw: {odds_draw}, {team2}: {odds2}.')
                collect_matches[0].append(category_name)
                collect_matches[1].append(team1)
                collect_matches[2].append(team2)
                collect_matches[3].append(odds1)
                collect_matches[4].append(odds2)
                collect_matches[5].append(odds_draw)
            except:
                pass
            
    driver.quit()
'''
page_url = 'https://www.betsson.com/en/sportsbook/football'
collect_matches = [[], [], [], [], [], []]
football_matches(page_url, collect_matches)
print(np.array(collect_matches).shape)
print(collect_matches)
'''