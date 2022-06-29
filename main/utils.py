def getPOSTValue(post):
    result = [];
    for data in post:
        result.append(post[data])
    return result[1:]

