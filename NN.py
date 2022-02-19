import numpy as np
import pickle


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def weights_to_vector(w):
    return w.reshape(1, -1).flatten()


def weights_to_matrix(w, shape):
    return w.reshape(*shape)


class NN:
    def __init__(self, pop_size, parents_num, mutation_rate):
        self.pop_size = pop_size
        self.parents_num = parents_num
        self.mutation_rate = mutation_rate

        self.pop_params = []
        for p in range(self.pop_size):
            pars = {"w1": np.random.randn(50, 3) * 0.01,
                    "w2": np.random.randn(100, 50) * 0.01,
                    "w3": np.random.randn(100, 100) * 0.01,
                    "w4": np.random.randn(1, 100) * 0.01}
            self.pop_params.append(pars)

        self.fitness = [0 for _ in range(self.pop_size)]

    def load_pop(self, src):
        pop = pickle.load(open(src, "rb"))
        self.pop_params[0] = pop

    def reset_fitness(self):
        self.fitness = [0 for _ in range(self.pop_size)]

    def forward_prop(self, x, i):
        params = self.pop_params[i]

        z1 = params["w1"]@x
        a1 = np.tanh(z1)
        z2 = params["w2"]@a1
        a2 = np.tanh(z2)
        z3 = params["w3"]@a2
        a3 = np.tanh(z3)
        z4 = params["w4"]@a3
        a4 = sigmoid(z4)

        return (np.squeeze(a4) > 0.5) * 1

    def parents_selection(self):
        max_fitness = sorted(self.fitness, reverse=True)[:self.parents_num]
        return [self.pop_params[self.fitness.index(f)] for f in max_fitness]

    def offsprings_creation(self, parents):
        offsprings = []
        for i in range(self.pop_size - self.parents_num):
            p1 = parents[i % self.parents_num]
            p2 = parents[(i+1) % self.parents_num]

            pars = {}
            for k in p1.keys():
                w1 = weights_to_vector(p1[k])
                w2 = weights_to_vector(p2[k])
                mid = w1.shape[0]//2
                pars[k] = np.zeros(w1.shape[0])
                pars[k][:mid] = w1[:mid]
                pars[k][mid:] = w2[mid:]
            offsprings.append(pars)

        return offsprings

    def offsprings_mutation(self, offsprings):
        for o in offsprings:
            for k, v in o.items():
                mutation_num = int(v.shape[0] * self.mutation_rate)
                mutation_indices = np.random.randint(0, v.shape[0] - 1, mutation_num)
                o[k][mutation_indices] += np.random.uniform(-1, 1)

        return offsprings

    def optimize(self):
        parents = self.parents_selection()
        offsprings = self.offsprings_creation(parents)
        offsprings = self.offsprings_mutation(offsprings)

        params = self.pop_params[0]
        for o in offsprings:
            for k, v in o.items():
                o[k] = weights_to_matrix(v, params[k].shape)

        self.pop_params = parents + offsprings
        self.reset_fitness()

    def save_best(self):
        idx = self.fitness.index(max(self.fitness))
        pickle.dump(self.pop_params[idx], open("best.data", "wb"))

