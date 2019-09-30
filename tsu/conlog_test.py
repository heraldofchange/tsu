from conlog import Conlog


@Conlog.module
class Timetools:
    def wait(console, s):
        console.debug(f's={s}')
        print("waiting")

    def retry(console, n):
        print("rettrun")
        console.debug(f'=n={n}')


console = Conlog(Conlog.Debug, enabled=True)

timetools = Timetools(conlog=Conlog.DEBUG)


def main(arg):
    timetools.wait(5)
    timetools.retry(5)


main(5)
