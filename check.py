from bs4 import BeautifulSoup
import requests
class Check():
  
    '''
    initialize
    '''
    def __init__(self):
      self.user = ""
      self.sites = [ ['https://twitter.com/', 'Twitter', "Sorry, that page doesn’t exist!"], ['https://instagram.com/', 'Instagram', "Sorry, this page isn't available."], ['https://facebook.com/', 'Facebook', 'Page Not Found | Facebook']] # tumblr not working now [".tumblr.com", "Tumblr", "\n                    There's nothing here.\n                ", 'fronturl'] ]
      self.stored_sites = [ ['https://github.com/', 'GitHub', 'Not Found'], ['https://repl.it/@', 'repl.it', 'This page could not be found'] ] #,  ['https://www.twitch.tv/ninja', 'Twitch', 'Sorry. Unless you’ve got a time machine, that content is unavailable.'] ]
      self.avail = []
      self.unavail = []

    '''
    set the username, while also clearning unavail and avail sites in the lists--which would otherwise become cluttered from previous usernames due to the append feature
    '''
    def set_user(self, user):
      self.user = user
      self.unavail = []
      self.avail = []
      
      
    '''
    remove undesired sites
    '''
    def rem_sites(self):
      if len(self.sites) == 0: # if no sites to remove, prompt adding more
          if input("No sites that can be removed. Add some?\n(y) yes \n(else) no") == 'y':
            self.add_sites()
            self.all_sites()
          return
      print("Removing unwanted sites!\n(site number) Remove that site\n(else) Exit")
      while True:
        for x in range(len(self.sites)):
          print("#{0}. {1}".format(str(x), self.sites[x][1]))
        user_input = input("")
        for x in range(len(self.sites)):
          if user_input == str(x):
            self.stored_sites.append(self.sites.pop(x))
            break # only break for love, since user may want to remove more
          if x == len(self.sites) - 1:
            return # stop removing if non-choice input
        if len(self.sites) == 0:
          print("All sites removed. Can't remove anymore.")
          return # stop removing, since all are removed
          
    '''
    add sites
    '''
    def add_sites(self):
      if len(self.stored_sites) == 0: # if no sites to add just print statement and end
          print("All sites available already being checked. Can't add more.")
          return
      print("Adding additional sites!\n(site number) Add that site\n(else) Exit")
      while True:
        for x in range(len(self.stored_sites)):
          print("#{0}. {1}".format(str(x), self.stored_sites[x][1]))
        user_input = input("")
        for x in range(len(self.stored_sites)):
          if user_input == str(x):
            self.sites.append(self.stored_sites.pop(x))
            break # only break, since user may want to add more
          if x == len(self.stored_sites) - 1:
            return # stop adding if non-choice input
        if len(self.stored_sites) == 0:
          print("All sites available added! Can't add anymore.")
          return # stop adding, since all added
      
      
    '''
    define sites and parameters for username availability, then call a search
    '''
    def full_look(self):
      for x in range(len(self.sites)):
        #if len(self.sites[x]) == 3:
          self.search(self.sites[x][0], self.sites[x][1], self.sites[x][2])
          ''' currently only needed for tumblr, which isn't working right now
        else:
          self.search(self.sites[x][0], self.sites[x][1], self.sites[x][2], self.sites[x][3])
          '''
    
    '''
    search the appropriate sites
    '''
    def search(self, site, name, avail_phrase, other='backurl'):
      url = site + self.user
      if other == 'fronturl':
        url = 'https://' + self.user + site
      body_text = BeautifulSoup(requests.get(url).text, 'html.parser')
      # if availabiltiy phrase found, username is available on that site
      words = body_text.find_all(text = avail_phrase)
      # if availability phrase not found, username is unavailable
      if not words:
        self.unavail.append(name)
        return False
      # otherwise, there's a chance it can be used
      self.avail.append(name)
      return True
        
    '''
    check to see if username avail on all sites. automatically return false if not on site
    '''
    def usuable(self):
      for x in range(len(self.sites)):
        #if len(self.sites[x]) == 3:
          if not self.search(self.sites[x][0], self.sites[x][1], self.sites[x][2]):
            return False
          ''' only for tumblr, which isn't working right now
        else:
          if not self.search(self.sites[x][0], self.sites[x][1], self.sites[x][2], self.sites[x][3]):
            return False
          '''
      return True
    
    '''
    print sites
    '''    
    def all_sites(self):
      if not self.sites or not self.stored_sites:
        if not self.sites:
          print('No sites being checked')
        else:
          print('All sites are being checked')
        print("Sites:")
        for n in self.sites + self.stored_sites:
          print(n[1])
      else:
        print("\nSites being checked:")
        for n in self.sites:
          print(n[1])
        else: 
          print("\nSites currently stored and not checked:")  
          for n in self.stored_sites:
            print(n[1])
      while True:
        action = input("\nDo anything else?\n(0) Yes, see username validity guidelines for sites being checked\n(1) Yes, remove from list of sites being checked\n(2) Yes, add to list of sites being checked\n(else) No\n") 
        if action == '0':
            self.guides()
        elif action == '1':
            self.rem_sites()
        elif action == '2':
            self.add_sites()
        else:
          return
    
    '''
    print results
    '''    
    def done(self):
      if not self.avail or not self.unavail:
        if not self.avail:
          print('Not available on any site!')
        else:
          print('Likely available on every site!*')
        print("Sites:")
        for n in self.avail + self.unavail:
          print(n)
      else:
        print("\nUsername might be available on:*")
        for n in self.avail:
          print(n)
        else: 
          print("\nUsername unavailable on:")  
          for n in self.unavail:
            print(n)
      
      print("\n*username could be owned by private/banned user and not allowed for use\n")
          
    '''
    print guidelines for a proper username, only for sites that the user is interested in
    '''
    def guides(self):
      print("\nProper username guidelines for sites:")
      # all available domains
      raw_guides = [['Twitter', '1-15 char, with any combo of alphanumeric and underscore chars'], ['Instagram', '1-30 char, with any combo of alphanumeric, and period or underscore chars. Cannot start with a periods, and cannot end with periods or domains, like ".com" or ".org"'], ['Facebook', '5-50 char, with any combo of alphanumeric, and period chars. A username with a period is considered the same as the same one without. Cannot end with domains, like ".com" or ".org"'], ['GitHub', '2-15 char, with any combo of alphanumeric and underscore chars. Cannot start with underscore or have consecutive underscores'], ['Tumblr', '1-32 char, with any combo of alphanumeric and hyphen chars. Cannot start with hyphen'], ['repl.it', '-25 char, with any combo of alphanumeric and underscore chars. Cannot start with underscore'], ['Twitch', '4-25 char, with any combo of alphanumeric and underscore chars. Cannot start with underscore']]
      # create separate list that only includes the guides for the sites the user wants to look at
      adjusted_guides = []
      for x in range(len(self.sites)):
        for y in range(len(raw_guides)):
          if self.sites[x][1] == raw_guides[y][0]:
            adjusted_guides.append(raw_guides[y])
            print("{0}:\n{1}".format(raw_guides[y][0], raw_guides[y][1]))
      if not adjusted_guides:
        print("No sites are being checked! No guidelines to print\n")
      # github
      # reddit - _ a-z 0-9, 3-20