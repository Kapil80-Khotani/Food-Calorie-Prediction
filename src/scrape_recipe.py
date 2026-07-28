import os
import re
import json
import time
import pandas as pd
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================================
# CONFIG
# ==========================================================

INPUT_FILE = "master_recipe_urls.csv"
OUTPUT_FILE = "recipes_dataset.csv"
FAILED_FILE = "failed_urls.csv"
PROGRESS_FILE = "recipe_progress.txt"

RESTART_INTERVAL = 100
SAVE_INTERVAL = 10

# ==========================================================
# START CHROME
# ==========================================================

def start_driver():

    options = uc.ChromeOptions()
    options.page_load_strategy = "eager"

    driver = uc.Chrome(
        options=options,
        version_main=150
    )

    driver.set_page_load_timeout(30)

    wait = WebDriverWait(driver, 20)

    return driver, wait

# ==========================================================
# LOAD RECIPE URLS
# ==========================================================

recipe_urls = (
    pd.read_csv(INPUT_FILE)["Recipe_URL"]
    .drop_duplicates()
    .tolist()
)

print("="*70)
print("Total Recipe URLs :", len(recipe_urls))
print("="*70)

# ==========================================================
# RESUME DATASET
# ==========================================================

dataset = []
done_urls = set()

if os.path.exists(OUTPUT_FILE):

    old = pd.read_csv(OUTPUT_FILE)

    dataset = old.to_dict("records")

    if "url" in old.columns:
        done_urls = set(old["url"])

    print("Existing Dataset Found")
    print("Already Scraped :", len(done_urls))

else:

    print("No Existing Dataset Found")

print("="*70)

# ==========================================================
# RESUME INDEX
# ==========================================================

start_index = 0

if os.path.exists(PROGRESS_FILE):

    with open(PROGRESS_FILE, "r") as f:

        start_index = int(f.read().strip())

print("Starting Index :", start_index)

print("="*70)

# ==========================================================
# START DRIVER
# ==========================================================

driver, wait = start_driver()

print("Chrome Started Successfully")

print("="*70)

failed_urls = []

# ==========================================================
# SCRAPING
# ==========================================================

for i in range(start_index, len(recipe_urls)):

    # ---------------------------------------
    # Restart Browser
    # ---------------------------------------

    if i != start_index and i % RESTART_INTERVAL == 0:

        print("\nSaving Dataset...")

        pd.DataFrame(dataset).to_csv(
            OUTPUT_FILE,
            index=False
        )

        with open(PROGRESS_FILE, "w") as f:
            f.write(str(i))

        try:
            driver.quit()
        except:
            pass

        time.sleep(2)

        driver, wait = start_driver()

        print("Chrome Restarted")

    url = recipe_urls[i]

    if url in done_urls:
        continue

    print("\n" + "="*70)
    print(f"{i+1}/{len(recipe_urls)}")
    print(url)

    recipe = None

    try:

        # ---------------------------------------
        # Retry Once
        # ---------------------------------------

        loaded = False

        for attempt in range(2):

            try:

                driver.get(url)

                wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         "//script[@type='application/ld+json']")
                    )
                )

                loaded = True
                break

            except:

                print("Retrying...")

                time.sleep(3)

        if not loaded:

            failed_urls.append(url)
            continue

        scripts = driver.find_elements(
            By.XPATH,
            "//script[@type='application/ld+json']"
        )

        # ---------------------------------------
        # Find Recipe JSON
        # ---------------------------------------

        for script in scripts:

            try:
                data = json.loads(
                    script.get_attribute("innerHTML")
                )

            except:
                continue

            if isinstance(data, dict):
                data = [data]

            for obj in data:

                types = obj.get("@type", [])

                if isinstance(types, str):
                    types = [types]

                if "Recipe" in types:

                    recipe = obj
                    break

            if recipe:
                break

        if recipe is None:

            print("Recipe JSON Not Found")

            failed_urls.append(url)

            continue

        # ---------------------------------------
        # Extract
        # ---------------------------------------

        title = recipe.get("name", "").strip()

        ingredients = recipe.get(
            "recipeIngredient",
            []
        )

        nutrition = recipe.get(
            "nutrition",
            {}
        )

        calories = nutrition.get(
            "calories",
            ""
        )

        match = re.search(r"\d+", str(calories))

        if match:

            calories = int(match.group())

        else:

            print("Calories Missing")

            continue

        dataset.append({

            "url": url,

            "title": title,

            "ingredients": ", ".join(ingredients),

            "calories": calories

        })

        done_urls.add(url)

        print("Title :", title)
        print("Ingredients :", len(ingredients))
        print("Calories :", calories)

        # ---------------------------------------
        # Save Every 10 Recipes
        # ---------------------------------------

        if len(dataset) % SAVE_INTERVAL == 0:

            pd.DataFrame(dataset).to_csv(
                OUTPUT_FILE,
                index=False
            )

            with open(PROGRESS_FILE, "w") as f:
                f.write(str(i))

            print("Auto Saved")

        time.sleep(0.5)

    except Exception as e:

        print("FAILED :", e)

        failed_urls.append(url)

# ==========================================================
# FINAL SAVE
# ==========================================================

try:
    driver.quit()
except:
    pass

pd.DataFrame(dataset).to_csv(
    OUTPUT_FILE,
    index=False
)

pd.DataFrame({
    "url": failed_urls
}).drop_duplicates().to_csv(
    FAILED_FILE,
    index=False
)

if len(done_urls) == len(recipe_urls):

    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

print("\n" + "="*70)
print("SCRAPING FINISHED")
print("Recipes :", len(dataset))
print("Failed :", len(failed_urls))
print("="*70)