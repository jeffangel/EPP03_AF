import sys
from pets.webserver import Webserver

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    webserver = Webserver()
    webserver.run(host='0.0.0.0',port=5000,debug=True)

if __name__ == "__main__":
    sys.exit(main())