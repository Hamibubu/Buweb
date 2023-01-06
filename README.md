# buweb
Crawler, bruteforce directory, bruteforce login

## ¿How to use it?

-u Specify url 
```text
-u "https://example.com/"
```

-w Wordlist

```text
-w /usr/share/wordlists/rockyou.txt
```
-s Option to scan subdomains

-e Export the results on a txt, put the name of the file

-c Option to crawl

-b Option for bruteforcing a login page

## How to install


```text
git clone https://github.com/Hamibubu/buweb.git
```

Install the requirements.txt

```text
pip3 install -r requirements.txt
```
Run it 

Example

```text
python3 Buweb.py -u "http://domain.com/" -c
```
