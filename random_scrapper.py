import praw
import random
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reddit = praw.Reddit(client_id='{replace}',
                     client_secret='{replace}',
                     user_agent='random_scrapper')

time_filter = datetime.utcnow() - timedelta(days=90) #const to only display recent posts
score_filter = 1000 #changable

def get_random_subreddit():
    popular_subreddits = reddit.subreddits.popular(limit=100)

    subreddits= [subreddit.display_name for subreddit in popular_subreddits]

    return random.choice(subreddits)

def get_reddit_posts(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)

    posts_within_time_filter = []

    for post in subreddit.new(limit=100):
        if datetime.utcfromtimestamp(post.created_utc) > time_filter and post.score > score_filter:
            posts_within_time_filter.append(post)
            if len(posts_within_time_filter) >= 1: #amendable if you would like more posts being scrapped
                return posts_within_time_filter
                break
                    
    return posts_within_time_filter

def send_ads_email(title, url, score, upvote, creation, comments, author, subreddit_name, id):
    sender_email = "{replace}"
    sender_password = "{replace}"
    receiver_email = "{replace}"
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = sender_email
    msg['To'] = receiver_email

    creation = datetime.utcfromtimestamp(creation).strftime('%Y-%m-%d %H:%M:%S')
    reddit_post_url = f"https://www.reddit.com/r/{subreddit_name}/comments/{id}/"


    html_msg = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>""" + title + """</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 20px auto; /* Added margin to center the container */
                padding: 20px;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                border: 2px solid #ccc; /* Border added */
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .content {
                padding: 20px;
            }
            .button {
                display: inline-block;
                background-color: #ff0000; /* Red background */
                color: #ffffff !important; /* White text color */
                text-decoration: none;
                padding: 12px 24px;
                border-radius: 6px;
                border: none;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #cc0000; /* Darker shade of red on hover */
            }
            .button a {
                color: #ffffff !important; /* White text color for the anchor element */
                text-decoration: none !important; /* Remove underline */
            }
            h1 {
                font-size: 24px;
                color: #333333;
                margin: 0 0 20px;
            }
            p {
                font-size: 16px;
                color: #666666;
                line-height: 1.6;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>""" + title + """</h1>
            </div>
            <div class="content">
                <p>We think this post might interest you. Check it out!</p>
                <p>Written by """ + author + """ on """ + creation + """</p>
                <p>""" + upvote + """ others liked the post!</p>
                <p>The post has a score of """ + score + """</p>
                <p>""" + comments + """ comments have been made. Join the conversation!</p>
                <p></p>
                <p><a href=""" + reddit_post_url + """ class="button">Read Post</a></p>
            </div>
        </div>
    </body>
    </html>

    """

    msg.attach(MIMEText(html_msg, 'html'))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("EMAIL sent successfully")

while True:
    random_subreddit = get_random_subreddit()
    posts = get_reddit_posts(random_subreddit)

    if posts:
        for post in posts:
            print('---------------------')
            print(post.title)
            print('URL:', post.url)
            print('Score:', post.score)
            print('---------------------')
            send_ads_email(str(post.title), str(post.url), str(post.score), str(post.ups), post.created_utc, str(post.num_comments), str(post.author), str(post.subreddit.display_name), str(post.id))
        break
