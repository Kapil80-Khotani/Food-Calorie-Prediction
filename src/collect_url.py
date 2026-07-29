import json
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----------------------------
# CONFIG
# ----------------------------

CATEGORY_FILE = "allrecipes_categories.csv"
OUTPUT_FILE = "../data/raw/all_urls.csv"

categories = pd.read_csv(CATEGORY_FILE)["Category_URL"].tolist()

# ----------------------------
# Chrome
# ----------------------------

options = uc.ChromeOptions()
options.page_load_strategy = "eager"

driver = uc.Chrome(
    options=options,
    version_main=150
)

wait = WebDriverWait(driver,20)

all_urls = []

for idx, category in enumerate(categories,1):

    print(f"\n[{idx}/{len(categories)}] {category}")

    driver.get(category)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH,"//script[@type='application/ld+json']")
        )
    )

    scripts = driver.find_elements(
        By.XPATH,
        "//script[@type='application/ld+json']"
    )

    found = 0

    for script in scripts:

        try:
            data = json.loads(script.get_attribute("innerHTML"))
        except:
            continue

        if not isinstance(data,list):
            continue

        for obj in data:

            if "itemListElement" not in obj:
                continue

            for item in obj["itemListElement"]:

                url = item.get("url")

                if not url:
                    continue

                if "/gallery/" in url:
                    typ = "gallery"

                elif "/article/" in url:
                    typ = "article"

                else:
                    typ = "recipe"

                all_urls.append({
                    "source_category":category,
                    "url":url,
                    "type":typ
                })

                found += 1

    print("URLs Found:",found)

driver.quit()

df = pd.DataFrame(all_urls)

df = df.drop_duplicates(subset=["url"])

print("\nTotal Unique URLs:",len(df))

print(df["type"].value_counts())

df.to_csv(OUTPUT_FILE,index=False)