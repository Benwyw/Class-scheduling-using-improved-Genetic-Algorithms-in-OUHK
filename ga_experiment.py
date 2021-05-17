# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 06:54:56 2021

@author: User
"""
import ga
import copy
from bottle import request, route, run, template, static_file

global ole_Gen_schedule
ole_Gen_schedule = []
global final_schedule
final_schedule = []
global final_schedule_2
final_schedule_2 = []
global ole_Gen_schedule_fitness
ole_Gen_schedule_fitness = 0
global final_schedule_fitness
final_schedule_fitness = 0
global final_schedule_fitness_2
final_schedule_fitness_2 = 0



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/display')
def display():
    global ole_Gen_schedule
    global final_schedule
    output = template('display', oldGen=ole_Gen_schedule,final=final_schedule,secondGen=final_schedule_2,ole_fitness=ole_Gen_schedule_fitness,final_fitness=final_schedule_fitness,secondGen_fitness=final_schedule_fitness_2)
    return output
    

def init():
    #ga.initial_population()
    init_gen = []
    gen = []

    for i in range(4):
        popu = ga.initial_population()
        init_gen.append(popu)

    # 留2個
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


if __name__ == '__main__':
    loopGen = init() # 2 gen
    ole_Gen_schedule = copy.deepcopy(loopGen[0])
    ole_Gen_schedule_fitness = ga.fitness(copy.deepcopy(ole_Gen_schedule))
    count = 1
    
    #while (ga.fitness(copy.deepcopy(loopGen[0])) <= ole_Gen_schedule_fitness):
    while(ga.fitness(copy.deepcopy(loopGen[0])) < 300 ):
        #if count > 100:
            #break
        #if count > 1:
            #break
        if ga.fitness(copy.deepcopy(loopGen[1])) > 300 and count > 1:
            break
        newGen = []

        print("Old Gen:")
        oldGenFitness = []
        for popu in loopGen:
            oldGenFitness.append(ga.fitness(popu))
        maxOldGenIndex = oldGenFitness.index(max(oldGenFitness))
        newGen.append(loopGen[maxOldGenIndex])
        print(ga.fitness(loopGen[0]))
        print(ga.fitness(loopGen[1]))

        loopGen2 = copy.deepcopy(loopGen)
        crossoverGen = ga.crossover(loopGen2[0],loopGen2[1])

        mutationGen = []
        crossoverGen2 = copy.deepcopy(crossoverGen)
        for crossoverPopu in crossoverGen2:
            #mutationGen.append(ga.mutation_1(copy.deepcopy(ga.mutation(crossoverPopu))))
            temp = ga.mutation(crossoverPopu)
            mutationGen.append(temp)
            #mutationGen.append(ga.mutation_1(temp))
            
        print("Mutation:")
        print(ga.fitness(mutationGen[0]))
        print(ga.fitness(mutationGen[1]))
        print()
        mutationFitness = []
        for mutationPopu in mutationGen:
            mutationFitness.append(ga.fitness(mutationPopu))
        maxMutationGenIndex = mutationFitness.index(max(mutationFitness))
        newGen.append(mutationGen[maxMutationGenIndex])
        print("NewGen:")
        for i in newGen:
             print(ga.fitness(i))
        print("==================================================={}".format(count))
        count += 1
        loopGen = copy.deepcopy(newGen)
    
    finalFitness = []
    for popu in loopGen:
        finalFitness.append(ga.fitness(popu))
    finalGenIndex = finalFitness.index(max(finalFitness))
    print("Final:")
    print(ga.fitness(loopGen[finalGenIndex]))
    print("===================================================")
    print()
    secondIndex = 0
    if finalGenIndex == 0:
        secondIndex = 1
    else:
        secondIndex = 0
    #final_schedule = copy.deepcopy(loopGen[finalGenIndex])
    final_schedule = copy.deepcopy(loopGen[finalGenIndex])
    final_schedule_2 = copy.deepcopy(loopGen[secondIndex])
    final_schedule_fitness = ga.fitness(copy.deepcopy(final_schedule))
    final_schedule_fitness_2 = ga.fitness(copy.deepcopy(final_schedule_2))
    run(host='0.0.0.0', port=8080)
        #print(loopGen[finalGenIndex])
        
        


            






    