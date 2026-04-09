lst = [7,'$',5,9,'.',1]
ints = [i for i in lst if isinstance(i, int)]
sorted_lst = sorted(ints)
j = 0
for i in range(0,len(lst)):
    if type(lst[i]) != str:
        lst[i] = sorted_lst[j]
        j+=1
print(lst)
