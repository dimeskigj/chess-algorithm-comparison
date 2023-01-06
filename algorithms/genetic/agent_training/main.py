from fitness import *
import genetic_algo
import eval_network
import joblib

eval_model = eval_network.simple_eval()
tourno_fitness = fitness

ga = genetic_algo.genetic_algorithm()
agent, loss = ga.execute(tourno_fitness, eval_model, pop_size = 8, generations = 8)
print(agent.fitness)

path = 'genetic_agent.joblib'
joblib.dump(agent, path)
