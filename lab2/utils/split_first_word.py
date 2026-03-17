def split_first_word(sentence):
    word = ""
    remainder = ""
    i = 0
    while i < len(sentence):
        c = sentence[i]
        if c.isalpha():
            word += c
        #ommit first whitespaces
        elif len(word) != 0:
            break
        i += 1
    
    remainder = sentence[i:]

    return word, remainder