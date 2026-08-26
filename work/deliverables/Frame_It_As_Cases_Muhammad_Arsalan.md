# Frame It as Cases — Muhammad Arsalan

---

## Voice Card

**Straightforward, builder-minded, calm, no buzzwords.**

Short sentences. No "passionate," "results-driven," or "dynamic." Say what I built, what it does, and what I learned. If a line sounds like a generic AI bio, rewrite it the way I'd say it to a friend.

---

## Before / After

| Generic AI version | My edited version |
|---|---|
| "I am a passionate and results-driven AI/ML engineer who leverages cutting-edge technologies to deliver innovative, scalable solutions that drive meaningful impact." | "I build ML systems that solve real problems — face recognition for attendance, prediction models for delivery times, ranking models for search data. I keep it honest: if the number looks too good, I check for leakage before I celebrate." |

---

## Case 1: AI Attendance System

**Face recognition attendance — Python, OpenCV, Streamlit**

[GitHub](https://github.com/24pwai0015-max/ai-attendance-system)

### The problem

University attendance was done by hand — a teacher calling names one by one. It ate class time every day. Worse, proxy attendance was easy: a friend answers for you, and nobody catches it. The system had no way to verify who was actually sitting in the room.

### What I did

I built a face-recognition attendance system as my semester final project. The flow is simple: register each student's face once, then the camera recognizes them and marks attendance daily — no roll call, no name-calling, no proxies. I used Python for the backend, OpenCV for face detection and recognition, and Streamlit so the whole thing runs in a browser with a clean interface. No complicated setup, no desktop install — just open it and it works.

### What came of it

Got an A. The system correctly identified registered students and logged attendance without manual intervention. It solved the two problems it was built for: no more wasted class time on roll calls, and no way to fake attendance with a friend's name.

**Next time:** I'd handle multiple faces in a single frame (a classroom has thirty students, not one), add anti-spoofing so someone can't hold up a printed photo to fool the camera, improve the UI, and deploy it online so it's not just a local demo.

---

## Case 2: Delivery Time Prediction

**Food delivery time prediction — Random Forest, pandas, Streamlit**

[GitHub](https://github.com/24pwai0015-max/delivery-time-prediction)

### The problem

When someone orders food, they want to know when it arrives. The delivery time depends on many things at once — distance, traffic, weather, time of day — and no single rule covers all the combinations. My ML professor assigned this as a project: take real delivery data and predict the time.

### What I did

I used a Kaggle dataset of food delivery records. Cleaned the data and engineered features using pandas and NumPy. Then I tried three models head to head: Linear Regression, XGBoost, and Random Forest Regressor. I compared them on R² to see which one explained the delivery time best. Random Forest won — it handled the messy, non-linear relationships between features better than a straight line could.

I built a Streamlit front end so you can plug in delivery details and get a predicted time back, no command line needed.

### What came of it

Got an A. The Random Forest model gave accurate predictions on the test set, beating both Linear Regression and XGBoost on R². The project taught me the full ML pipeline end to end: data cleaning, feature engineering, model comparison, and putting the result behind a usable interface.

**Next time:** I'd improve the UI and add real-time features — like pulling live traffic or weather data — instead of relying only on static dataset columns.

---

## Case 3: FlyRank ML Internship — Content Refresh Ranking

**Search ranking model — sklearn, DuckDB, pandas**

[GitHub](https://github.com/24pwai0015-max/flyrank-ml-muhammad-arsalan)

### The problem

FlyRank manages content for clients across the web. With 30,000+ pages, no human can manually check which pages are declining in search traffic and need a refresh. A content strategist has limited time each week — they need a ranked list that puts the most urgent pages at the top, not a vague dashboard that says "things are down."

### What I did

I'm working through the ML track of FlyRank's internship, building a ranking model on real (anonymized) search data — 30,000 pages × 44 columns from Google Search Console. I framed the problem as ranking, not classification: the output is a priority score per page, sorted so a strategist can work top-down.

The label is `is_declining_label` (pages where impressions dropped 20%+ over 30 days). I used Precision@50 as the metric — because only the top of the list matters when someone has limited review time. A naive "stalest page first" rule scores 0.500 at Precision@50. A Random Forest with a proper client-holdout split (no client's pages in both train and test) reaches 0.740 — a 3x improvement.

The biggest lesson: a 2-line decision tree that includes `trend_pct` as a feature hits Precision@50 = 1.000 — which sounds amazing until you realize it's just re-deriving the rule that defines the label. That's data leakage, not a real model. Learning to catch that before trusting a number was worth more than any accuracy score.

### What came of it

The internship is ongoing. So far I've completed the ML task framing (ML-03), with the full pipeline — research question, target definition, metric selection, leakage demonstration — committed and reviewed. The work continues through model training, validation, and a capstone.

**What I've learned:** Data leakage can make any model look perfect. Client-holdout splits matter more than random splits. Precision@K is more honest than accuracy when only the top of a ranked list gets acted on. Frame the decision first, model second.

---

## Bio

I build ML systems that work on real data — face recognition for attendance, prediction models for delivery logistics, ranking models for search content. I'm a 4th-semester AI student doing the FlyRank ML internship, and I care more about whether a model is honest than whether the accuracy number is high.

## Contact

Want to talk about AI/ML, robotics, or a research collaboration? Email me or book a call.

---

*Voice card applied throughout. All claims are based on work I actually did. No inflated numbers, no borrowed stories.*
