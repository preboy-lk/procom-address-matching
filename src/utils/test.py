import sys

def main(argv, arc):
    print(argv, arc)

if __name__ == '__main__':
    main(sys.argv[-1], len(sys.argv))