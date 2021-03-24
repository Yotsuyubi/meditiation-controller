from controller import App
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('mindwave', metavar='/path/to/mindwave', type=str,
                    help='path of mindwave serial port')

parser.add_argument('midi', metavar='midi-port', type=str,
                    help='name of midi port')

parser.add_argument('--midi-learn', dest='midi_learn', action='store_const',
                    const=True, default=False,
                    help='send dummy message for midi learn (default: False)')

args = parser.parse_args()


def midi_learn(mindwave, midi):
    try:
        app = App(mindwave, midi)
        app.send_dummy()

    except:
        pass


def run(mindwave, midi):
    try:
        app = App(mindwave, midi)
        app.run()

    except:
        pass

if __name__ == '__main__':

    if args.midi_learn:
        midi_learn(args.mindwave, args.midi)

    else:
        run(args.mindwave, args.midi)
