# Given an appropriate Jira dump as CSV, plot the number of SPs resolved
# per period.
#
# Jira CSV should include only stories you want to plot (ie, don't include
# stories that were “Won't Fix”, or “Invalid”, and don't include epics, and
# must include the "Resolved" and "Custom Field (Story Points)" fields.
#
# The following Jira query should do the right thing:
#
#   project = dm and status = done and issuetype != epic
#
# You could do all this through the REST API, but it's so slow — better to
# download the CSV file and feed it to Python like this.

import argparse
import csv
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument("csvfile", help="CSV data exported from Jira")
parser.add_argument("--output", default="SPs.pdf", help="output file name")
args = parser.parse_args()

totals = {}
with open(args.csvfile, "r") as f:
    reader = csv.DictReader(f)
    for line in reader:
        month = datetime.strptime(
            line["Resolved"], "%d/%b/%y %I:%M %p"
        ).strftime("%Y-%m")
        try:
            points = float(line["Custom field (Story Points)"])
        except ValueError:
            points = 1.0

        if month in totals:
            totals[month] += points
        else:
            totals[month] = points

months = sorted(totals)
points = [totals[month] for month in months]

fig, ax = plt.subplots(1, 1, figsize=(12, 6))
sns.barplot(x=months, y=points, ax=ax, palette="viridis")
xtext = ax.get_xticklabels()
xtext = [x.get_text() for x in xtext]
ax.set_xticklabels(xtext, rotation=90)
ax.set_xlabel("Month")
ax.set_ylabel("Story Points")

plt.tight_layout()
plt.savefig(args.output)
