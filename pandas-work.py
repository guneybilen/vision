import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv("recent-grads.csv")

#print(type(df))

#pd.set_option("display.max.columns", None)
#df.head()


#df.plot(x="Rank", y=["P25th", "Median", "P75th"])
#plt.show()


#plt.plot(df["Rank"], df["P75th"])
#plt.show()

#df.plot(x="Rank", y="P75th")
#plt.show()

#median_column = df["Median"]
#print(type(median_column))
#median_column.plot(kind="hist")
#plt.show()


#top_5 = df.sort_values(by="Median", ascending=False).head()
#top_5.plot(x="Major", y="Median", kind="bar", rot=5, fontsize=4)
#plt.show()


#top_medians = df[df["Median"] > 60000].sort_values("Median")
#top_medians.plot(x="Major", y=["P25th", "Median", "P75th"], kind="bar")
#plt.show()

#df.plot(x="Median", y="Unemployment_rate", kind="scatter")
#plt.show()

cat_totals = df.groupby("Major_category")["Total"].sum().sort_values()
#print(cat_totals)

#cat_totals.plot(kind="barh", fontsize=4)
#plt.show()

"""
small_cat_totals = cat_totals[cat_totals < 100_000]
big_cat_totals = cat_totals[cat_totals > 100_000]
# Adding a new item "Other" with the sum of the small categories
small_sums = pd.Series([small_cat_totals.sum()], index=["Other"])
big_cat_totals = big_cat_totals.append(small_sums)
big_cat_totals.plot(kind="pie", label="")
#plt.show()
"""

df[df["Major_category"] == "Engineering"]["Median"].plot(kind="hist")
plt.show()


