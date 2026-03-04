def reverse_list(orginal ):
    reverse = []
    for i in range(len(orginal)-1, -1 ,-1):
        reverse.append(orginal[i])
    return reverse


a = reverse_list([1,2,3,4,5,5,6,7,8,8,5,44,3,22,434])

print(a)