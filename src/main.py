from aiza import Aiza


config = {
        'ai': {'model': 'GPT'},
        'you': {'sources': {'google'}}
        }


def main():
    aiza = Aiza(config)
    aiza.learn_user()
    aiza.start()


if __name__ == '__main__':
    main()
