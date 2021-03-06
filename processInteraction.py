import simpy

class Car(object):
    
    def __init__(self, env):
        self.env = env
        #Start the run function in the process of self.process()
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            try:
                #Interrupt is thrown into the process as exception
                #Therefore it could also interrupt a timeout !!
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                print ('Was interrupted. Hope, the battery is full enough ...')
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, charge_duration):
        yield self.env.timeout(charge_duration)


def driver(env, car):
    yield env.timeout(2)
    print('This driver interrupted the car at time %d' % env.now)
    car.action.interrupt()




if __name__ == "__main__":
    env = simpy.Environment()
    car = Car(env)
    env.process(driver(env, car))
    #any call to env.process will not be started unless we call env.run 
    env.run(until = 15)
    print env.now

