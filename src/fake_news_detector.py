import argparse, sys, os
def main():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--cli', action='store_true')
    g.add_argument('--gui', action='store_true')
    args = parser.parse_args()
    sys.path.append(os.path.dirname(__file__))
    if args.cli:
        from cli import menu
        menu()
    else:
        from gui import run_gui
        run_gui()

if __name__=='__main__':
    main()
