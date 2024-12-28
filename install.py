import os
import sys
import utils

print(
    f"""> {utils.CYAN}Current platform{utils.GREEN}[{utils.RESET}{sys.platform}{utils.GREEN}]{utils.RESET}"""
)

if sys.platform == "win32":
    print(f"""{utils.RED}::ERR platform error.{utils.RESET}""")
    exit()

postDeps = {
    "pip": "sudo apt install -y pip",
    "go": "sudo apt install -y golang-go",
    "assetfinder": "sudo apt install -y assetfinder",
    "subfinder": "sudo apt install -y subfinder",
    "hakrawler": "sudo apt install -y hakrawler",
    "whois": "sudo apt install -y whois",
    "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && sudo cp ~/go/bin/httpx /usr/local/bin",
    "gau": "go install github.com/lc/gau/v2/cmd/gau@latest && sudo cp ~/go/bin/gau /usr/local/bin",
}


def checkDep(printAble):
    for key in postDeps:
        if len(os.popen(f"""which {key}""").read()) == 0:
            print(
                f"""> {utils.CYAN}Installing{utils.GREEN}[{utils.RESET}{key}{utils.GREEN}]{utils.RESET}"""
            )
            os.system(postDeps[key])
            continue

        if printAble:
            print(
                f"""> {utils.CYAN}Found{utils.GREEN}[{utils.RESET}{key}{utils.GREEN}]{utils.RESET}"""
            )

if __name__ == "__main__":
    checkDep(True)
    print(f"""{utils.GREEN}+=== Installation success ===+{utils.RESET}""")
