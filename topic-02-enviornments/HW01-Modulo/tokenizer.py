import re
from pprint import pprint #as print #this prints left aligned. if you do it with  as print on the end pprint() becomes a fuinction to do this

#p = re.compile("ab*")

#if p.match("abbbbbbb") :
 #   print("match")
#else:
 #   print("not match")
 #declare a list of possible regex operators
patterns = [
    (r"\s+", "whitespace"),
    (r"\d+", "number"),
    (r"\+", "+"),
    (r"\-", "-"),
    (r"\/", "/"),
    (r"\*", "*"),
    (r"\(", "("),
    (r"\)", ")"),
    (r"\%", "%"), #modulo
    (r".", "error") #only use everything if nothing else matches
]

patterns = [(re.compile(p), tag) for p, tag in patterns] #Patterns is assigned new values--turns from string and tag to compiled pattern and tag

def tokenize(characters): #characters is the passed in list of terms to tokenize
    "Tokenize a string using the patterns above"
    tokens = []
    position = 0
    line = 1
    column = 1
    current_tag = None

    while position < len(characters): #while we've not run out of characters
        for pattern, tag in patterns: #go through only the tags in patterns.
            match = pattern.match(characters, position)
            if match:
                current_tag = tag 
                break #if we encounter a regex, break
        assert match is not None
        value = match.group(0) #set value to the matched item.

        if current_tag == "error": #if what we got equals nothing in the regex, it falls into . for everything.
            raise Exception(f"Unexpected character: {value!r}")
        
        if tag != "whitespace": #we want to filter out anything that is blank, this appends our match to the list of tokens only if it isn't white
            token = {"tag": current_tag, "line": line, "column": column} #set up tokens to be a list of touples with these labels
            if current_tag == "number":
                token["value"] = int(value)
            tokens.append(token) #if we don't have whitespace, append the token to the end of our tokens list
        
        #now advance the position in the line
        for ch in value:
            if ch =="\n":
                line += 1
                column += 1
            else:
                column +=1
        position = match.end()

    #now add a ending token when we're done (kinda like a null)
    tokens.append({"tag": None, "line": line, "column": column})
    return tokens

def test_digits():
    print("test tokenizer")
    t = tokenize("123")
    assert t[0]["tag"] == "number"
    assert t[0]["value"] == 123
    assert t[1]["tag"] is None

def test_operators():
    print("test tokenize operators")
    t = tokenize("( + - * / ) %")
    tags = [tok["tag"] for tok in t]
    assert tags == ["(", "+", "-", "*", "/", ")", "%", None] #modulo tests

def test_expressions():
    print("test tokenize expressions")
    t = tokenize("1+222*3%1")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 222
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] == "%"
    assert t[6]["tag"] == "number" and t[6]["value"] == 1
    assert t[7]["tag"] is None

def test_whitespace():
    print("test tokenize whitespace")
    t = tokenize("1 +\t2  \n*    3")
    assert t[0]["tag"] == "number" and t[0]["value"] == 1
    assert t[1]["tag"] == "+"
    assert t[2]["tag"] == "number" and t[2]["value"] == 2
    assert t[3]["tag"] == "*"
    assert t[4]["tag"] == "number" and t[4]["value"] == 3
    assert t[5]["tag"] is None

def test_error():
    print("test tokenize error")
    try:
        t = tokenize("1@@@ +\t2  \n*    3")
    except Exception as e:
        assert str(e) == "Unexpected character: '@'"
        return
    assert Exception("Error did not happen.")
     

if __name__ == "__main__":
    test_digits()
    test_operators()
    test_expressions()
    test_whitespace()
    test_error()
    print("done.")