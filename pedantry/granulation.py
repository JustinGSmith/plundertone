data = [0, 1, 2, 3, 4, 5]

def buffer(l):
    result = l.copy()
    result.extend([0, 0, 0])
    return result

"""
nearly the simplest thing we can call granulation
"""
def granulate0 (l):
    result = []
    buffered = buffer(l)
    for i in range(len(l)):
        result.extend(buffered[i:i+3])
    return result

print("granulate0: ", granulate0(data), "\n")
# granulate0:  [0, 1, 2, 1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 0, 5, 0, 0]


"""
granulation with window and overlap
"""
def granulate1 (l):
    result = [0]
    buffered = buffer(l)
    window = [0.5, 1, 0.5]
    for i in range(len(l)):
        grain = []
        for j in range(len(window)):
            grain.append(window[j] * buffered[i+j])
        # overlap
        result[-1] += grain[0]
        result.extend(grain[1:])
    return result

print("granulate1: ", granulate1(data), "\n")
# granulate1:  [0.0, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 2.5, 0, 0.0]

