import os
import time
import pandas as pd
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================================
# CONFIG
# =====================================================

INPUT_FILE = "all_urls.csv"
OUTPUT_FILE = "../data/raw/master_recipe_urls.csv"

SAVE_INTERVAL = 50

# =====================================================
# LOAD EXISTING DATA
# =====================================================

df = pd.read_csv(INPUT_FILE)

recipe_urls = set(df[df["type"] == "recipe"]["url"])

extra_pages = df[df["type"] != "recipe"]["url"].tolist()

print("Initial Recipes :", len(recipe_urls))
print("Pages To Visit :", len(extra_pages))

# =====================================================
# RESUME SUPPORT
# =====================================================

start_index = 0

if os.path.exists("page_progress.txt"):
    with open("page_progress.txt") as f:
        start_index = int(f.read().strip())

print("Starting From :", start_index)

# =====================================================
# DRIVER
# =====================================================

options = uc.ChromeOptions()
options.page_load_strategy = "eager"


def start_driver():
    driver = uc.Chrome(
        options=options,
        version_main=150
    )
    driver.set_page_load_timeout(30)
    wait = WebDriverWait(driver, 20)
    return driver, wait


driver, wait = start_driver()

# =====================================================
# SCRAPE
# =====================================================

for i in range(start_index, len(extra_pages)):

    # restart every 50 pages
    if i != start_index and i % SAVE_INTERVAL == 0:

        print("\nSaving...")

        pd.DataFrame(
            {"Recipe_URL": sorted(recipe_urls)}
        ).to_csv(
            OUTPUT_FILE,
            index=False
        )

        with open("page_progress.txt", "w") as f:
            f.write(str(i))

        driver.quit()

        time.sleep(2)

        driver, wait = start_driver()

    url = extra_pages[i]

    print(f"\n{i+1}/{len(extra_pages)}")
    print(url)

    try:

        driver.get(url)

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        links = driver.find_elements(By.TAG_NAME, "a")

        new_found = 0

        for a in links:

            href = a.get_attribute("href")

            if not href:
                continue

            # recipe formats
            if (
                "/recipe/" in href
                or "-recipe-" in href
            ):

                if href not in recipe_urls:
                    recipe_urls.add(href)
                    new_found += 1

        print("New Recipes :", new_found)

    except Exception as e:

        print("Skipped :", e)

# =====================================================
# SAVE
# =====================================================

driver.quit()

pd.DataFrame(
    {"Recipe_URL": sorted(recipe_urls)}
).to_csv(
    OUTPUT_FILE,
    index=False
)

if os.path.exists("page_progress.txt"):
    os.remove("page_progress.txt")

print("\nFinished")
print("Total Recipes :", len(recipe_urls))