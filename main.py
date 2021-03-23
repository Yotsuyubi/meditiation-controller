from controller import App

try:
    app = App("/dev/tty.MindWaveMobile-SerialPo-1", 'IAC Mindwave')
    app.send_dummy()

except:
    pass
