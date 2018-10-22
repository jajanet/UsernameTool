from bs4 import BeautifulSoup
import requests
from valid import Valid

class Suggest():
  '''
  keep track of possible choices and likes
  '''
  def __init__(self, checks, current_user = ""):
    self.checks = checks # primarily used since it holds site list
    self.choices = []
    self.likes = []
    self.name = current_user
    self.root = "" # initialize root which gets appended to generated suggestions, then get one based on user input
    self.base = "" # initialize safeguard for nonsensical input, based on root
    self.gen_root()
    print('Root word is ' + self.root)
    # get ways how user wants to combine words and execute the combining
    self.combo_types()
    # get whether user wants any of the generated usernames
    self.wanted()

  
  '''
  take user root word, or randomly generate one. root word is what the suggestions are added to
  '''
  def gen_root(self):
    print("To suggest a username, let's first get a root word")
    ask = ""
    if self.name == "":
      ask = input("Do you have a specific root in mind? \n(1) Yes, I'll input one right now\n(else) No, generate one for me\n")
    else:
      ask = input("Do you have a specific root in mind? \n(1) Yes, I'll input one right now\n(2) Yes, use my current username as a root\n(else) No, generate one for me\n")
      if ask == '2':
        self.root = self.name
        self.gen_base()
        return
    if ask == '1':
      self.root = input("Enter your inputted root: ")
      if input("Is this slang for a real word that you want generated words to relate to?\n(y) yes \n(else) no") == 'y':
        self.gen_base(True)
        return
      else:
        self.gen_base()
        return
    print("Ok! Generating random word...")
    self.root = self.random()[0]
    self.gen_base()
  
  '''
  base helps generate suggestions to append to root word
  useful in case of nonsense/obscure input or slang
  '''
  def gen_base(self, slang = False):
    if slang:
      nonslang = input("What real word is your slang term similar to? ")
      self.base = self.similar(nonslang)
    else:
      self.base = self.similar(self.root)
  
  '''
  return the current username that the user picked
  '''
  def liked(self):
      return self.likes
    
  '''
  decide and do combos the user wants with their root word
  '''
  def combo_types(self):
    print("Do you want to combine your root with words with...")
    # generates words that relate to the current root word, check if they they're valid/available, and add them to the choice list if so
    if input("...related words? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...)")
      self.good_choices(self.related(self.base))
    # generates words that rhyme with the current root word, check if they they're valid/available, and add them to the choice list if so
    if input("...rhyming words? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...)")
      self.good_choices(self.rhymes(self.base))
      
    if input("...adjectives? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...)")
      self.good_choices(self.adjec(self.base), False)
    
    if input("...words that start with the same letter? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...)")
      self.good_choices(self.same_letter(self.base))
      
    # generate 10 random words to combine with root word, check if they they're valid/available, and add them to the choice list if so
    if input("...random words? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...)")
      # create random word list
      # take first 10 elements and figure if they're valid/available
      self.good_choices(self.random())
      
    if input("...numbers? (y) yes (else) no\n") == 'y':
      print("(currently creating usernames...will take awhile...)")
      self.good_choices(self.num())
      
    #ask = input("...start with the same letter? (y) yes (else) no")
      
  
  '''
  see what usernames are valid and available, and make them a choice
  '''
  def good_choices(self, words, back = True):
    # this appends words behind the root word
    if back:
      for x in words:
        self.checks.set_user(self.root + x)
        if Valid(self.root + x).fulfilled(self.checks.sites) and self.checks.usuable():
          self.choices.append(self.root + x)
    # if want in front, add words in front of root
    else:
      for x in words:
        self.checks.set_user(x + self.root)
        if Valid(x + self.root).fulfilled(self.checks.sites) and self.checks.usuable():
          self.choices.append(x + self.root)
  
  '''
  determine what the user likes from the available list
  '''
  def wanted(self):
      # print choices
      print("\nAvailable and valid choices:")
      if not self.choices: # if no sites to add just print statement and end
          print("No suggestions that to be added with your input. Sorry, try again!")
          return
      while True:
        for x in range(len(self.choices)):
          print("#{0}. {1}".format(str(x), self.choices[x]))
        choice = input("\nWhat do you want to add?\n(choice) Pick the choice at that number \n(else) None\n")
        for x in range(len(self.choices)):
          if choice == str(x):
            self.likes.append(self.choices[x])
            self.choices.pop(x)
            break # only break, since user may want to add more
          if x == len(self.choices) - 1:
            return # stop adding if non-choice input
        if not self.choices:
          print("All suggestions available added! Can't add anymore.")
          return # stop adding, since all added

  
  '''
  generate random word list
  '''
  def random(self):
    body_text = BeautifulSoup(requests.get("https://jimpix.co.uk/generators/word-generator.asp").text, 'html.parser')
    # remove html markup text
    words = ''.join(body_text.find_all(text = True))
    # isolate actual word list
    random_start = words.find("Random word examples") + len("Random word examples\n\n")
    random_end = words.find("Main Options\n\nCategory") - len("\n\n\n\n")
    words = words[random_start:random_end].split("\n")
    # remove extra characters
    for x in range(10):
      words[x] = ''.join([i for i in words[x] if i.isalpha()])
    return words
  
  '''
  generate list of words related to input
  '''
  def related(self, word):
    return self.list_gen(word, "ml=")
  
  
  '''
  generate list of words that are usd to describe the input
  '''
  def adjec(self, word):
    return self.list_gen(word, "rel_jjb=", 20)
    
  '''
  generate list of numbes 0-99 to appened to words
  '''
  def num(self):
    num_list = []
    for x in list(range(100)):
      num_list.append(str(x))
    return num_list

  '''
  generate list of words that rhymes with input
  '''
  def rhymes(self, word):
    return self.list_gen(word, "rel_rhy=")
      
  '''
  generate list of words that starts with same letter as input. can be compounded with other functions
  ''' 
  def same_letter(self, word):
      return self.list_gen(word[0] + "*", "sp=", 20)
    
  '''
  generate word similar to input, which checks for nonsensical input
  if similar word doesn't generate good relational words, give a get another random word
  '''
  def similar(self, word):
      if not not self.related(word): # has related words = good word
        return word
      # otherwise, generate a similar word
      sim_words = (self.list_gen(word, "sl="))
      sim_word = sim_words[0]
      x = 0
      while not self.related(sim_word) and x < len(sim_words):
        sim_word = (self.list_gen(word, "sl="))[x]
        x = x + 1
      if not self.related(sim_word):
        return self.similar(self.random())
      return sim_word
      
  '''
  generate list of words using th api with given criteria
  ''' 
  def list_gen(self, word, ending, maxi = 15):
      # access api
      word_bank = "https://api.datamuse.com/words?" + ending + word + "&max=" + str(maxi)
      # get body text
      body_text = BeautifulSoup(requests.get(word_bank).text, 'html.parser')
      # extract all words, split up
      words = ''.join(''.join(body_text.find_all(text = True)).split('{"word":"')).split('},')
      word_list = []
      for x in range(len(words)):
        # remove other extraneous characters
        word_list.append(''.join([i for i in words[x].rsplit('","scor')[0] if i.isalpha()]))
#      print(list(set(filter(None, word_list))))
      return list(set(filter(None, word_list)))