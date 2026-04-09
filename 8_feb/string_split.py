# s = input("enter the string")
s = "ABAABBAAABBBAAAABBBB"
lst = []
sub_s= ""
a_count = 0
b_count = 0
for ch in s:
    if a_count == b_count and a_count != 0 and b_count != 0 :
        lst.append(sub_s)
        sub_s = ""
        a_count = 0
        b_count = 0
    sub_s +=ch
    if ch == 'A':
        a_count +=1
    else:
        b_count +=1

if a_count == b_count :
    lst.append(sub_s)
print(lst)
