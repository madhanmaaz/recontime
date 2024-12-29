import os
import sys
import utils
import processor

if "-h" in sys.argv or len(sys.argv) != 2:
    print("Usage: recontime domains.txt")
    exit(0)

def recon():
    try:
        domainsFile = os.path.join(os.getcwd(), sys.argv[1])
        if not os.path.exists(domainsFile):
            print(f">{utils.RED} ::ERR {domainsFile} Domains file not found.{utils.RESET}")
            exit(1)

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
    recon()


if __name__ == "__main__":
    main()
