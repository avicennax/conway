# Conway's Game of Life

## Setup

### Requirements

I've provided a `requirements.txt` file to install the dependencies - feel free to use the Python environment management tool of your choice (e.g: virtualenv, pipenv, poetry, etc.)
If you're new to [Python](https://www.python.org/downloads/) and want to get up and running quickly and if you don't mind poluting your global python installation, run:

```bash
# might be `pip3` depending on env.
pip install -r requirements.txt
```

## Running

I've deviated slightly from the prompt to produce a simpler interface; the input is specified via filepath rather than via stdin. An example execution:

```bash
./game_of_life.py -f sample.gol
```

By default the script will run for 10 iterations, but this is configurable via `-k` option. Run `./game_of_life.py --help` for details.
