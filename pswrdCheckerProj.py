# password checker project which checks how many times a specific password is hacked or found
import requests
import hashlib
import sys

def request_api_data(query_char):
    url='https://api.pwnedpasswords.com/range/'+query_char
    res=requests.get(url)
    if res.status_code!=200:
        raise RuntimeError(f'Error fetching: {res.status_code},check the api amd try again')
    return res

# def read_response(response):
#     print(response.text)

# this func evaluates how many times a particular password has been leaked/hacked
def get_pswrd_leaks_count(hashes, hash_to_check):
    hashes=(line.split(':') for line in  hashes.text.splitlines())
    for h, count in hashes:
        # print(h, count)
        if h==hash_to_check :
            return count
    return 0
    

def pwned_api_check(password):
    # check passwrod if it exists in api response
    sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5Char,rest=sha1password[:5],sha1password[5:]
    # print(first5Char)
    response=request_api_data(first5Char) #we send only first 5 char of our passwords because certainly we do not want to send the complete password over their server
    print(response)
    # return read_response(response)
    return get_pswrd_leaks_count(response,rest)

#if  passwords are taken from command line then run this as main function
# and comment out the main2()
def main(args):  
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was not found.. Carry on')
    return 'done'


# if the passwords are written in a text file then you may use the below func 
# in that case you need to comment out the main() above
def main2(filename): 
    f=open(filename)
    pswrdlist=f.readlines()
    for password in pswrdlist:
        # print(password)
        count=pwned_api_check(password.strip())
        # print(count)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was not found.. Carry on')
    return 'done'

if __name__=='__main__': 
    # below you should execute main() or main2() as per your requirement
    # whichever 'main' you do not comment out ,use that below !
    sys.exit(main2(sys.argv[1]))  
    # sys.exit(main(sys.argv[1:]))
#  note--main() takes list of strings amd main2() takes a string