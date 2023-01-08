# Install PyQT5 on OS X (m1 arch)

    brew install pyqt5
    python -m venv venv
    source venv/bin/activate
    export PATH="/opt/homebrew/opt/qt5/bin/:$PATH"
    yes | pip3 install pyqt5 --config-settings --confirm-license= --verbose

# Compile the qtbytebeat.ui

    pyuic5 -x -o qtbytebeat.py qtbytebeat.ui
