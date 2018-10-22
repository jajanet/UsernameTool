from valid import Valid
from suggest import Suggest
from check import Check

class Username():
    '''
    initialize username tool driver
    '''
    def __init__(self):
      self.look = Check() # initalize checker, stores websites being checked to pass as parameter
      self.names = []
      self.option()

    def change(self):
      passed = False
      while not passed or not self.look.usuable():
        name = input("What do you want to set your username to?")
        self.look.set_user(name)
        self.names.append(name)
        passed = self.avail(name)
        self.names.pop()
  
    '''
   master loop for taking and conduction desired user actions
    '''
  
    def option(self):
      while (True):
        action = input('\nWhat do you want to do?\n(1) Check custom username\n(2) Generate username suggestions\n(3) See site lists\n(4) See stored usernames\n(else) End\n ')
        if action == '1':
          self.change()
        elif action == '2':
          suggestion = Suggest(self.look)
          add = suggestion.liked()
          for x in add:
            self.names.append(x)
        elif action == '3':
          self.look.all_sites()
        elif action == '4':
          self.see_names()
        else:
          print("\nThanks for using the username tool! Bye!")
          return

    '''
    print stored names
    '''
    def see_names(self):
      print("Stored names:")
      if(len(self.names) == 0):
        print("None!")
        return
      for x in self.names:
        print(x)
      action = input("Remove any names?\n(y) Yes \n(else) No\n") 
      if action == 'y':
        self.rem_names()
      else:
        return
        
    def rem_names(self):
      if len(self.names) == 0: # if no sites to remove, prompt adding more
          print("No names to remove")
          return
      print("Removing unwanted names!\n(name number) Remove that name\n(else) Exit")
      while True:
        for x in range(len(self.names)):
          print("#{0}. {1}".format(str(x), self.names[x]))
        user_input = input("")
        for x in range(len(self.names)):
          if user_input == str(x):
            self.names.pop(x)
            break # only break for love, since user may want to remove more
          if x == len(self.names) - 1:
            return # stop removing if non-choice input
        if len(self.names) == 0:
          print("All names removed. Can't remove anymore.")
          return # stop removing, since all are removed
        
        
    '''
    check validity of name, then availability if passed
    '''
    def avail(self, name):
      print("Must ensure username is valid before checking availability...")
      if not Valid(self.names[-1]).fulfilled(self.look.sites):
        print("Username entered not all valid for the current sites! Change your username until it is.")
        return False
      else:
        print("Validity checks all passed! Checking availability of the username {0}...\n".format(self.names[-1]))
        self.look.full_look()
        self.look.done()
        if not self.look.usuable():
          print("Try again, seems like your username is taken somewhere\n")
          return True
      keep = input("Would you like to store this username? (y) yes (else) no")
      if keep == 'y':
        self.names.append(name)
        print("Added {0} to list of names!\n".format(name))
      return True
        
