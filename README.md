# Fidelity Options Performance

Intended to be a little tool to track options trading performance in Fidelity,
addressing their barebones profit/loss reporting.

Will print the gross revenue and gross expense for each symbol you buy/sell
options on, and print the total gross revenue/expense and net gain/loss for all
of your options trading.

Requires no authentication, just needs the CSV files that Fidelity exports.

1. Download Fidelity CSV files from the account Activity tab. You'll have to
   manually get as much data as you want to run the numbers on.
2. For now, you'll need to massage the data into a well-formed CSV. Cut off the
   garbage whitespace and disclaimers at the front and back of the CSV files,
   and make sure there is no leading whitespace at the beginning of each line.
3. Activate your venv (`python3 -m venv venv`)
4. Source the environment (`source venv/bin/activate`)
5. Get your requirements (`pip3 install -r requirements.txt`)
6. Run:

```sh
$ python fidelity_performance.py run data1.csv data2.csv ...
```

## How it works

CLI argument parsing is done with Fire.

Pandas does most of the heavy lifting (CSV parsing, filtering, summing).
