import argparse
import sys
import ridepicker

class UserShell:
    def __init__(self, config):
        self.config = config
        self.running = True
        
    def process_command(self, command_line):
        if not command_line.strip():
            return
            
        parts = command_line.strip().split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command in ['q', 'quit', 'exit']:
            self.running = False
            print("Bye for now!")    
        elif command == 'run':
            self.exec_run()  
        elif command == 'help':
            self.show_help()  
        elif command == 'status':
            self.show_status()
        elif command in ['config', 'start', 'end', 'age', 'height', 'categories']:
            self.set_config(args)
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
            
    def show_help(self):
        print("\n Available commands: \n")
        print("  help          - Show this help message")
        print("  run           - To run current configuration")
        print("  status        - Show current configuration")
        print("  start/end/age/height/categories   - Add parameters to user shell")
        print("  exit/quit/q   - Exit the shell")
        print()

    def exec_run(self):
        ride_data = ridepicker.read_data()
        ridepicker.run_algo(self.config, ride_data)

    def show_status(self):
        print("\nCurrent Configuration:")
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        print()
        
    def set_config(self, args):
        print(args)
        if len(args) < 2:
            print("Usage: set <key> <value>")
            return
        key, value = args[0], ' '.join(args[1:])
        self.config[key] = value
        print(f"Set {key} = {value}")
        
    def get_config(self, args):
        if not args:
            print("Usage: get <key>")
            return
        key = args[0]
        value = self.config.get(key, "Not found")
        print(f"{key} = {value}")
        
    def run(self):
        print(f"User Shell Started")
        print(f"Mode: {self.config.get('mode', 'default')}")
        if self.config.get('verbose', False):
            print("Verbose mode: ON")
        print("Type 'help' for commands or 'exit' to quit.\n")
        
        while self.running:
            try:
                mode = self.config.get('mode', 'default')
                prompt = f"[{mode}] >>> "
                user_input = input(prompt)
                
                if self.config.get('verbose', False):
                    print(f"DEBUG: Processing command: '{user_input}'")
                self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting on Ctrl+C...")
                break
            except EOFError:
                print("\n\nExiting on EOF...")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Ride picker command-line configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        python main.py -s 10:00:AM -e 8:00:PM -a 8 -h 50 -c=['Train Ride', 'Spinning']
        python main.py --help
                """
    )
    #Flags
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-s', '--start',
        type=str,
        default='8:00AM',
        help='Set the start time of entry to park HH:MMAM'
    )

    parser.add_argument(
        '-e', '--end',
        type=str,
        default='12:00AM',
        help='Set the end time of entry to park as HH:MMAM'
    )
    
    parser.add_argument(
        '-a', '--age',
        type=int,
        default=5,
        help='Set the user age in round years'
    )

    parser.add_argument(
        '-ht', '--height',
        type=int,
        default=50,
        help='Set the user height in cm (Preference for kids)'
    )

    parser.add_argument(
        '-p', '--preference',
        type=str,
        default='maximize_rides',
        choices=['maximize_rides', 'popularity'],
        help='Set the preference for ride itienary. maximize_rides: max rides that can be covered in duration visiting park. popularity: based on ride score picked by algorithm'
    )

    parser.add_argument(
        '-c', '--categories',
        type=str,
        default=[],
        nargs='*',
        choices=['Transportation', 'Thrill Ride', 'Boat Ride', 'Dark Ride', 'Flume Ride','Roller Coaster','Simulator','Driving','Interactive','Spinning','Carousel','Train Ride'],
        help='Set the ride categories (default: any), set as -c Boat Ride Dark Ride'
    )
    
    try:
        args = parser.parse_args()
    except SystemExit:
        return
    
    config = {
        'verbose': args.verbose,
        'start': args.start,
        'end': args.end,
        'age': args.age,
        'height': args.height,
        'categories': args.categories
    }
    
    if args.verbose:
        print("Starting with configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    shell = UserShell(config)
    shell.run()

if __name__ == "__main__":
    main()
