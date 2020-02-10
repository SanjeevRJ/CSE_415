'''chatbot.py
This module provides a base class for your chatbot.
The rule format is adopted from the Chat class distributed
as part of NLTK at nltk.org.
S. Tanimoto, Jan. 4, 2020.
'''

import time, re, random

class chatbot:
  def __init__(self, rule_list, you_me_map, name, introduction_string):
    self.log=[]
    self.rule_list = self.compile(rule_list)
    # Set up the phrase replacement mapping:
    self.you_me_map = you_me_map
    ymm_inputs = sorted(you_me_map.keys(), key=len, reverse=True)
    self.ymmpat = re.compile(r"\b({0})\b".format('|'.join(map(re.escape, ymm_inputs))))
    # The replacement mapping is ready for use.
    # Get the chatbot's name:
    self.name = name
    self.introduction_string = introduction_string

  def agentName(self):
    return self.name

  def introduce(self):
    return self.introduction_string
    # BTW subclassing and instantiation are covered in Python as a
    # Second Language -- part of the reading for Assignment 1.

  def chat(self):
    self.start_time = time.time()
    print(self.introduce())
    print("Type to chat with me.")
    print("When you want to quit, type 'bye'.")
    while True:
      input_text = input("-> ")
      if input_text.lower()=='bye':
        print("Thanks for chatting. Goodbye!")
        break
      response = self.respond(input_text)
      print(response)
 
  def compile(self, rule_list):
    '''Replace each string that represents a condition
    by a regular-expression pattern object.'''
    compiled_rules = [(re.compile(condition), responses) for (condition, responses)in rule_list]
    return compiled_rules

  def do_the_you_me_map(self, itext):
    #print("In you_me_map, itext=", itext)
    result = self.ymmpat.sub(lambda m: self.you_me_map[m.group(0)], itext)
    #print("  result = ", result)
    return result

  def respond(self, itext):
    response = ''
    # Make all the you_me_map substitutions.
    itext = self.do_the_you_me_map(itext)
    #print("itext is: ", itext)
    # Now start trying rules until one works.
    for rule in self.rule_list:
      #print("Considering rule: "+str(rule))
      pattern, responses = rule
      #match = re.match(pattern, itext)
      match = pattern.match(itext)
      if match:
        #print("We got a match: ", match)
        response = random.choice(responses)
        # Replace '$1$' by the first matched group, etc.
        for i in range(len(match.groups())+1):
          code='\$'+str(i)+'\$'
          #print("code = ", code)
          try:
            response = re.sub(code, match.group(i), response)
          except: break
        break
    # The following case could come into play if no rule is provided
    # in the rule_list that handles this input text.
    if response=='':    
      response = "I can't really understand '"+itext+"' (sorry)"
    self.log.append(("User", itext))
    self.log.append((self.name, response))
    return response

if __name__=="__main__":
  marys_rules = [
    (r"you like (.*)", ["Why do you like $1$?", "Hey, I like you!"]),
      # The above rule catches user inputs for the form "I like hot sauce."
      # There are two response patterns.

    (r"", ["Please go on", "Do tell..."])
      # This rule catches all other inputs .
      # It also gives two possible responses.
  ]
  # Note that "r" in front of a string means that it is a "raw" string.
  # In a raw string, the backslash character "\" is taken literally
  # instead of being used as an escape character.
  # Also, note that each rule above has a condition-actions format where
  # the condition is a pattern described by a "regular expression",
  # like  "you like (.*)".  To learn about regular expressions, see
  # https://docs.python.org/3/library/re.html.
  you_me = {'I':'you', 'me':'you','you':'me','am':'are',
   'mine':'yours','my':'your','yours':'mine','your':'my'}
  introduction_string = '''Hello! I am Mary-Bot. I am a naive bot who can barely
carry out the simple task of responding to your input.
Please instantiate chatbot with some better rules!'''
  Mary_Bot = chatbot(marys_rules, you_me, "Mary-Bot", introduction_string)
  Mary_Bot.chat()

