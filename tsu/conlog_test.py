from conlog import Conlog

import inspect


class Timetools:
    @Conlog.fn
    def wait(self, console, s):

        console.debug(r'{s=}')
        print("waiting")

    @Conlog.fn
    def retry(self, console, n):
        console.debug(r'{n=}')
        print("rettrun")

    @Conlog.fn
    def sleep(self, console, secs, minutes):
        print("I am Sleeping")
        console.debug(r' =>  {secs=} {minutes=}')


console = Conlog(Conlog.DEBUG, enabled=True)




def main(arg):
    ## Factory function
    timetools = console.impl(Timetools, Conlog.DEBUG, enabled=True)
    timetools.wait(5)
    timetools.retry(9)
    timetools.sleep(4, 5)


main(5)
