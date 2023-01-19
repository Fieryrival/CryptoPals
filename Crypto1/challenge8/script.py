#from Crypto.Cipher import AES

in_file = open('8.txt','rb')
list_of_hex = in_file.readlines()


score_sheet = []
final_scr = 0
line_no = 0
for k in list_of_hex:
    score = 0
    for i in range(10-1):
        for j in range(i+1,10-1):
            str1 = k[(i)*32:(i+1)*32:]
            str2 = k[(j)*32:(j+1)*32:]
        
            if str1 == str2:
                score += 1
                #print(k + " "+str(i)+" "+ str(j) + " " +str1+ " " + str2)
    if score > 0:
        data = {
            'hex':k,
            'score':score,
            'line_no':line_no
        }
        score_sheet.append(data)
    final_scr += score
    line_no = line_no+1

print(score_sheet)
in_file.close()

