# serial-monitor-test-python

Quick Python script for reading and printing serial input.

Useful when combined with an Arduino running the [serial-print-test-arduino](../serial-print-test-arduino) program.

## How to use this

You’ll probably want to create a virtualenv to store the Python library we’re about to install:

    cd serial-monitor-test
    virtualenv .
    . bin/activate

Now install the [`pyserial`](https://pythonhosted.org/pyserial/index.html) library:

    pip install -r requirements.txt

And finally run the script:

    ./monitor.py

Exit the program by typing `ctrl`-`C`.

The script assumes a serial port path of `/dev/ttyUSB0`. If yours is different, supply it as an argument:

    ./monitor.py -p /dev/tty.wchusbserial1410

You can see all options by adding `--help`:

    ./monitor.py --help
