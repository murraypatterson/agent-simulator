from random import random

# in calculating
#----------------------------------------------------------------------

# points for clean squares
def score(a, b) :
    s = 0

    s += 1 if not a else 0
    s += 1 if not b else 0

    return s


# apply penalties for actions
def penalty(old_a, a, old_b, b, old_pos, pos) :

    if old_a and not a : # for cleaning a
        return 1

    if old_b and not b : # for cleaning b
        return 1

    if old_pos + pos == 1 : # for moving
        return 1

    return 0


# square becomes dirty again with probability p
def dirty(a, b, p = 0) :

    if random() < p :
        a = 1
    if random() < p :
        b = 1

    return(a, b)


# in diplaying
#----------------------------------------------------------------------

# textual depiction of current state 
def dep(a, b, pos) :

    print()
    print('  {} {}'.format(' ' if pos else 'o', 'o' if pos else ' '))
    print('[ {} {} ]'.format('x' if a else ' ', 'x' if b else ' '))
    print()


# display initial configuration
def init(a, b, pos) :

    print(70*'-')
    dep(a, b, pos)
    print(70*'-')
    print()


# display a step
def disp(i, a, b, pos, score, total, T, compact = True, final = False) :

    if final : # just the final score
        if i == T - 1 :
            print('total =', total)

        return

    if compact : # compact display
        if i >= 3 and i <= T - 4 :
            return

    print('step', i+1)
    dep(a, b, pos)

    print('score =', score)
    print('total =', total)

    print()
    print('---')
    print()

    if compact : # compact display
        if i == 2 :
            print(' .')
            print(' .')
            print(' .')
            print()


# agents
#----------------------------------------------------------------------

# the reflex agent of the 34th slide of slides ch2
class ReflexAgent :

    def __init__(self, sensor = True) :
        self.sensor = sensor

    def act(self, a, b, pos) :

        if pos : # on square b
            if b : # b is dirty
                return a, 0, pos # clean square b

            else : # b is clean
                if not self.sensor : # if the sensor is broken
                    return a, b, pos # stay
                else :
                    return a, b, 0 # move to square a

        else : # on square a
            if a : # a is dirty
                return 0, b, pos # clean square a
            else :
                return a, b, 1 # move to square b


# the agent which does nothing
class NullAgent :

    def act(self, a, b, pos) :
        return a, b, pos


# an agent which checks other square with some fixed probability
class ProbabilisticAgent :

    def __init__(self, prob = 1.) :
        self.prob = prob
        self.mode = False

    def act(self, a, b, pos) :

        if self.mode : # other square is checked

            if pos : # on square b
                if b : # b is dirty
                    return a, 0, pos # clean square b
                else : # b is clean
                    p = 0 if random() < self.prob else 1
                    return a, b, p # move to square a with prob

            else : # on square a
                if a : # a is dirty
                    return 0, b, pos
                else : # a is clean
                    p = 1 if random() < self.prob else 0
                    return a, b, 1 # move to square b with prob

        else : # just starting out..

            if pos : # on square b
                if b : # b is dirty
                    return a, 0, pos # clean square b
                else : # b is clean
                    self.mode = True # set mode
                    return a, b, 0 # move to square a

            else : # on square a
                if a : # a is dirty
                    return 0, b, pos # clean square a
                else : # a is clean
                    self.mode = True # set mode
                    return a, b, 1 # move to square b


# an agent which checks other square from time to time
class WaitingAgent :

    def __init__(self, wait = 0) :
        self.wait = wait
        self.mode = False
        self.count = 0
        
    def act(self, a, b, pos) :

        if self.mode : # other square is checked

            if pos : # on square b
                if b : # b is dirty
                    return a, 0, pos # clean square b
                else : # b is clean

                    if self.count == self.wait : # waited long enough..
                        self.count = 0
                        return a, b, 0 # move to square a

                    else :
                        self.count += 1
                        return a, b, pos # wait on square b

            else : # on square a
                if a : # a is dirty
                    return 0, b, pos # clean square a
                else : # a is clean

                    if self.count == self.wait : # waited long enough..
                        self.count = 0
                        return a, b, 1 # move to square b

                    else :
                        self.count += 1
                        return a, b, pos # wait on square a

        else : # just starting out..

            if pos : # on square b
                if b : # b is dirty
                    return a, 0, pos # clean square b
                else : # b is clean
                    self.mode = True # set mode
                    return a, b, 0 # move to square a

            else : # on square a
                if a : # a is dirty
                    return 0, b, pos # clean square a
                else : # a is clean
                    self.mode = True # set mode
                    return a, b, 1 # move to square b


# running the entire simulation
#----------------------------------------------------------------------

def simulation(
        T = 100, # number of timesteps
        agent = 'reflex', # choice of agent
        probability = 1., # probability for prob agent
        wait = 0, # how many timesteps to wait for the waiting agent
        pen = True, # whether or not to penalize actions
        dirt = 0., # probablity that a square becomes dirty again
        printing = False, # whether to print or not
) :

    overall = 0
    j = 0
    for a_ in 0, 1 : # squares a and b, dirty (1) or not (0)
        for b_ in 0, 1 :
            for pos_ in 0, 1 : # positions a (0) and b (1)
                total = 0
                a, b, pos = a_, b_, pos_ # initial configuration

                if printing :
                    init(a, b, pos)

                Agent = None
                if agent == 'reflex' :
                    Agent = ReflexAgent()
                elif agent == 'broken' :
                    Agent = ReflexAgent(sensor = False)
                elif agent == 'null' :
                    Agent = NullAgent()
                elif agent == 'prob' :
                    Agent = ProbabilisticAgent(probability)
                elif agent == 'wait' :
                    Agent = WaitingAgent(wait)
                else :
                    assert False, 'Error: unknown agent type'

                for i in range(T) : # run agent for T timesteps
                    old_a = a
                    old_b = b
                    old_pos = pos

                    a, b, pos = Agent.act(a, b, pos)
                    s = score(a,b)
                    p = penalty(old_a, a, old_b, b, old_pos, pos) if pen else 0
                    total += s - p

                    if printing :
                        disp(i, a, b, pos, s - p, total, T, compact = True, final = True)

                    a, b = dirty(a, b, p = dirt) # become dirty with prob p

                overall += total
                j += 1

    expected = overall / j
    if printing :

        print()
        print('---')
        print()
        print('expected performance =', expected)
        print()

    return expected


# running sets of simulations of an agent
def simulations(agent = 'prob', probability = 1., wait = 0, dirt = 0., n = 1000) :

    exps = []
    if agent == 'prob' :
        
        for i in range(n) :
            exp = simulation(agent = 'prob', probability = probability, dirt = dirt)
            exps.append(exp)

    elif agent == 'wait' :

        for i in range(n) :
            exp = simulation(agent = 'wait', wait = wait, dirt = dirt)
            exps.append(exp)

    elif agent == 'reflex' :

        for i in range(n) :
            exp = simulation(agent = 'reflex', dirt = dirt)
            exps.append(exp)

    elif agent == 'broken' :

        for i in range(n) :
            exp = simulation(agent = 'broken', dirt = dirt)
            exps.append(exp)
            
    elif agent == 'null' :

        for i in range(n) :
            exp = simulation(agent = 'null', dirt = dirt)
            exps.append(exp)
            
    else :
        assert False, 'Error: unknown agent type'
            
    return sum(exps) / len(exps)


# perform the bisection method on sets of simulations of an agent in
# order to tune the optimal parameter
def bisection(agent = 'prob', dirt = 0., n = 1000, uw = 20, printing = False) :

    low = None
    upp = None

    if agent == 'prob' :

        low = 0.
        upp = 1.

    elif agent == 'wait' :

        low = 0
        upp = uw

    else :
        assert False, 'Error: unknown agent type'

    while True :

        v_low = None
        v_upp = None

        if agent == 'prob' :

            v_low = simulations(probability = low, dirt = dirt, n = n)
            v_upp = simulations(probability = upp, dirt = dirt, n = n)

            if printing :

                print('p = {}, exp = {}'.format(low, v_low))
                print('p = {}, exp = {}'.format(upp, v_upp))
                print()

            if abs(upp - low) < 0.001 or abs(v_upp - v_low) < 0.001 :
                return upp, v_upp

            bis = abs(upp - low) / 2. # bisector
            if v_low < v_upp :
                low += bis
            else :
                upp -= bis

        # note that this is not really "bisection", but just closing the gap
        elif agent == 'wait' :

            v_low = simulations(agent = 'wait', wait = low, dirt = dirt, n = n)
            v_upp = simulations(agent = 'wait', wait = upp, dirt = dirt, n = n)

            if printing :

                print('k = {}, exp = {}'.format(low, v_low))
                print('k = {}, exp = {}'.format(upp, v_upp))
                print()

            if upp == low :
                return upp, v_upp

            if v_low < v_upp :
                low += 1
            else :
                upp -= 1


# Main
#----------------------------------------------------------------------

print()
print('suppose that actions have no cost:')
print()

exp = simulation(pen = False)
print('  reflex vacuum agent has expected performance =', exp)
print()

print('suppose that each action (move or clean) has cost 1:')
print()

exp = simulation()
print('  reflex vacuum agent has expected performance =', exp)
print()

exp = simulation(agent = 'broken')
print('  reflex agent with a broken sensor has expected performance = ', exp)
print()

exp = simulation(agent = 'null')
print('  agent that does nothing has expected performance =', exp)
print()

c = .1
print('suppose also that each clean square has a 10% chance of becoming dirty again:')
print()

exp = simulations(agent = 'reflex', dirt = c)
print('  reflex vacuum agent has expected performance ~', exp)
print()

exp = simulations(agent = 'broken', dirt = c)
print('  reflex vacuum with a broken sensor has expected performance ~', exp)
print()

exp = simulations(agent = 'null', dirt = c)
print('  agent that does nothing has expected performance ~', exp)
print()

print('  consider agent which checks other square with probability p,')
print('  we tune p with bisection:')
print()

p, v = bisection(dirt = c)
print('  -> it seems to converge to p = {:.3f} (performance = {:.3f})'.format(p,v))
print()

uw = 20
print('  consider agent which checks other square after k time steps,')
print('  we tune k by closing the gap between 0 and {}:'.format(uw))
print()

k, v = bisection(agent = 'wait', dirt = c, uw = uw)
print('  -> it seems to converge to k = {} (performance = {:.3f})'.format(k,v))
print()
