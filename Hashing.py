#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class HashTable:
    """This class represents Hashtables.
    Parameters
    ----------
    self.m - the size of the hashtable 
    self.hash_table - an empty hashtable with size m         
    self.prime - a prime number used in the second hashh table
    Methods
    -------
    double_hashing(self, key,j,hashtable)
        A hash function made of two hash functions
    tables(self, x, y, k)
        Creates hash tables for substrings in x and y 
    rh_get_match(self,x,y,substring)
        Finds overlapping hash values in hash tables
     """
    
    def __init__(self, m):
        """Creates the Hashtable instance, creates an empty hash table with size m.
        
        Parameters
        ----------
        m : integer
            The size of a hash table
        """
        self.m = m
        self.hash_table = [None for _ in range(m)]
        self.prime = 11 # a prime number for the second hash function

    def isPrime(self, x):
        """Checks whether a number is prime.
        
        Parameters
        ----------
        x : integer
            a number to be checked on being prime
        Returns
        -------
        boolean
            True if prime  
        """
        for j in range(2,int(x**0.5)+1): 
            if x%j==0: # if divisible 
                return False
        return True

    def findPrimeNum(self, num):
        """Finds the largest prime number smaller than num.
        
        Parameters
        ----------
        num : integer
            a number which is larger than desired prime number
        Returns
        -------
        integer
            a prime integer  
        """
        for i in range(num-1,1,-1):
            if self.isPrime(i):
                return i
    
    def double_hashing(self, key,j,hashtable):
        """Creates a hash value for a key.
        
        Parameters
        ----------
        key : string
            A substring
        Returns
        -------
        integer
            A hash value from two hash functions        
        """
        h = 0 # setting h to 0
        base = 7 # we work with the base of seven for convenience 
        q = self.findPrimeNum(self.m) # finding q in n mod q in the first hash function 
        for i in key: # finding h(x)
            h += (ord(i)*base**(len(key)-key.index(i)-1)) 
        
        # if there is already a key with the same hash value, we increment i by 1
        while (h % q + j * (self.prime - h % self.prime)) % q in hashtable: 
            j += 1
        #estimating a hahs value for the key 
        value = (h % q + j * (self.prime - h % self.prime)) % q
        return value
    
    def tables(self, x, y, k):
        """Creates hash tables for substrings in x and y.
        
        Parameters
        ----------
        x : string
            The text which is checked for plagiarims 
        y : string
            The original text
        
        Returns
        -------
        lists
            Contains hash values of substrings of x and y       
        """
        j = 1
        valuesx = [] # storing hash values for substrings in x
        valuesy = [] # storing hash values for substrings in y
        keys = [] # stroing keys
        
        for i in range(len(y)-k+1):
            if y[i:k+i] in keys: # if a substring exists already exists in the hast table, we append its value
                valuesy.append(valuesy[keys.index(y[i:k+i])])
            else: # otherwise we calculate a new hash value and append the substring (key) and its hash value (value)
                h = self.double_hashing(y[i:k+i],j,valuesy)
                valuesy.append(h)
                keys.append(y[i:k+i])
        j = 1
        # repeat the same approach for building a hash table for y 
        for i in range(len(x)-k+1):
            h = self.double_hashing(x[i:k+i],j,valuesx)
            valuesx.append(h)
        return valuesy, valuesx

    def rh_get_match(self,x,y,substring):
        """Finds a match between substrings in x and y.
        
        Parameters
        ----------
        x : string
            The text which is checked for plagiarims 
        y : string
            The original text
        substring: integer
            The length of substrings 
        
        Returns
        -------
        a list of tuples 
            Contains indices of similar substrings of x and y       
        """
        h_x = self.tables(x,y,substring)[1] # gettig hash values for all substrings 
        h_y = self.tables(x,y,substring)[0]
        sim = [] # stores tuples
        m = len(x)
        n = len(y)
        for i in h_x: # loop through all entries in x hash tables 
            k = 0
            while k <= n-m+1:
                if h_y[k] == i: # is a similar hash value is found, append their corresponding indices to the list 
                    sim.append((k,h_x.index(i)))
                k = k+1
        print(round((len(sim)*substring)/len(x)*100,2), "% is plagiarised") # the formula for plagiarism 
        return sim

original_x = "Day"
original_y = "Today is Monday"

# characters to be removed from the orginal texts 
bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']',' '] 

# removing bad characters and putting all characters in x and y to the lower case
x_just_text = ''.join(c for c in original_x if c not in bad_chars).lower()
x = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in x_just_text)

y_just_text = ''.join(c for c in original_y if c not in bad_chars).lower()
y = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in y_just_text)

m = round(len(y) * 1.3) # the table size depends of the length of y as y>x and we need space for all substrings
n = 1
for i in original_x:
    if i == " ":
        n += 1
k = round(len(original_x)/n) # k is assumed to be the averag elength of all words in x

table = HashTable(m)
print(table.rh_get_match(x,y,2))


# In[ ]:


# test case 1
original_x = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean and hideous that all Harry wanted was to get back to the Hogwarts School for Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a warning from a strange impish creature who says that if Harry returns to Hogwarts, disaster will strike. And strike it does. For in Harry’s second year at Hogwarts, fresh torments and horrors arise, including an outrageously stuck-up new professor and a spirit who haunts the girls’ bathroom. But then the real trouble begins – someone is turning Hogwarts students to stone. Could it be Draco Malfoy, a more poisonous rival than ever? Could it possible be Hagrid, whose mysterious past is finally told? Or could it be the one everyone at Hogwarts most suspects… Harry Potter himself!"

original_y = "Harry Potter's life is miserable. His parents are dead and he's stuck with his heartless relatives, who force him to live in a tiny closet under the stairs. But his fortune changes when he receives a letter that tells him the truth about himself: he's a wizard. A mysterious visitor rescues him from his relatives and takes him to his new home, Hogwarts School of Witchcraft and Wizardry. After a lifetime of bottling up his magical powers, Harry finally feels like a normal kid. But even within the Wizarding community, he is special. He is the boy who lived: the only person to have ever survived a killing curse inflicted by the evil Lord Voldemort, who launched a brutal takeover of the Wizarding world, only to vanish after failing to kill Harry. Though Harry's first year at Hogwarts is the best of his life, not everything is perfect. There is a dangerous secret object hidden within the castle walls, and Harry believes it's his responsibility to prevent it from falling into evil hands. But doingso will bring him into contact with forces more terrifying than he ever could have imagined. Full of sympathetic characters, wildly imaginative situations, and countless exciting details, the first installment in the series assembles an unforgettable magical world and sets the stage for many high-stakes adventures to come."

bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']',' ']

x_just_text = ''.join(c for c in original_x if c not in bad_chars).lower()
x = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in x_just_text)

y_just_text = ''.join(c for c in original_y if c not in bad_chars).lower()
y = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in y_just_text)

m = round(len(y) * 1.3)
n = 1
for i in original_x:
    if i == " ":
        n += 1
k = round(len(original_x)/n) 

table = HashTable(m)
print(table.rh_get_match(x,y,k))
print("Substring length:", k)


# In[ ]:





# In[ ]:


class HashTable:
    """This class represents the creation of a Hashtable.
     Parameters
     ----------
    self.m - the size of the hashtable 
    self.hash_table - an empty hashtable with size m         
    self.base - a base value used to calculate hash values in hash functions
    Methods
    -------
    get_h(self, string)
        A hash function that converts a string to a number 
    tables(self, x, k)
        Creates a hash table with hash values of substrings with lengths k in x
    regular_get_match(self,x,y,substring)
        Finds the overlapping hash values in hash tables of substrings in x and y
     """
    def __init__(self, m):
        """Creates the Hashtable instance, creates an empty hash table with size m.
        
        Parameters
        ----------
        m : integer
            The size of a hash table
        """
        self.m = m
        self.hash_table = [None for _ in range(m)]
        self.base = 11

    def get_h(self, string):
        """Finds a hash value of a string.
        
        Parameters
        ----------
        string : string
            A substring which hash value to be estimated 
        Returns
        -------
        integer
            A hash value 
        """
        h = 0 # setting h to 0
        for i in range(len(string)): # iterate through each letter in the string 
            h += ord(string[i])*self.base**(len(string)-i-1) # add the numerical conversion of a letter to h 
        return int(str(h*h)[2:6]) # finding a hash value by taking middle four numbers of the square of h 
    
    def tables(self, x, k):
        """Creates a hash table for k length substrings in x.
        
        Parameters
        ----------
        x : string
            The original string which is checked for plagiarism
        k : integer 
            The length of substrings
        Returns
        -------
        list
            Contains hash values 
        """
        values = [] # stores values of keys which are hash values found using the hash function 
        keys = [] # stores keys which are substrings 
         
        for i in range(len(x)-k+1): # iterates through x len(x)-k+1 times where k is the legnth of substrings
            h = self.get_h(x[i:k+i]) # find h for a substring 
            if x[i:k+i] in keys: # if a substrings already exists in the keys list
                values.append(values[keys.index(x[i:k+i])]) # we append its value to the values list 
            else: # if it is a unique key
                values.append(h) # we append its h to the values list 
                keys.append(x[i:k+i]) # we append the substring to the leys list 
        return values
    
    def regular_get_match(self,x,y,k):
        """Finds a match between substring h values in x and y.
        
        Parameters
        ----------
        x : string
            The original string which is checked for plagiarism
        y: string
            The original string which is checked for plagiarism
        k : integer 
            The length of substrings        
        Returns
        -------
        list
            Contains tuples of indices corresponding to similar substrings
        """
        h_x = self.tables(x,k) # creates a hash table for substrings in x
        sim = [] # stores tuples with overlapping substrings in x and y 
        for i in h_x: # for all hast values in h_x find similiraties in the hash table of y 
            q = 0 # setting the index to 0 
            while q <= len(y)-len(x)+1: # while there are substrings to check 
                if self.get_h(y[q:q+k]) == i: # if we find the same hash values 
                    sim.append((q,h_x.index(i))) # we append the indices of keys as a tuple to the list 
                q = q+1 # keep incrementing 1 to the index until a sinilairity is found 
        # print a percentage of overlapping substrings with length k relative to the original text x
        print(round((len(sim)*k)/len(x)*100,2), "% is plagiarised")  
        return sim
    
original_x = "Day"
original_y = "Today is Monday"

# characters to be removed from the orginal texts 
bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']',' '] 

# removing bad characters and putting all characters in x and y to the lower case
x_just_text = ''.join(c for c in original_x if c not in bad_chars).lower()
x = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in x_just_text)

y_just_text = ''.join(c for c in original_y if c not in bad_chars).lower()
y = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in y_just_text)

# the size of the hashtable is set to the length of y time 1.3  
m = round(len(y) * 1.3)
n = 1
for i in original_x:
    if i == " ":
        n += 1
k = round(len(original_x)/n) # k is the average length of all words in y 

table = HashTable(m)
print(table.regular_get_match(x,y,2))


# In[ ]:


# test case 1
original_x = "However, when it comes to my husband, I will say that I am definitely biased, and for good reason. I have been with Donald for 18 years and I have been aware of his love for this country since we first met. He never had a hidden agenda when it comes to his patriotism, because, like me, he loves this country so much. I was born in Slovenia, a small, beautiful and then-communist country in Central Europe. My sister Ines, who is an incredible woman and a friend, and I were raised by my wonderful parents. My elegant and hard-working mother Amalia introduced me to fashion and beauty. My father Viktor instilled in me a passion for business and travel. Their integrity, compassion and intelligence reflects to this day on me and for my love of family and America. "

original_y = "As you might imagine, for Barack, running for president is nothing compared to that first game of basketball with my brother, Craig. I can't tell you how much it means to have Craig and my mom here tonight. Like Craig, I can feel my dad looking down on us, just as I've felt his presence in every grace-filled moment of my life. At 6-foot-6, I've often felt like Craig was looking down on me too ... literally. But the truth is, both when we were kids and today, he wasn't looking down on me. He was watching over me. And he's been there for me every step of the way since that clear February day 19 months ago, when — with little more than our faith in each other and a hunger for change — we joined my husband, Barack Obama, on the improbable journey that's brought us to this moment. But each of us also comes here tonight by way of our own improbable journey. I come here tonight as a sister, blessed with a brother who is my mentor, my protector and my lifelong friend. I come here as a wife who loves my husband and believes he will be an extraordinary president. I come here as a mom whose girls are the heart of my heart and the center of my world — they're the first thing I think about when I wake up in the morning, and the last thing I think about when I go to bed at night. Their future — and all our children's future — is my stake in this election."

bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']',' ']

x_just_text = ''.join(c for c in original_x if c not in bad_chars).lower()
x = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in x_just_text)

y_just_text = ''.join(c for c in original_y if c not in bad_chars).lower()
y = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in y_just_text)

m = round(len(y) * 1.3)
n = 1
for i in original_x:
    if i == " ":
        n += 1
k = round(len(original_x)/n) 

table = HashTable(m)
print(table.regular_get_match(x,y,k))


# In[ ]:


# test case 2
original_x = "In Turkey, the traditional hammams or also called Turkish baths are wet steam baths that developed in the Ottoman Empire after the capture of Constantinople in 1453. Inspired by Roman baths, the hammam developed in the Ottoman Empire, the Maghreb, and as far as the Middle East. A hammam is a place of purification of body and mind and cleanliness. Istanbul has about sixty baths, it would be a shame to miss this experience! Traditionally,the hammam is divided into three rooms. You will find the first room at room temperature which acts as a cloakroom. In the second room, the temperature is a little higher but remains warm (37°C/38°C), the last room is the warmest room (50°C) where we sit on a bench in marble and where you let yourself sweat."
original_y = "While this culture based on the Roman Empire, the tradition is completely associated with the Ottoman and Turkish culture. When you take this traditional attraction, you can enjoy an authentic experience, relax your muscles, rest in a steam bath, refresh your body, get peeling, lots of body massages, aromatherapy, etc. You’ll find yourself like you are living in a palace or pavilion on that era, and experience the culture and traditional rituals in an impressive and authentic atmosphere.The environment can be considered as you are in shrine of healing, relaxation and purification with the sprit of water. The environment inside is warm and lets your whole body and muscles relax. When you get to the hammam, you’ll start your day with a personal care kit comes with an Ottoman style basin in gold plate, private bath gloves (“kese” in Turkish), olive oil soap and several accessories. You can than choose from several packages and rituals such as traditional body scrubbing, relaxing bubble wash, aromatherapy massage, face masks, body care, peeling, etc."
 
bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']',' ']

x_just_text = ''.join(c for c in original_x if c not in bad_chars).lower()
x = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in x_just_text)

y_just_text = ''.join(c for c in original_y if c not in bad_chars).lower()
y = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in y_just_text)

m = round(len(y) * 1.3)
n = 1
for i in original_x:
    if i == " ":
        n += 1
k = round(len(original_x)/n) 

table = HashTable(m)
print(table.regular_get_match(x,y,k))

