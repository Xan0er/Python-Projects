#Import Packages

import praw
import pandas as pd

#Accessing the reddit API

reddit = praw.Reddit(client_id="", #client id
                     client_secret="",  #My client secret
                     user_agent="", #My useragent name
                     username = "",     #My reddit username
                     password = "")

#Making a list of subreddits to scrape the data from
sub = ['ReverseEngineering']

for s in sub:
    subreddit = reddit.subreddit(s) #Choosing the Subreddit

########################################
#   CREATING DICTIONARY TO STORE THE DATA WHICH WILL BE CONVERTED TO A DATAFRAME
########################################

#   NOTE: ALL THE POST DATA AND COMMENT DATA WILL BE SAVED IN TWO DIFFERENT
#   DATASETS AND LATER CAN BE MAPPED USING IDS OF POSTS/COMMENTS AS WE WILL 
#   BE CAPTURING ALL IDS THAT COME IN OUR WAY

# SCRAPING CAN BE DONE VIA VARIOUS STRATEGIES {HOT,TOP,etc} we will go with keyword strategy i.e using search a keyword
    query = ['Code']

    for item in query:
        post_dict = {
            "title" : [],   #title of the post
            "score" : [],   # score of the post
            "id" : [],      # unique id of the post
            "url" : [],     #url of the post
            "comms_num": [],   #the number of comments on the post
            "created" : [],  #timestamp of the post
            "body" : []         # the descriptionof post
        }
        comments_dict = {
            "comment_id" : [],      #unique comm id
            "comment_parent_id" : [],   # comment parent id
            "comment_body" : [],   # text in comment
            "comment_link_id" : []  #link to the comment
        }
        for submission in subreddit.search(query,sort = "top",limit = 1):
            post_dict["title"].append(submission.title)
            post_dict["score"].append(submission.score)
            post_dict["id"].append(submission.id)
            post_dict["url"].append(submission.url)
            post_dict["comms_num"].append(submission.num_comments)
            post_dict["created"].append(submission.created)
            post_dict["body"].append(submission.selftext)
            
            ##### Acessing comments on the post
            submission.comments.replace_more(limit = 1)
            for comment in submission.comments.list():
                comments_dict["comment_id"].append(comment.id)
                comments_dict["comment_parent_id"].append(comment.parent_id)
                comments_dict["comment_body"].append(comment.body)
                comments_dict["comment_link_id"].append(comment.link_id)
        
        post_comments = pd.DataFrame(comments_dict)

        post_comments.to_csv(s+"_comments_"+ item +"subreddit.csv")
        post_data = pd.DataFrame(post_dict)
        post_data.to_csv(s+"_"+ item +"subreddit.csv")
