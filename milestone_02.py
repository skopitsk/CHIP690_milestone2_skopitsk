import pandas as pd
import matplotlib.pyplot as plt

## Load the dataset
df = pd.read_csv(
    "/Users/sarahkopitskie/Desktop/UNC COURSES/CHIP 690/assignments/Export (2).csv"
)

# Q1. How does the crude prevalence of age related muscular degeneration vary across different age groups?

## Filtering the data for prevalance and the correct measurment type
filtered_df = df[
    (df["Question"] == "Prevalence of AMD")
    & (df["Data_Value_Type"] == "Crude Prevalence")
].copy()

## Getting the average crude prevelance for each age group
## Also calculating the standard deviation for error bars in the plot
prevalence_by_age = filtered_df.groupby("Age")["Data_Value"].agg(["mean", "std"])

## ordering the age groups for the plot
age_order = ["40-64 years", "40 years and older", "65-84 years", "85 years and older"]

## Apply the order and drop any missing groups
prevalence_by_age = prevalence_by_age.loc[
    prevalence_by_age.index.intersection(age_order)
].reindex(age_order)
prevalence_by_age = prevalence_by_age.dropna(how="all")

## Calculate the magnitude of the difference
youngest_group_name = prevalence_by_age.index[0]
oldest_group_name = prevalence_by_age.index[-1]

oldest_group_mean = prevalence_by_age.loc[oldest_group_name, "mean"]
youngest_group_mean = prevalence_by_age.loc[youngest_group_name, "mean"]
prevalence_difference = oldest_group_mean - youngest_group_mean

## Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(
    prevalence_by_age.index,
    prevalence_by_age["mean"],
    yerr=prevalence_by_age["std"],
    capsize=5,
    color="darkred",
)

plt.title("Average Crude Prevalence of AMD by Age Group (2019)")
plt.xlabel("Age Group")
plt.ylabel("Mean Crude Prevalence (%)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

## Save and show the plot
plt.savefig("amd_prevalence_by_age_progression_code_output.png")
plt.show()


# Q2. Which U.S. states show the largest and smallest increases in crude AMD prevalence when comparing adults aged 40-64 to those aged 85 and older?

## Defining the age groups for comparison
YOUNGEST_AGE = "40-64 years"
OLDEST_AGE = "85 years and older"

## Filtering for only the two relevant age groups
comparison_df = filtered_df[filtered_df["Age"].isin([YOUNGEST_AGE, OLDEST_AGE])]

## make State the index and Age groups the columns (used AI for code assistance)
prevalence_pivot = comparison_df.pivot_table(
    index="LocationDesc", columns="Age", values="Data_Value", aggfunc="mean"
)

## Renaming columns and droping states that don't have both age groups reported
prevalence_pivot.columns.name = None
prevalence_pivot = prevalence_pivot.rename(
    columns={YOUNGEST_AGE: "Prevalence_40_64", OLDEST_AGE: "Prevalence_85_plus"}
).dropna(subset=["Prevalence_40_64", "Prevalence_85_plus"])

## Calculating the difference (Increase in Prevalence)
prevalence_pivot["Increase_in_Prevalence"] = (
    prevalence_pivot["Prevalence_85_plus"] - prevalence_pivot["Prevalence_40_64"]
)

## Sorting to find the states with the largest and smallest increases
increase_sorted = prevalence_pivot.sort_values(
    by="Increase_in_Prevalence", ascending=False
)

## Print the results
print("=" * 75)
print("State-Level Increase in Crude AMD Prevalence (40-64 to 85+)")
print("=" * 75)

print("\n--- Top 5 States with the LARGEST Increase (Steepest Progression) ---")
print(
    increase_sorted[
        ["Prevalence_40_64", "Prevalence_85_plus", "Increase_in_Prevalence"]
    ]
    .head()
    .to_string(float_format="%.2f")  ## used AI to create clean table
)

print("\n--- Bottom 5 States with the SMALLEST Increase (Shallowest Progression) ---")
print(
    increase_sorted[
        ["Prevalence_40_64", "Prevalence_85_plus", "Increase_in_Prevalence"]
    ]
    .tail()
    .to_string(float_format="%.2f")
)
