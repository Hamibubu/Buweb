#!/usr/bin/env python3
import requests, sys, signal, argparse, re, urllib
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from tqdm import tqdm

Bienvenida = " ______                    _     \n" + "(____  \                  | |    \n" + " ____)  )_   _ _ _ _  ____| | _  \n" + "|  __  (| | | | | | |/ _  ) || \ \n" + "| |__)  ) |_| | | | ( (/ /| |_) )\n" + "|______/ \____|\____|\____)____/ \n"

print(Bienvenida)
links = []

def handler(sig, frame):
    print("\n\n[i] SALIENDO\n")
    sys.exit(1)

#Decimos que es lo que tenemos que hacer cuando demos CTRL+C
signal.signal(signal.SIGINT, handler) 

def getARG():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="http/https://tudominio.com así")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="/usr/share/wordlists/rockyou.txt por ejemplo")
    parser.add_argument("-s", "--subdomain", dest="subdomain", help="Opcion para buscar subdominios", default=False, action="store_true")
    parser.add_argument("-d", "--dirs", dest="dirs", help="Opcion para escanear directorios", default=False, action="store_true")
    parser.add_argument("-c", "--crawl", dest="crawl", help="Opcion para hacer crawling", default=False, action="store_true")
    parser.add_argument("-e", "--export", dest="export", help="Opcion para exportar resultados")
    parser.add_argument("-b", "--brute", dest="brute", help="Opcion para fuerza bruta", default=False, action="store_true")
    opcion = parser.parse_args()
    if not opcion.url:
        parser.error("[-] Especifica una url, para ayuda ve a -h")
    if not opcion.wordlist:
        if (opcion.subdomain | opcion.dirs | opcion.brute):
            parser.error("[-] Especifica una wordlist, para ayuda ve a -h")
    return opcion

#Agrega el subdominio
def acomoda(url, ext):
    url = url.split('://')
    new = url[0] + '://' + ext + '.' + url[1]
    return new

#Importamos la wordlist para subdirectorios
def importa_wsd(url, cuenta, prog, wordlist):
    with open(wordlist,  "r", encoding='latin-1') as file: 
        for i in file:
            prog.update(1)
            i = i.strip()
            manda_url = acomoda(url, i)
            respuesta = manda(manda_url)
            if respuesta:
                print(manda_url,"[UP]","\n", end="\r")
                links.append(manda_url)
        prog.close()

#Importamos la wordlist para directorios
def importa_wdr(url, cuenta, prog, wordlist):
    with open(wordlist,  "r", encoding='latin-1') as file: 
        for i in file:
            prog.update(1)
            i = i.strip()
            manda_url = url + '/' + i
            print(manda_url)
            respuesta = manda(manda_url)
            if respuesta:
                print(manda_url,"[UP]","\n", end="\r")
                links.append(manda_url)
        prog.close()

#Extrae los links en el codigo fuente
def saca(turl):
    resp = requests.get(turl)
    return re.findall('(?:href=")(.*?)"', resp.content.decode(errors="ignore"))


def crawl(turl):
    href = saca(turl)
    try:
        for link in href:
            link = urlparse.urljoin(turl, link)
            if "#" in link:
                link = link.split('#')[0]
            if opcion.url in link and link not in links:
                    links.append(link)
                    print(link)
                    crawl(link)
    except AttributeError:
        pass

#Cuenta las palabras de la wordlist
def cuenta(wordlist):
    arch = open(wordlist,  "r", encoding='latin-1')
    for xd, rd in enumerate(arch):
        pass
    return xd

def Brute_force(url, wordlist):
    resp = manda(url)
    html = BeautifulSoup(resp.content, features="lxml")
    html_form = html.findAll("form")
    for i in html_form:
        link_a_mandar = urllib.parse.urljoin(url, (i.get("action")))
        metodo = i.get("method")
        inputs = i.findAll("input")
        dicc = {}
        user = input("[*] Dame el username: ")
        with open(wordlist,"r",encoding='latin-1') as contra:
            for cont in contra:
                for j in inputs:
                    cont = cont.strip()
                    nombre = j.get("name")
                    tipo = j.get("type")
                    valor = j.get("value")
                    if tipo == 'password': # Cambiar si se requiere
                        valor = cont
                    if ((tipo == 'text') | (nombre == 'username')): #Cambiar si se requiere
                        valor = user
                    dicc[nombre] = valor 
                if metodo == "post":
                    res = requests.post(link_a_mandar, data=dicc)
                elif metodo == "get":
                    res = requests.get(link_a_mandar, params=dicc)
                if "Login failed" not in str(res.content):
                    print("[+] Contra encontrada ", cont)
                    exit()

#Mandamos la peticion
def manda(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.InvalidSchema:
        print(url)
        pass
    
#Input para la url
opcion = getARG()
if not opcion.crawl and not opcion.brute:
    tam = cuenta(opcion.wordlist)
    Barra_progreso = tqdm(total=tam, unit='iB', unit_scale=True)
    if opcion.subdomain:
        importa_wsd(opcion.url, tam, Barra_progreso, opcion.wordlist)
    elif opcion.dirs:
        importa_wdr(opcion.url, tam, Barra_progreso, opcion.wordlist)
elif opcion.crawl:
    crawl(opcion.url)
elif opcion.brute:
    Brute_force(opcion.url, opcion.wordlist)
if opcion.export:
    with open((opcion.export + ".txt"), "w") as xd:
        xd.write(str(links))
