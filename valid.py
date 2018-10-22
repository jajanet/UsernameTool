import string
class Valid():
    '''
    initalize validity check for names and lists
    '''
    def __init__(self, name):
      self.name = "START" + name + "END"
      self.invalid_sites = []
      self.valid_sites = []
    
    '''
    specify sites and their criteria
    '''
    def fulfilled(self, sites):
      adjusted = []
      checks = [["Twitter", 1, 15, '_'], ["Instagram", 1, 30, '_.', ['.END', 'START.', '.comEND', '.netEND', '.ioEND', '.orgEND', '.govEND']], ["Facebook", 5, 50, '.', ['.comEND', '.netEND', '.ioEND', '.orgEND', '.govEND']], ["Tumblr", 1, 32, '-', ['START-']], ["Github", 2, 15, '_', ['START_', '__']],['repl.it', 2, 15, '_'], ["Twitch", 4, 25, '_', ['START_']]]
      for x in range(len(sites)):
        for y in range(len(checks)):
          if sites[x][1] == checks[y][0]:
            adjusted.append(checks[y])
      for x in range(len(adjusted)):
        if len(adjusted[x]) == 4:
          self.full_check(adjusted[x][0], adjusted[x][1], adjusted[x][2], adjusted[x][3])
        else:
          self.full_check(adjusted[x][0], adjusted[x][1], adjusted[x][2], adjusted[x][3], adjusted[x][4])
      return self.all_valid()
      
    '''
    call both check functions
    '''
    def full_check(self, name, mini, maxi, chars, prohibitted=[]):
      if self.check_length(mini, maxi) and self.check_char(chars, prohibitted):
        self.valid_sites.append(name)
      else:
        self.invalid_sites.append(name)
    
    '''
    check the length of the name
    '''
    def check_length(self, mini, maxi):
      return (len(self.name) - 8 >= mini) and (len(self.name) - 8 <= maxi)
      
    '''
    check if only valid characters used in the name
    '''
    def check_char(self, chars, prohibitted):
      valid = set(string.ascii_letters + string.digits + chars)
      # check if the name only contains alphanumeric char and ok characters
      if not valid.issuperset(self.name):
        return False
      # check for prohibitted input, if applicable
      if prohibitted:
        for x in prohibitted:
          if x in self.name:
            return False
      return True
        
    '''
    print guidelines for a proper username
    '''
    def print_results(self):
      if self.all_valid:
        print("\nWorks for all sites listed here!\n")
      elif not self.valid_sites:
        print("\nDoesn't work for all sites listed here\n")
        print("\nInvalid on the following sites:")
        for site in self.invalid_sites:
          print(site)
        print("\nValid on the following sites:")
        for site in self.valid_sites:
          print(site)
        print("\n")

    '''
    determine if username is valid on all sites
    '''
    def all_valid(self):
      if not self.invalid_sites:
        return True
      return False
        