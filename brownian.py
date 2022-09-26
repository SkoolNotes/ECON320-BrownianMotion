import scipy
from random import Random
import math
import statistics

from tqdm import tqdm
import seaborn as sns
from matplotlib import pyplot as plt

from decimal import Decimal,getcontext

# fix a pseudorandom seed
R = Random(7)

# and define a custom function
# f(x) = (\sqrt{x}-1)^2 for now, for fun
# this function has the added advantage
# of not being bounded in values x<0
# and dips into the negative at x>1
f = lambda x: (x**0.5-1)**2

# riemann limits
def problem_1(N):
    # and a sequence x
    # first value is 0
    x = [0]
    # generate N-2 values
    for _ in tqdm(range(N-2)):
        # create random intervals
        # 1/N apart
        x.append(x[-1]+1/N)
    # add 1
    x.append(1)

    # now, let's compute the riemann sum
    Sn_seq = [f(x[i])*(x[i+1]-x[i]) for i in tqdm(range(N-1))]
    Sn = sum(Sn_seq)

    return Sn


# create order of magnitude trials
problem_1_results = []
for i in range(0,8):
    print(f"generating for {i}")
    problem_1_results.append((10**i, problem_1(10**i)))

problem_1_results


# socastic sequence
def socastic_sequence(p, epsilon=0.001, random=R):
    # we start at 0 for a classic
    # Brownian
    X = [0]

    # when, while we are not at 1,
    # we keep trying
    while X[-1] < 1:
        # choose based on probabliity
        # we round not because we want to,
        # but because of gloating point errors
        choice = random.uniform(0,1)
        if choice <= p:
            X.append(round(X[-1] + epsilon,4))
        else:
            X.append(round(X[-1] - epsilon,4))

        print(f"{X[-1]}\r", end="")
    print()

    return X

# problem 2
def problem_2(p,epsilon):
    # we round again here because of
    # floating point shenanigans
    D_expected = round((epsilon*p-epsilon*(1-p)), 10)
    Dsq_expected = round(((epsilon**2)*p-(epsilon**2)*(1-p)), 10)
    D_variance = (Dsq_expected - D_expected**2)

    T_expected = 1/D_expected
    T_variance = 1/D_variance

    return T_expected, T_variance**0.5 

# problem 3
def problem_3(trials, p, epsilon):
    # collect data
    data = [len(socastic_sequence(p, epsilon)) for _ in range(trials)]

    # analyze
    data_mean = sum(data)/len(data)
    data_std = statistics.stdev(data)

    return data_mean, data_std

def problem_4(p, epsilon):
    # get sequence
    seq = socastic_sequence(p, epsilon)

    # calculate quadratics
    quads = []

    for i in range(len(seq)-1):
        quads.append((seq[i+1]-seq[i])**2)

    # return variation
    return sum(quads)

p4_one = problem_4(0.51, 0.1)
p4_two = problem_4(0.51, 0.01)
p4_three = problem_4(0.51, 0.001)

f = lambda x: (x-1)**2

def problem_5(p, epsilon):
    # get sequence
    seq = socastic_sequence(p, epsilon)

    # calculate quadratics
    function_base = []
    function_next = []
    function_mean = []

    for i in range(len(seq)-1):
        diff = (seq[i+1]-seq[i])

        function_base.append(f(seq[i])*diff)
        function_next.append(f(seq[i+1])*diff)
        function_mean.append(f(diff/2)*diff)

    # return variation
    return sum(function_base), sum(function_next), sum(function_mean)

p5_one = problem_5(0.51, 0.1)
p5_two = problem_5(0.51, 0.01)
p5_three = problem_5(0.51, 0.001)

p5_one
p5_two
p5_three

