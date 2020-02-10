'''sanjrj_agent.py
CSE 415, Winter 2020, Assignment 1
Sanjeev Janarthanan
'''

import chatbot

rule_list = [(r"you want to work in (biotech|genomics|computational biology)", 
              ["Tell me more! That's an area of interest for me!"]),
             #The above rule catches user input of the form "I want to work in biotech."
             #There is one response pattern.
             (r"you like math", ["I can apply the subject but am actually quite " +
                               "bad at pure math", "math is alright"]),
            #The above rule catches user input of the form "I like math."
            #There are two response patterns.
             (r"you like (.*) models", ["Interesting! I think many models can be useful"]),
             #The above rule catches user input of the form "I like random forest models."
             #There is one response pattern.
             (r"you (.*) data collection", ["Don't even get me started on collecting data"]),
             #The above rule catches user input of the form "I hate data collection."
             #There is one response pattern.
             (r"you predict (.*)", ["That's neat! There are a lot of interesting medical outcomes"]),
             #The above rule catches user input of the form "I predict medical dosing."
             #There is one response pattern.
             (r"you think (.*) data (.*)", ["It's hard to say!"]),
             #The above rule catches user input of the form "I think voice data is the most useful."
             #There is one response pattern.
             (r"you like (.*) modeling (.*)", ["I like recurrent neural nets, but $1$ is cool"]),
             #The above rule catches user input of the form "I like logistic regression modeling because it's useful."
             #There is one response pattern.
             (r"you are (.*) at (.*) data", ["Data collection is hard"]),
             #The above rule catches user input of the form "I am bad at acquiring data."
             #There is one response pattern.
             (r"you are interested in (.*)", ["Cool! ACMS majors have many interests, including $1$"]),
             #The above rule catches user input of the form "I am interested in data science."
             #There is one response pattern.
             (r"your favorite part of data science is (.*)", ["$1$ isn't great honestly"])]
             #The above rule catches user input of the form "My favorite part of data science is modeling."
             #There is one response pattern.
you_me = {'I':'you', 'me':'you','you':'me','am':'are',
          'mine':'yours','my':'your','yours':'mine','your':'my'}
intro_string = "My name is Mathish. I was programmed by Sanjeev Janarthanan a senior in the ACMS programs at UW. If I'm not performing up to your standards, you can contact him at sanjrj@uw.edu."
                
ACMSAgent = chatbot.chatbot(rule_list, you_me, "Mathish", intro_string)

if __name__=="__main__":
    ACMSAgent.chat()