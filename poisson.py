from matplotlib import pyplot as plt
import random
import math


class Spread():
    def __init__(self, graph):
        self.graph = graph

    def reset(self):
        self.graph.cla()
        self.graph.set_xlim(0, 10000)
        self.graph.set_ylim(-1, 1)

    def plot_data(self, data):
        self.reset()
        # x axis: data
        # y axis: [0, 0, 0 ..., 0, 0, 0] with len(data) 0's
        self.graph.plot(data, [0 for i in range(len(data))], "|r")

    def annotate(self, total, average, probability):
        self.graph.annotate(f"Average: {average}", (200, 0.6))
        self.graph.annotate(f"Successes: {total}", (200, 0.5))
        self.graph.annotate(f"Probability: {probability}", (200, 0.4))


class CurrentProbability():
    def __init__(self, graph, probability_function, rate, y_axis):
        self.graph = graph
        self.graph.set_xlim(0, 40)
        self.graph.set_ylim(0, y_axis)

        # generates graph 2 using Calc.getProbability
        for i in range(0, 41):
            probability = probability_function(i, rate)
            self.graph.plot(i, probability, "k.")

    def placeMarker(self, x, y):
        return (self.graph.plot(x, y, "bo"), self.annotate(x, y))

    def removeMarker(self, marker):
        # TODO: figure out what the hell i managed to do here
        # how is the point object structured? why do the handle identifiers contain f"line{x}"?
        for handle in marker:
            handle.remove()

    def annotate(self, x, y):
        return self.graph.annotate(str(round(y, 3)), (x, y+0.05))


class TotalProbability():
    def __init__(self, graph, y_axis):
        self.graph = graph
        self.y_axis = y_axis

    def reset(self):
        self.graph.cla()
        self.graph.set_xlim(0, 40)
        self.graph.set_ylim(0, self.y_axis)

    def plot_subtotals(self, subtotals, iterations):
        self.reset()
        for index in range(len(subtotals)):
            # for each subtotal value, plot with height = total occurances / total cycles
            self.graph.bar(index, subtotals[index] / iterations, 1)


class Calc:
    def getProbability(target, rate):
        # finding   P(X=x) = rate^x * e^-rate / rate!   where target represents x
        return (rate ** target) * math.exp(-rate) / math.factorial(target)

    def generateData(n, rate):
        successes = []
        for m in range(n):
            # if random number (32-bit float from 0-1) less than the rate (per n m's)
            if random.random() < rate / n:
                # add m+1 (the trial number; the range() method iterates from 0 to n-1) to the successes list
                successes.append(m + 1)

        return successes


# * variables to mess with
rate = 20
speed = 1
y_axis = 0.5

print("this is here so you can stop the program\n\nwithout it, it would continue to run\nbecause its main process isn't terminated by closing the interface")

# divide canvas into 1 by 3 sections
fig, subplots = plt.subplots(1, 3)

# canvas formatting (to make it look nicer)
fig.canvas.window().statusBar().setVisible(False)
plt.get_current_fig_manager().full_screen_toggle()

# creating graph objects
s = Spread(subplots[0])
c = CurrentProbability(subplots[1], Calc.getProbability, rate, y_axis)
t = TotalProbability(subplots[2], y_axis)


def cycle(speed=1, total=0, iterations=1):
    data = Calc.generateData(10000, rate)

    s.plot_data(data)

    subtotal = len(data)
    probability = Calc.getProbability(subtotal, rate)

    s.annotate(subtotal, (total + subtotal) // iterations, probability)

    point, annotation = c.placeMarker(subtotal, probability)
    plt.pause(speed)
    c.removeMarker(point)
    annotation.remove()

    return subtotal


total = 0
i = 1
subtotals = [0 for i in range(40+1)]

while True:
    subtotal = cycle(speed, total, i)
    total += subtotal

    # separate because there's no point passing subtotals in and out of the function every call
    if subtotal <= 40:
        subtotals[subtotal] += 1
    t.plot_subtotals(subtotals, i)

    i += 1
