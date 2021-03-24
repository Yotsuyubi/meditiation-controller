from controller import App

try:
    app = App("/dev/tty.MindWaveMobile-SerialPo", 'IAC Mindwave')
    app.run()

except:
    pass
