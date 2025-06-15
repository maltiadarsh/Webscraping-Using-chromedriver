# **Tender Data Scraper**

This project is a web scraper built with Python, Selenium, and BeautifulSoup. It automatically navigates to the "New Tenders" section of a government tender site, selects "All" tenders, sets the dropdown to display 20 results, and extracts tender details from the first two pages. The data is then saved into a CSV file.

---

## 📌 Features

- Navigates to the New Tenders → All tab
- Extracts top 20 tenders from two pages (20 total)
- Captures important fields:
  - NIT/RFP NO
  - Name of Work / Subwork / Packages
  - Estimated Cost (in ₹)
  - EMD Amount (in ₹)
  - Bid Submission Closing Date & Time
  - Bid Opening Date & Time
- Saves the data into a CSV file with renamed columns for clarity

---

## Setup Environment
```bash
conda create -n prime python=3.11 -y
```
```bash
conda activate prime
```

## 🛠 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```
## run apps
```bash
python main.py
```
