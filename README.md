<div align="center">

<h1>Ride Picker</h1>

### :space_invader: 

<details>
  <summary>Language</summary>
  <ul>
    <li><a href="https://www.python.org/downloads/release/python-3134/">Python 3.13.2</a></li>
  </ul>
</details>

<!-- Getting Started -->
## 	:toolbox: Getting Started
Create a virtual env, install requirements, ready to run

<!-- Prerequisites -->
### :bangbang: Prerequisites

This project uses pip as package manager
```bash
pip install -f requirements.txt
```

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/
```

Go to the project directory

```bash
  cd ridepicker
```

Install dependencies

```bash
  pip install -r requirements.txt

```
Starting user interaction shell

```bash
  Example run:
  
  python main.py --start 8:00AM --end 10:00AM --age 10 --height 120 --categories "Transportation" "Boat Ride"

  Available commands: 
  help          - Show this help message
  run           - To run current configuration
  status        - Show current configuration
  start/end/age/height/categories   - Add parameters to user shell
  exit/quit/q   - Exit the shell
```
