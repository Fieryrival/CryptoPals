encoded_text = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

target = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
ans = b''
key = 'ICE'
j=0
for i in encoded_text:
    ans += bytes([i^ord(key[j])])
    j=j+1
    if j>2:
        j=j%3
res = ans.hex()
print(res)
if target==res:
    print('done')
else:
    print('fail')