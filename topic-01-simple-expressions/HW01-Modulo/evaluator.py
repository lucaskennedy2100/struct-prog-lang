import parser

def evaluate(ast):
    if ast["tag"] == "number":
        return ast["value"]
    elif ast["tag"] == "+":
        return evaluate(ast["left"]) + evaluate(ast["right"])
    elif ast["tag"] == "-":
        return evaluate(ast["left"]) - evaluate(ast["right"])
    elif ast["tag"] == "*":
        return evaluate(ast["left"]) * evaluate(ast["right"])
    elif ast["tag"] == "/":
        return evaluate(ast["left"]) / evaluate(ast["right"])
    elif ast["tag"] == "%":
        if evaluate(ast["left"]) < 0:
            return (evaluate(ast["left"]) % evaluate(ast["right"]))*-1
        return evaluate(ast["left"]) % evaluate(ast["right"])
    else:
        raise ValueError(f"Unknown AST node: {ast}")

def test_evaluate():
    print("test evaluate()")
    ast = {"tag": "number", "value": 3}
    assert evaluate(ast) == 3
    ast = {
        "tag": "+",
        "left": {"tag": "number", "value": 3},
        "right": {"tag": "number", "value": 4},
    }
    assert evaluate(ast) == 7
    ast = {
        "tag": "*",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 3},
            "right": {"tag": "number", "value": 4},
        },
        "right": {"tag": "number", "value": 5},
    }
    assert evaluate(ast) == 35
    #modulo test
    ast = {
        "tag": "%",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 6},
            "right": {"tag": "number", "value": 3},
        },
        "right": {"tag": "number", "value": 2},
    }
    assert evaluate(ast) == 1    
    ast = {
        "tag": "%",
        "left":  {"tag": "number", "value": -9},
        "right": {"tag": "number", "value": 2},
    }
    assert evaluate(ast) == -1 
    ast = {
        "tag": "%",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": -10},
            "right": {"tag": "number", "value": 1},
        },
        "right": {"tag": "number", "value": 2},
    }
    assert evaluate(ast) == -1    
    
if __name__ == "__main__":
    test_evaluate()
    print("done.")