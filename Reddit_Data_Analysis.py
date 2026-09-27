#Reddit Data Analysis using the BRIDGES API

from datetime import datetime
from bridges.data_src_dependent.data_source import reddit_data
import matplotlib.pyplot as plt

#=========================================
# Fetch Data from Reddit
#=========================================

#Get posts from the askscience subreddit
posts = reddit_data("askscience")
print(f"Fetched {len(posts)} posts\n")

#=========================================
# Data Aggregation
#=========================================

#Average score across all posts
scores = [p.score for p in posts]
average_score = sum(scores) / len(scores)
print(f"Average score: {average_score:.2f}")

#Post with the highest and lowest score
#Finds the min and max from the list by score
highest_score = max(posts, key=lambda p: p.score)
lowest_score = min(posts, key=lambda p: p.score)
print(f"Highest score: {highest_score.score}  -  {highest_score.title}")
print(f"Lowest score:  {lowest_score.score}  -  {lowest_score.title}\n")

#Finds the average comment count across all posts
comment_counts = [p.comment_count for p in posts]
average_comments = sum(comment_counts) / len(comment_counts)
print(f"Average comment count: {average_comments:.2f}")

#Post with the most and fewest comments
most_comments = max(posts, key=lambda p: p.comment_count)
fewest_comments = min(posts, key=lambda p: p.comment_count)
print(f"Most comments:   {most_comments.comment_count}  -  {most_comments.title}")
print(f"Fewest comments: {fewest_comments.comment_count}  -  {fewest_comments.title}\n")

#=========================================
# Categorize by Vote Ratio
#=========================================

#Sort every post into one of three lists based on its vote_ratio
high_ratio = [p for p in posts if p.vote_ratio > 0.8]
medium_ratio = [p for p in posts if 0.5 <= p.vote_ratio <= 0.8]
low_ratio = [p for p in posts if p.vote_ratio < 0.5]

print("Vote Ratio Categories")
print("-" * 30)
print(f"High (>0.8):          {len(high_ratio)} posts")
print(f"Medium (0.5-0.8):     {len(medium_ratio)} posts")
print(f"Low (<0.5):           {len(low_ratio)} posts\n")