import os
import utils
import install
import processor

def checkRecon():
    allFiles = os.listdir(os.getcwd())
    reStart = False

    for i in allFiles:
        if ".txt" in i:
            userInput = input("(Already recon done. if you want to recon again)[y/n]> ")

            if userInput == "":
                exit()
            elif userInput == "y":
                reStart = True
            elif userInput == "n":
                exit()
            break

    if reStart:
        for i in allFiles:
            try:
                if ".txt" in i:
                    os.remove(os.path.join(os.getcwd(), i))
            except:
                pass
        return

def recon():
    try:
        domainsFile = os.path.join(os.getcwd(), "domains")
        if os.path.exists(domainsFile):
            print(
                f">{utils.CYAN} Domains filepath{utils.GREEN}[{utils.RESET}{domainsFile}{utils.GREEN}]{utils.RESET}"
            )

            with open(domainsFile, "r") as df:
                data = df.read().splitlines()
                if len(data) == 0:
                    print(f"> {utils.RED}::ERR Empty domains file.{utils.RESET}")
                else:
                    domains = []
                    for domain in data:
                        if len(domain) != 0:
                            domains.append(domain)

                    processor.process(domains)
        else:
            print(f">{utils.RED} ::ERR Domains file not found.{utils.RESET}")
            print(f">{utils.CYAN} Creating doamins file.{utils.RESET}")
            print(f" Example           : google.com,facebook.com,instagram.com")
            print(f" Verbose           : -v")
            print(f" Clear             : -c")
            print(f" To save and recon : -s")
            allDomains = ""

            while True:
                domains = input(
                    f"{utils.CYAN}[{utils.RESET}Enter domains{utils.CYAN}]{utils.RESET}> "
                )

                if len(domains) == 0:
                    continue
                elif domains == "-s":
                    print(allDomains)
                    break
                elif domains == "-v":
                    print(allDomains)
                elif domains == "-c":
                    allDomains = ""
                else:
                    if "." not in domains:
                        continue

                    for d in domains.split(","):
                        allDomains += f"\n{d}"

            with open(domainsFile, "w") as f:
                f.write(allDomains)

            recon()
    except KeyboardInterrupt:
        exit()


def main():
    print(
        f"""{utils.RED}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║{utils.RESET}{utils.CYAN}     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ TIME
                    {utils.GREEN}- Designed by madhan
                    {utils.CYAN}- https://madhanmaaz.netlify.app                  
                    - https://github.com/madhanmaaz/recontime{utils.RESET}                   
"""
    )
    install.checkDep(False)
    checkRecon()
    recon()


if __name__ == "__main__":
    main()
