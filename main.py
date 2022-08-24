import redis

r = redis.Redis(host='localhost', port=6379, db=0)

words = [
    "apple",
    "peach",
    "peaches",
    "banana",
    "bananas"
]


def add_word_to_trie(word):
    stub = ""
    for letter in word:
        stub += letter
        r.hincrby(stub, word, amount=1)


def main():
    r.flushall() # flush all to give clean run
    # Initial load of Redis from horrible DB query to get list of words

    for word in words:
        add_word_to_trie(word)

    print("######## Initial populate search example #########")

    print("p")
    print(r.hgetall("p"))
    
    print("pe")
    print(r.hgetall("pe"))
    
    print("pea")
    print(r.hgetall("pea"))
    
    print("peac")
    print(r.hgetall("peac"))

    # Here "p" returns "peach" or "peaches"
    # On new fields being created by the user, we add these to the trie.
    # When we search again these will be returned as options. 
    # Let's add "pear"

    add_word_to_trie("pear")

    print("######## After adding 'pear' search example #########")

    print("p")
    print(r.hgetall("p"))
    
    print("pe")
    print(r.hgetall("pe"))
    
    print("pea")
    print(r.hgetall("pea"))
    
    print("peac")
    print(r.hgetall("peac"))

    # Note "pear" appears in the search results until we add the letter "c" in "peach".

    # Turns out pears are super popular and our users add this frequently.
    # Let's mimic our users adding "pear" a few more times
    add_word_to_trie("pear")
    add_word_to_trie("pear")
    add_word_to_trie("pear")

    # Now let's search again

    print("######## After adding lots of 'pear' search example #########")

    print("p")
    print(r.hgetall("p"))
    
    print("pe")
    print(r.hgetall("pe"))
    
    print("pea")
    print(r.hgetall("pea"))
    
    print("peac")
    print(r.hgetall("peac"))

    # We can now see 'pear' has a value of 4 while peach and peaches is on one.
    # We can use this to sort our response so we only show the top X number of results.

    # Note hgetall is O(n) - we need this to be able to add in the weightings.
    # To then make use of the weightings we need to then loop over the results
    # and sort them making this as least O(2n)
    # If we get rid of weightings we can make this O(n)


def add_unweighted_word_to_trie(word):
    stub = ""
    for letter in word:
        stub += letter
        r.sadd(stub, word)


def unweighted_main():
    r.flushall() # flush all to give clean run

    for word in words:
        add_unweighted_word_to_trie(word)

    print("######## Initial unweighted populate search example #########")

    print("p")
    print(r.smembers("p"))
    
    print("pe")
    print(r.smembers("pe"))
    
    print("pea")
    print(r.smembers("pea"))
    
    print("peac")
    print(r.smembers("peac"))

    # Returns results for peach and peaches, let's add "pear" and see what happens

    add_unweighted_word_to_trie("pear")

    print("######## After adding 'pear' search example #########")

    print("p")
    print(r.smembers("p"))
    
    print("pe")
    print(r.smembers("pe"))
    
    print("pea")
    print(r.smembers("pea"))
    
    print("peac")
    print(r.smembers("peac"))


# main() is weighted example
main()
# unweighted_main() in unweighted example
unweighted_main()