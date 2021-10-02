def is_isogram(s):
    seen = []
    for w in range(s):
        if w in seen:
            return True
        else:
            seen += i
    return False

print(is_isogram("qwdqwdqwdqwdqwdqwd"))