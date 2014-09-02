kiva_data
=========

Goal:scrapping kiva data

Phase 1
=========

1. Scraping kiva lender data of the day

**Source: http://api.kivaws.org/v1/lenders/newest.json**

Destination: today_list, basic_info1

Time: every 2 hours

*Code: today_id_update.py*

Data description:
Listings for the 20 lenders who have most recently joined Kiva.
- id
- posted date
- planned expiration date
- loan amount
- purpose 
- sector
- activity 
- partner id
- total funded amount
- borrower count 
- bonus credit eligibility
- country
- longitude and latitude


2. Scraping extra information about the lenders

**source: http://www.kiva.org/lend/{id}**

Destination: basic_info2

Time: everyday 18pm PST 

*Code: basic_info2.py*

Data description:
Extra information from lender's individual page
- id
- gender_m
-	term
-	content related to child flag
-	partner due diligence type
-	partner rating
-	partner time on kiva
-	partner borrowers
-	partner total loans
-	interest charged
-	average cost per borrower
-	profitablity
-	loan per capita income
-	deliquency
-	risk rate 
-	default rate 
-	loss rate


3. Scraping daily fund update

**Source: http://www.kiva.org/lend/{id}**

Destination: daily_update

Time: everyday 18pm PST

*Code: daily_update.py*

Data description:
Daily fund update for each lender
- id
- date
- how much to go

