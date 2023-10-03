import os
import time
import utils
import socket


stage = 0

def printStage(text: str):
    global stage
    stage += 1
    print(
        f"{utils.GREEN}\n[{utils.RESET}{stage}{utils.GREEN}]{utils.CYAN} +=== {text.upper()} ===+{utils.RESET}"
    )


def printManualStage(text: str):
    print(f"> {utils.GREEN}[{utils.RESET}MANUAL{utils.GREEN}]{utils.RESET} {text}")


def domainToIp(domain_name):
    try:
        if "https" in domain_name:
            domain_name = domain_name[8:]
        if "http" in domain_name:
            domain_name = domain_name[7:]

        ip_address = socket.gethostbyname(domain_name)
        return "{:<17} {}".format(ip_address, domain_name)
    except socket.gaierror:
        return f"[{domain_name}] Invalid domain or unable to resolve"
    except:
        return f"[{domain_name}] Error while getting ip"


# process
def process(domains: list):
    subdomainsFile = os.path.join(os.getcwd(), "subdomains.txt")
    ipAddressFile = os.path.join(os.getcwd(), "ipaddress.txt")
    totalDomainsLen = len(domains)

    # stage 1
    printStage("SCOPE ENUMERATION")
    print(f"> Target domains {domains}")
    printManualStage("Search for related domains.")

    # stage 2
    printStage("INFORMATION GATHERING")
    printManualStage(f"MX Lookup {utils.YELLOW}https://mxtoolbox.com/{utils.RESET}")
    printManualStage(
        f"Spf Records {utils.YELLOW}https://mxtoolbox.com/spf.aspx{utils.RESET}"
    )
    printManualStage(
        f"Certificate Transparancy {utils.YELLOW}https://developers.facebook.com/tools/ct/search/{utils.RESET}"
    )
    printManualStage("Search information about target on dark web")
    print("> Whois & whatweb process")
    tools = [{"n": "whois", "c": ""}]
    for tool in tools:
        name = tool["n"]
        command = tool["c"]

        for index, domain in enumerate(domains):
            try:
                output = os.popen(f"{name} {domain} {command}").read()
            except Exception as e:
                print(f"> {utils.RED}::ERR[{utils.RESET}{e}{utils.RED}]{utils.RESET}")

            if len(output) == 0:
                print(
                    f"> {utils.RED}::ERR Content-Length{utils.GREEN}({utils.RESET}0{utils.GREEN})[{utils.RESET}{domain}{utils.GREEN}]{utils.RESET}"
                )
            else:
                with open(f"{name}.txt", "a", encoding="utf-8") as info:
                    info.write(f"\n{output}\n")
            print(
                f"> {name}{utils.GREEN}({utils.RESET}{len(output)}{utils.GREEN})[{utils.RESET}{domain}{utils.GREEN}]{utils.RESET}"
            )
            time.sleep(1)
        time.sleep(1)
    
    print(f"> {utils.GREEN}+=== Information gathering done. ===+{utils.RESET}")

    # stage 3
    printStage("dorking")
    printManualStage(f"Wikipedia {utils.YELLOW}https://www.wikipedia.org/{utils.RESET}")
    printManualStage(f"Google {utils.YELLOW}https://www.google.com{utils.RESET}")
    printManualStage(f"Github {utils.YELLOW}https://github.com/{utils.RESET}")
    printManualStage(f"Shodan {utils.YELLOW}https://www.shodan.io/{utils.RESET}")
    printManualStage(f"MxToolBox {utils.YELLOW}https://mxtoolbox.com/{utils.RESET}")
    printManualStage(f"Waybacks {utils.YELLOW}https://archive.org/{utils.RESET}")
    printManualStage(
        f"Waybacks {utils.YELLOW}https://timetravel.mementoweb.org/{utils.RESET}"
    )

    # stage 4
    printStage("enumaration process")
    printManualStage(
        f"Virustotal {utils.YELLOW}https://www.virustotal.com/gui/home/search{utils.RESET}"
    )
    print("> Subdomain enumeration")
    totalSubDomains = []
    tools = [
        {
            "n": "assetfinder",
            "c": "",
        },
        {"n": "subfinder", "c": "-silent -d"},
    ]

    for tool in tools:
        name = tool["n"]
        command = tool["c"]
        subcount = 0

        for index, domain in enumerate(domains):
            try:
                output = os.popen(f"{name} {command} {domain}").read()
            except Exception as e:
                print(f"> {utils.RED}::ERR[{utils.RESET}{e}{utils.RED}]{utils.RESET}")

            output = output.splitlines()
            totalSubDomains += output
            outputLen = len(output)
            subcount += outputLen
            print(
                f"> {utils.GREEN}[{utils.RESET}{index + 1}/{totalDomainsLen}{utils.GREEN}]{utils.RESET} {name}{utils.GREEN}[{utils.RESET}{domain}{utils.GREEN}]-({utils.RESET}{outputLen}{utils.GREEN}){utils.RESET}"
            )
            time.sleep(1)

        print(
            f"> {utils.GREEN}[{utils.RESET}{totalDomainsLen}{utils.GREEN}]{utils.RESET} Total result {name}{utils.GREEN}[{utils.RESET}{subcount}{utils.GREEN}]{utils.RESET}"
        )
        time.sleep(1)

    if len(totalSubDomains) == 0:
        print(f"> {utils.RED}::ERR Subdomains not found try again.{utils.RESET}")
    else:
        print(f"> Total subdomains{utils.GREEN}[{utils.RESET}{len(totalSubDomains)}{utils.GREEN}]{utils.RESET}")

    filteredSubDomains = []
    for domain in domains:
        for i in totalSubDomains:
            if f".{domain}" in i:
                filteredSubDomains.append(i)

    uniqueSubDomains = [*set(filteredSubDomains)]
    with open(subdomainsFile, "w") as f:
        f.write("\n".join(uniqueSubDomains))
    time.sleep(2)

    print("> Filtering live domains process")
    try:
        output = os.popen(
            f"""cat "{os.path.join(os.getcwd(), 'subdomains.txt')}" | httpx -silent"""
        ).read()
        if len(output) == 0:
            print(f"> {utils.RED}::ERR Live subdomains not found.{utils.RESET}")
    except Exception as e:
        print(f"> {utils.RED}ERROR: [{utils.RESET}{e}{utils.RED}]{utils.RESET}")
    time.sleep(2)

    with open(subdomainsFile, "w") as f:
        f.write(output)

    print(
        f"""> {utils.GREEN}+=== subdomain enumeration result ===+{utils.RESET}
> total subdomains  : {len(totalSubDomains)}
> filter subdomains : {len(filteredSubDomains)}
> unique subdomains : {len(uniqueSubDomains)}
> live subdomains   : {len(output.splitlines())}
"""
    )

    print("> Ip finding process")
    liveDomains = output.splitlines()
    allIps = []
    for d in liveDomains:
        allIps.append(domainToIp(d))

    with open(ipAddressFile, "w") as ipAFile:
        ipAFile.write("\n".join(allIps))

    print(f"> {utils.GREEN}+=== IP finding done. ===+{utils.RESET}")

    # stage 5
    printStage("extract urls and filtering")
    tools = ["hakrawler", "gau"]
    totalUrls = []

    for tool in tools:
        urlCount = 0

        for index, domain in enumerate(liveDomains):
            try:
                output = os.popen(f'''echo "{domain}" | {tool}''').read()
                output = output.splitlines()
            except Exception as e:
                print(f"> {utils.RED}ERROR: {e}{utils.RESET}")

            temp = []
            for i in output:
                if i[0] == "[" and "] " in i:
                    temp.append(i[i.find("] ") + 2:])
                else:
                    temp.append(i)
            
            with open(os.path.join(os.getcwd(), "all_urls.txt"), "a") as f:
                f.write("\n".join(temp))
            
            totalUrls += temp
            urlCount += len(temp)
            print(
                f"> {utils.GREEN}[{utils.RESET}{index + 1}/{len(liveDomains)}{utils.GREEN}]{utils.RESET} {tool}{utils.GREEN}[{utils.RESET}{domain}{utils.GREEN}]-({utils.RESET}{len(temp)}{utils.GREEN}){utils.RESET}"
            )

        print(
            f"> {utils.GREEN}[{utils.RESET}{len(liveDomains)}{utils.GREEN}]{utils.RESET} Total result {tool}{utils.GREEN}[{utils.RESET}{urlCount}{utils.GREEN}]{utils.RESET}"
        )
        time.sleep(1)
    time.sleep(1)
    
    if len(totalUrls) == 0:
        print(f"> {utils.RED}::ERR Subdomains not found try again.{utils.RESET}")
    else:
        print(f"> Total subdomains{utils.GREEN}[{utils.RESET}{len(totalUrls)}{utils.GREEN}]{utils.RESET}")

    filteredUrls = []
    for domain in liveDomains:
        for url in totalUrls:
            if domain == url[0:len(domain)]:
                filteredUrls.append(url)

    print("> Filtering unique urls")
    uniqueUrls = [*set(filteredUrls)]

    time.sleep(2)
    with open(os.path.join(os.getcwd(), "urls.txt"), "w") as f:
        f.write("\n".join(uniqueUrls))
    
    print("> Finding query urls")
    queryUrls = []
    for url in uniqueUrls:
        if "?" in url and "=" in url:
            queryUrls.append(url)
    
    with open(os.path.join(os.getcwd(), "query_urls.txt"), "w") as f:
        f.write("\n".join(queryUrls))

    print(f"""> {utils.GREEN}+=== Url extraction result ===+{utils.RESET}
> total urls     : {len(totalUrls)}
> filtered urls  : {len(filteredUrls)}
> unique urls    : {len(uniqueUrls)}    
> query urls [?] : {len(queryUrls)}""")
    
    # stage 6
    printStage("overview of the target")
    printManualStage("Information on browser extension")
    printManualStage("Use the features as normal user")
    printManualStage("Find vulnerabilites")

    print(f"\n{utils.GREEN}+====== RECON DONE ======+{utils.RESET}")