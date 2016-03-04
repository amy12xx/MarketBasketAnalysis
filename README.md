# MarketBasketAnalysis

Market Basket Analysis is a modelling technique based upon the theory that if you buy a certain group of items, you are more (or less) likely to buy another group of items.
The set of items a customer buys is referred to as an itemset, and market basket analysis seeks to find relationships between purchases.

Apriori is a classic algorithm that is used for market basket analysis in finding association rules. Apriori is designed to operate on data containing transactions (for example, collections of items bought by customers, or details of a website frequentation).

Support of a rule: % of transactions for which the rule/pattern is true.
Support (A, B) = (No. of transactions containing both A and B) / Total no. of transactions.

Confidence of a rule: The measure of certainty or trustworthiness associated with each discovered rule/pattern.
Confidence (A -> B) = (No. of transactions containing both A and B) / No. of transactions containing A

Dataset contains transactions of grocery items purchased by customers. Dataset contains about 10,000 transactions.
