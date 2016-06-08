import simpy

def car(env, name, bcs, driving_time, charge_duration):
    yield env.timeout(driving_time)

    print('%s arriving at %d' % (name, env.now))
    #with bcs.request() as req:
    req = bcs.request()
    # print bcs.put_queue, "This is the put queue"
    print bcs.users, "These are the users"
    # print bcs.capacity, "This is the capacity"
    # print bcs.get_queue
    #Need to yield the request so it gets the resource
    yield req
    print req, "This is request"

    print('%s starting to charge at %s' % (name, env.now))
    yield env.timeout(charge_duration)
    print('%s leaving the bcs at %s' % (name, env.now))
    bcs.release(req)


if __name__ == "__main__":
    env = simpy.Environment()
    bcs = simpy.Resource(env, capacity = 2)
    for i in range(4):
        env.process(car(env, 'Car %d' % i, bcs, i*2, 5))
    env.run()

