## Wine Reviews Data Prep

Prepping a dataset of wine reviews downloaded from [Kaggle](https://www.kaggle.com/zynicide/wine-reviews) for use in a Tableau training. Created by Zack Thoutt, the dataset includes 130,000 wine reviews scraped from WineEnthusiast on November 22, 2017. Each record includes the full-text review, variety (type),  source (country, province, region), points assigned, price, reviewer name, and reviewer Twitter handle.

This code removes duplicates, filters the dataset to a subset of records (reflecting the top 20 varieties by number of reviews), and breaks off the full-text reviews into a separate dataset. Full-text reviews are tokenized with stopwords removed, and summarized by most common words to describe wines in a given variety and from a given country. A smaller dataset displays examples of the full-text reviews, categorized by best (five highest rated wines in a given variety) and worst (five lowest rated wines).

Final CSVs are included in the res/ folder. 

## Workbook

Draft workbook up on [Tableau Public](https://public.tableau.com/profile/patrick.bradshaw#!/vizhome/WineReviews_16012101336830/WineExplorerFinal).

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
