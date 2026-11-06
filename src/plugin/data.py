"""Six synthetic filing excerpts (fictional companies) and their answer key.

The values were chosen first and the text rendered from them, so the key does not depend on any parser.
"""

import json

FILINGS = json.loads(r'''{
 "f1": {
  "form": "10-K",
  "text": "Northwind Cartography Inc.\nFORM 10-K (excerpt)\nFor the fiscal year ended December 31, 2025\n\nCONSOLIDATED STATEMENTS OF OPERATIONS (in thousands, except per share data)\n                                        Fiscal 2025      Fiscal 2024\nTotal revenues                            4,218,330        3,766,005\nCost of revenues                          2,530,998        2,259,603\nNet income (loss)                           312,480          280,110\n\nCONSOLIDATED BALANCE SHEETS (in thousands)\n                                       Dec 31, 2025     Dec 31, 2024\nCash and equivalents                        987,020          912,077\nTotal assets                              9,870,204        9,120,773\nTotal liabilities                         3,948,081        3,648,309\n\nMANAGEMENT'S DISCUSSION\nRevenue was affected by changes in pricing and volume. Operating expenses were 843,666."
 },
 "f2": {
  "form": "10-K",
  "text": "Lakeside Turbine Holdings\nFORM 10-K (excerpt)\nFor the fiscal year ended December 31, 2025\n\nCONSOLIDATED STATEMENTS OF OPERATIONS (in millions, except per share data)\n                                        Fiscal 2024      Fiscal 2025\nTotal revenues                               16,470           18,452\nCost of revenues                              9,882           11,071\nNet income (loss)                             1,655            1,907\n\nCONSOLIDATED BALANCE SHEETS (in millions)\n                                       Dec 31, 2024     Dec 31, 2025\nCash and equivalents                          3,998            4,133\nTotal assets                                 39,980           41,330\nTotal liabilities                            15,992           16,532\n\nMANAGEMENT'S DISCUSSION\nRevenue was affected by changes in pricing and volume. Operating expenses were 3,690."
 },
 "f3": {
  "form": "10-K",
  "text": "Quill & Anchor Media Corp.\nFORM 10-K (excerpt)\nFor the fiscal year ended December 31, 2025\n\nCONSOLIDATED STATEMENTS OF OPERATIONS (in thousands, except per share data)\n                                        Fiscal 2025      Fiscal 2024\nTotal revenues                              866,240          900,115\nCost of revenues                            519,744          540,069\nNet income (loss)                          (54,307)           12,880\n\nCONSOLIDATED BALANCE SHEETS (in thousands)\n                                       Dec 31, 2025     Dec 31, 2024\nCash and equivalents                        120,499          131,044\nTotal assets                              1,204,990        1,310,445\nTotal liabilities                           481,996          524,178\n\nMANAGEMENT'S DISCUSSION\nRevenue was affected by changes in pricing and volume. Operating expenses were 173,248."
 },
 "f4": {
  "form": "10-K",
  "text": "Tiny Harbor Bakery Ltd.\nFORM 10-K (excerpt)\nFor the fiscal year ended December 31, 2025\n\nCONSOLIDATED STATEMENTS OF OPERATIONS (in dollars, except per share data)\n                                        Fiscal 2025      Fiscal 2024\nTotal revenues                            2,845,190        2,510,770\nCost of revenues                          1,707,114        1,506,462\nNet income (loss)                            96,420           71,050\n\nCONSOLIDATED BALANCE SHEETS (in dollars)\n                                       Dec 31, 2025     Dec 31, 2024\nCash and equivalents                        112,030          100,588\nTotal assets                              1,120,300        1,005,880\nTotal liabilities                           448,120          402,352\n\nMANAGEMENT'S DISCUSSION\nRevenue was affected by changes in pricing and volume. Operating expenses were 569,038."
 },
 "f5": {
  "form": "10-K",
  "text": "Redwood Signal Systems\nFORM 10-K (excerpt)\nFor the fiscal year ended December 31, 2025\n\nCONSOLIDATED STATEMENTS OF OPERATIONS (in millions, except per share data)\n                                        Fiscal 2024      Fiscal 2025\nTotal revenues                                6,905            7,310\nCost of revenues                              4,143            4,386\nNet income (loss)                               388              402\n\nMANAGEMENT'S DISCUSSION\nRevenue was affected by changes in pricing and volume. Operating expenses were 1,462."
 },
 "f6": {
  "form": "10-Q",
  "text": "Cobalt Ridge Logistics\nFORM 10-Q (excerpt)\nFor the quarterly period ended September 30, 2025\n\nCONDENSED STATEMENTS OF OPERATIONS (in thousands)\n                                3M Sep 2025    3M Sep 2024    9M Sep 2025    9M Sep 2024\nTotal revenues                    1,503,220      1,388,940      4,509,667      4,166,825\nNet income (loss)                   (8,915)         61,330       (26,756)        183,993\n\nCONDENSED BALANCE SHEETS (in thousands)\n                               Sep 30, 2025   Dec 31, 2024\nTotal assets                      5,640,110      5,702,385"
 }
}''')

ANSWERS = json.loads(r'''{
 "f1": {
  "revenue_usd": 4218330000,
  "net_income_usd": 312480000,
  "total_assets_usd": 9870204000
 },
 "f2": {
  "revenue_usd": 18452000000,
  "net_income_usd": 1907000000,
  "total_assets_usd": 41330000000
 },
 "f3": {
  "revenue_usd": 866240000,
  "net_income_usd": -54307000,
  "total_assets_usd": 1204990000
 },
 "f4": {
  "revenue_usd": 2845190,
  "net_income_usd": 96420,
  "total_assets_usd": 1120300
 },
 "f5": {
  "revenue_usd": 7310000000,
  "net_income_usd": 402000000,
  "total_assets_usd": null
 },
 "f6": {
  "revenue_usd": 1503220000,
  "net_income_usd": -8915000,
  "total_assets_usd": 5640110000
 }
}''')
