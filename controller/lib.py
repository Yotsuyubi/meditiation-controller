from mindwavepy import Mindwave
import mido
from .utils import log, error, lerp, slide
import time


class App:

    def __init__(self, mindwave_dev, midi_dev):

        self.mindwave = self.connect_mindwave(mindwave_dev)
        self.midi_port = self.connect_midi_port(midi_dev)
        self.ASICs = [None, None]
        self.t = 0
        self.data_for_send = None
        self.updatable = False
        self.maxes = [0]*10


    def connect_mindwave(self, dev):

        try:
            mindwave = Mindwave()
            log("Mindwave", "Mindwave connecting...")
            mindwave.connect(dev)
            log("Mindwave", "Mindwave connected!")
            return mindwave

        except:
            error("Mindwave", "Cannot connect '{}'!".format(dev))
            raise Exception


    def connect_midi_port(self, dev):

        try:
            log("Midi", "Midi connecting...")
            midi_port = mido.open_output(dev)
            log("Midi", "Midi connected!")
            return midi_port

        except:
            error("Midi", "Cannot connect '{}'!".format(dev))
            raise Exception


    def update(self, rate=0.003):
        self.t = self.t + rate
        if self.t > 1:
            self.t = 1
            self.updatable = False


    def reset(self):
        self.t = 0
        self.updatable = True


    def send_raw(self, data):
        msg = mido.Message("control_change", control=100, value=int((data["value"]+1)/2*127))
        self.midi_port.send(msg)


    def send(self, control, data):
        msg = mido.Message("control_change", control=control, value=int(data))
        self.midi_port.send(msg)


    def send_asic(self, data):

        attention = data["attention"] * 127
        meditiation = data["meditiation"] * 127
        delta = data["delta"] * 127
        theta = data["theta"] * 127
        low_aplha = data["low_aplha"] * 127
        high_alpha = data["high_alpha"] * 127
        low_beta = data["low_beta"] * 127
        high_beta = data["high_beta"] * 127
        low_gamma = data["low_gamma"] * 127
        mid_gamma = data["mid_gamma"] * 127

        self.send(101, attention)
        self.send(102, meditiation)
        self.send(103, delta)
        self.send(104, theta)
        self.send(105, low_aplha)
        self.send(106, high_alpha)
        self.send(107, low_beta)
        self.send(108, high_beta)
        self.send(109, low_gamma)
        self.send(110, mid_gamma)


    def send_dummy(self):

        log("App", "Send dummy...")

        self.send_raw({"value": 0})
        self.send_asic({
            "attention": 0,
            "meditiation": 0,
            "delta": 0,
            "theta": 0,
            "low_aplha": 0,
            "high_alpha": 0,
            "low_beta": 0,
            "high_beta": 0,
            "low_gamma": 0,
            "mid_gamma": 0,
        })


    def run(self):

        log("App", "Running... (Ctrl + c to exit.)")

        while True:

            data = self.mindwave.parse()

            # if data and data["type"] == "RAW":
            #     self.send_raw(data)

            if data and data["type"] == "ASIC":
                self.ASICs = slide(self.ASICs, data)
                self.reset()

            if None not in self.ASICs:
                self.data_for_send = self.get_current_asic()

            if self.data_for_send is not None and self.updatable is True:
                self.send_asic(self.data_for_send)

            self.update()


    def get_current_asic(self):

        asics_from = self.ASICs[0]
        asics_to = self.ASICs[1]
        t = self.t

        values = [
            lerp(asics_from["attention"], asics_to["attention"], t),
            lerp(asics_from["meditiation"], asics_to["meditiation"], t),
            lerp(asics_from["ASIC"]["delta"], asics_to["ASIC"]["delta"], t),
            lerp(asics_from["ASIC"]["theta"], asics_to["ASIC"]["theta"], t),
            lerp(asics_from["ASIC"]["low_aplha"], asics_to["ASIC"]["low_aplha"], t),
            lerp(asics_from["ASIC"]["high_alpha"], asics_to["ASIC"]["high_alpha"], t),
            lerp(asics_from["ASIC"]["low_beta"], asics_to["ASIC"]["low_beta"], t),
            lerp(asics_from["ASIC"]["high_beta"], asics_to["ASIC"]["high_beta"], t),
            lerp(asics_from["ASIC"]["low_gamma"], asics_to["ASIC"]["low_gamma"], t),
            lerp(asics_from["ASIC"]["mid_gamma"], asics_to["ASIC"]["mid_gamma"], t),
        ]

        for i in range(len(values)):

            if self.maxes[i] < values[i]:
                self.maxes[i] = values[i]

            if self.maxes[i] != 0.0:
                values[i] = values[i] / self.maxes[i]


        return {
            "attention": values[0],
            "meditiation": values[1],
            "delta": values[2],
            "theta": values[3],
            "low_aplha": values[4],
            "high_alpha": values[5],
            "low_beta": values[6],
            "high_beta": values[7],
            "low_gamma": values[8],
            "mid_gamma": values[9],
        }
