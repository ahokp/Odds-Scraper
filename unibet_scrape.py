import numpy as np
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def football_matches(page_url, collect_matches):
    
    options = Options()
    options.headless = True
    options.add_argument('window-size=1920x1080') #when headless = True

    driver_path = 'C:/Users/PUL/Downloads/chromedriver_win32/chromedriver'
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get(page_url)

    current_categories = []

    try:
        # Wait for page to load
        ele = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, '_5f930')))
    except TimeoutException:
        print("Loading took too much time!")
    
    # accept cookies
    accept = driver.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
    accept.click()

    # Open different categories
    categories = driver.find_elements_by_class_name('_5f930')
    for category in categories:

        category_name = category.find_element_by_class_name('_4ec65').text
        # Skip category if already gone through it
        if category_name in current_categories:
            continue
        #print(f'Category: {category_name.text}')
        current_categories.append(category_name)
        
        lvl = category.find_elements_by_xpath(".//div[@data-test-name = 'accordionLevel1']")
        day = category
        # Only check main categories, skip if not main category
        if len(lvl) == 0:
            continue
        
        # Click category if not opened already
        cat_matches = category.find_elements_by_class_name('_20e33')
        if len(cat_matches) == 0:
            category.click()
        
        # Open possible sub-categories
        sub_cats = category.find_elements_by_class_name('_5f930')
        for sub_cat in sub_cats:
            try:
                sub_cat_matches = sub_cat.find_elements_by_class_name('_20e33')
                if len(sub_cat_matches) == 0:
                    sub_cat.click()
            except:
                pass

        days = category.find_elements_by_class_name('_28843')
        for day in days:
            d = day.find_element_by_class_name('_6043e')
            # Skip, if match is not today
            if d.text != 'Today':
                continue

            # Get matches
            matches = day.find_elements_by_class_name('_20e33')
            for match in matches:
                try:
                    # Get time
                    clock = match.find_element_by_class_name('a7fc8').text

                    # Get team names
                    teams = match.find_elements_by_class_name('_6548b')
                    team1 = teams[0].text
                    team2 = teams[1].text

                    # Get odds
                    odds = match.find_elements_by_class_name('_3373b')
                    odds1 = ''
                    odds_draw = ''
                    odds2 = ''
                    # Draw option
                    if len(odds) == 5:
                        odds1 = odds[0].text
                        odds_draw = odds[1].text
                        odds2 = odds[2].text
                    # No draw option
                    elif len(odds) == 4:
                        odds1 = odds[0].text
                        odds_draw = '1'
                        odds2 = odds[1].text
                    
                    # Get score if it exists
                    score = match.find_elements_by_class_name('_026a0')
                    live = ''
                    if len(score) != 0:
                        live = 'Live! '

                    #print(f'{live}Time: {clock}. Odds: {team1}: {odds1},  draw: {odds_draw}, {team2}: {odds2}.')
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
page_url = 'https://www.unibet.com/betting/sports/filter/football/all/matches'
collect_matches = [[], [], [], [], [], []]
football_matches(page_url, collect_matches)
print(np.array(collect_matches).shape)
'''