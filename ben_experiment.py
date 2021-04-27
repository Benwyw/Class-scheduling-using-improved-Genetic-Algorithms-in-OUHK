# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 06:54:56 2021

@author: User
"""
import ga, copy

#ga.initial_population()
def do_initial_generation():
    init_gen = []
    gen = []

    for i in range(4):
        popu = ga.initial_population()
        init_gen.append(popu)

    return init_gen, gen

# 留2個
def do_fitness(init_gen, gen):
    temp = []
    for popu in init_gen:
        temp.append(ga.fitness(popu))
    for i in range(2):
        if i == 0:
            print("Init Max Fitness = ",max(temp))
        maxFitness = max(temp)
        gen.append(init_gen[temp.index(maxFitness)])
        del init_gen[temp.index(maxFitness)]
        del temp[temp.index(maxFitness)]

    return gen

def do_looping(loopGen):
    for index in range(100):

        if index == 0: #first time
            Gen1 = loopGen[0]
            Gen2 = loopGen[1]
            print("First Time : ")
            print("Gen1",ga.fitness(Gen1))
            print("Gen2",ga.fitness(Gen2))
        else:
            Gen1 = oldBestPopu
            Gen2 = newBestPopu
            print("Not First Time:")
            print("Gen1",ga.fitness(Gen1))
            print("Gen2",ga.fitness(Gen2))
        
        

        #Crossover and Mutation
        workGen1 = copy.deepcopy(Gen1)
        workGen2 = copy.deepcopy(Gen2)
        crossoverPopu = ga.crossover(workGen1,workGen2) # (popu1,popu2)
        #print("After Crossover Gen1",ga.fitness(crossoverPopu[0]))
        #print("After Crossover Gen2",ga.fitness(crossoverPopu[1]))
        afterGen = (ga.mutation(crossoverPopu[0]),ga.mutation(crossoverPopu[1]))

        print("After Mutation Gen1",ga.fitness(afterGen[0]))
        print("After Mutation Gen2",ga.fitness(afterGen[1]))

        print("Special line",ga.fitness(Gen1))
        print("Special line",ga.fitness(Gen2))
        print("Special line",ga.fitness(afterGen[0]))
        print("Special line",ga.fitness(afterGen[1]))

        #Cal fitness of old gen
        if ga.fitness(Gen1) > ga.fitness(Gen2):
            oldBestPopu = Gen1
        else:
            oldBestPopu = Gen2

        print("oldBestPopu",ga.fitness(oldBestPopu))

        #Cal fitness of new gen
        if ga.fitness(afterGen[0]) > ga.fitness(afterGen[1]):
            newBestPopu = afterGen[0]
        else:
            newBestPopu = afterGen[1]

        print("newBestPopu",ga.fitness(newBestPopu))
    return oldBestPopu, newBestPopu

if __name__ == '__main__':
    temp = do_initial_generation()
    BestPopu = do_looping(do_fitness(temp[0], temp[1]))

    print("Finally")
    print(max(ga.fitness(BestPopu[0]), ga.fitness(BestPopu[1])))