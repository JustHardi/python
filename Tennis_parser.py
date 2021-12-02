import time
import colorama
import csv
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup  # pip install bs4
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

match_css = "event__match event__match--static event__match--twoLine"
calendar_css = ".calendar__direction.calendar__direction--tomorrow"
WAIT = 2
path = "Tennis_output_results_pro.csv"


# Функция для записи данных в CSV
def save_doc(r1, r2, path):
    with open(path, "a") as file:
        writer = csv.writer(file, delimiter=";")  # newLine="",
        """
        csv_file - объект с данными
        delimiter - разделитель
        """
        writer.writerow(
            (
                r1["time"],
                r1["name_home"],
                r1["name_away"],
                " "
                + r2["total_goals"]
                + " - | "
                + r2["total_goals1"]
                + " | "
                + r2["total_goals2"]
                + " | "
                + r2["total_goals3"]
                + " | ",
                "g_o: " + r2["avg_all"] + " g_f: " + r2["g_f"] + " g_s: " + r2["g_s"],
                r1["url"],
            )
        )


def find_matches(html):
    urlcount = 1

    template = "https://www.flashscore.ru/match/{}/#match-summary"
    soup = BeautifulSoup(html, "lxml")  # "html.parser"
    # html = soup.find("div" , id="live-table")
    matches = soup.find_all("div", class_=match_css)
    # print(matches)
    colorama.init()
    results = []
    # try:
    #    banner = driver.find_elements_by_css_selector("div[id=onetrust-button-group]")
    #    banner_click = banner[0].click()
    # except:
    #    print("banner not found")

    time.sleep(0.5)

    for m in matches:
        try:
            time_match = ""
            total_goals = 0  # Сумма очков одной встречи
            total_goals1 = 0  # Сумма очков одной встречи
            total_goals2 = 0  # Сумма очков одной встречи
            total_goals3 = 0  # Сумма очков одной встречи
            total_goals4 = 0  # Сумма очков одной встречи
            total_goals5 = 0  # Сумма очков одной встречи
            goals_player_home4 = 0
            goals_player_home5 = 0
            goals_player_away4 = 0
            goals_player_away5 = 0

            id_match = m["id"].split("_")[-1]  # g_1_ 8hbUk4F4
            url = template.format(id_match)

            if urlcount > len(matches) - 1:  # len(matches) - 1
                print("end")
                break

            urlcount += 1
            time_match = m.find(class_="event__time")
            time_match = time_match.text.strip()
            name_match_home = m.find_all("div", class_="event__participant")
            name_match_away = name_match_home[1].text.strip()
            name_match_home = name_match_home[0].text.strip()

            try:
                event_stage_block = m.find_all("div", class_="event__stage--block")
            except:
                print("event_stage_block failed")

            if len(event_stage_block) == 0:
                # //////////////////////////////////////////////////////////////////
                print(
                    Fore.YELLOW
                    + "  ------- "
                    + time_match
                    + " - Время начала матча. -------"
                )
                # driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
                # time.sleep(0.5)
                game_score_home = m.find_all("div", class_="event__score")
                game_score_away = game_score_home[1].text
                game_score_home = game_score_home[0].text

                goals_player_home1 = m.find_all("div", class_="event__part--home")
                goals_player_home2 = goals_player_home1[1].text
                goals_player_home3 = goals_player_home1[2].text
                if len(goals_player_home1) > 3:
                    goals_player_home4 = goals_player_home1[3].text
                if len(goals_player_home1) > 4:
                    goals_player_home5 = goals_player_home1[4].text
                goals_player_home1 = goals_player_home1[0].text
                # //////////////////////////////////////////
                goals_player_away1 = m.find_all("div", class_="event__part--away")
                goals_player_away2 = goals_player_away1[1].text
                goals_player_away3 = goals_player_away1[2].text
                if len(goals_player_away1) > 3:
                    goals_player_away4 = goals_player_away1[3].text
                if len(goals_player_away1) > 4:
                    goals_player_away5 = goals_player_away1[4].text
                goals_player_away1 = goals_player_away1[0].text
                # Находим счёт матча
                # //////////////////////////////////////////
                if (len(game_score_home)) != "":
                    print(
                        Fore.CYAN
                        + "{:>20} | {:<1} - {:<2} {:<2} {:<2} ".format(
                            name_match_home,
                            game_score_home,
                            goals_player_home1,
                            goals_player_home2,
                            goals_player_home3,
                        )
                    )
                    print(
                        "{:>20} | {:<1} - {:<2} {:<2} {:<2} ".format(
                            name_match_away,
                            game_score_away,
                            goals_player_away1,
                            goals_player_away2,
                            goals_player_away3,
                        )
                    )
                    sum_goals_of_all_games_by_first_player_och = (
                            int(goals_player_home1)
                            + int(goals_player_home2)
                            + int(goals_player_home3)
                            + int(goals_player_home4)
                            + int(goals_player_home5)
                    )
                    sum_goals_of_all_games_by_second_player_och = (
                            int(goals_player_away1)
                            + int(goals_player_away2)
                            + int(goals_player_away3)
                            + int(goals_player_away4)
                            + int(goals_player_away5)
                    )
                    total_goals = int(game_score_home) + int(game_score_away)
                    total_goals1 = int(goals_player_home1) + int(goals_player_away1)
                    total_goals2 = int(goals_player_home2) + int(goals_player_away2)
                    total_goals3 = int(goals_player_home3) + int(goals_player_away3)
                    total_goals4 = int(goals_player_home4) + int(goals_player_away4)
                    total_goals5 = int(goals_player_home5) + int(goals_player_away5)
                    average_all = (
                            total_goals1
                            + total_goals2
                            + total_goals3
                            + total_goals4
                            + total_goals5
                    )
                else:
                    continue
                print(
                    Fore.MAGENTA
                    + "\t\t      Total_goals: {} - | {} | {} | {} | \n".format(
                        total_goals,
                        total_goals1,
                        total_goals2,
                        total_goals3,
                    )
                )
                # //////////////////////////////////////////////////////////////////////
                results1 = {
                    "time": str(time_match),
                    "name_home": str(name_match_home),
                    "name_away": str(name_match_away),
                    "url": str(url),
                }
                results2 = {
                    "total_goals": str(total_goals),
                    "total_goals1": str(total_goals1),
                    "total_goals2": str(total_goals2),
                    "total_goals3": str(total_goals3),
                    "avg_all": str(average_all),
                    "g_f": str(sum_goals_of_all_games_by_first_player_och),
                    "g_s": str(sum_goals_of_all_games_by_second_player_och),
                }
                save_doc(results1, results2, path)
                print(Style.RESET_ALL)
                print("=======================================================")
        except:  # NoSuchElementException
            print("Failed")
            continue


my_profile = webdriver.FirefoxProfile(
    r"C:\Users\Hardi\AppData\Roaming\Mozilla\Firefox\Profiles\j62wgvhz.default"
)
binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
options = webdriver.FirefoxOptions()
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
)
# set headless mode on True False
options.set_headless(True)
driver = webdriver.Firefox(
    firefox_profile=my_profile, firefox_binary=binary, options=options
)
wait = WebDriverWait(driver, 10)

URL = "https://www.flashscore.ru/table-tennis/others-men/liga-pro/results/"


def get_html(url):
    try:
        driver.get(url)
        time.sleep(3)

        with open("index_selenium_pro.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)


def parse():
    try:
        get_html(URL)
        with open("index_selenium_pro.html", encoding="utf-8") as file:
            src = file.read()

        find_matches(src)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


parse()
