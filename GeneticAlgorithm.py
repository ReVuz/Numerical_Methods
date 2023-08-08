import numpy as np
import random

np.set_printoptions(edgeitems = 30 , linewidth = 100000)

print("Genetic algorithm for 0-1 Knapsack Problem")

MaximumWeight    = 100
NumberOfItems    = 30

Probability = 0.4
random.seed(5)

CostVector = np.random.randint(15 , size = NumberOfItems)
WeightVector = np.random.randint(16 , size = NumberOfItems)

print("\nCosts of items\t: ")
print(CostVector)
print("\nWeight of Items\t: ")
print(WeightVector)


InititalGeneration = np.random.choice([1 , 0] , size = (NumberOfItems , NumberOfItems) , p = (Probability , 1 - Probability))
#print("\nInitial Generation\t: ")
#print("\nEach Row represent an individual/chromosome and each colomn represents an item.")
#print(InititalGeneration)


def Fitness(Individual , NOItems , Costs , Weights , MaxWeight) :
    IndividualScore = 0
    IndividualWeight = 0
    for i in range(0 , NOItems) :
        if Individual[i] == 1 :
            IndividualScore = IndividualScore + Costs[i]
            IndividualWeight = IndividualWeight + Weights[i]
    if IndividualWeight > MaxWeight :
        IndividualScore = 0
    return IndividualScore

def CalculateGenerationScore(Generation , NoItems , Costs , Weights , MaxWeight) :
    ScoreVector = np.array([])
    for i in Generation :
        ScoreVector = np.append(ScoreVector , Fitness(
            Individual = i ,
            NOItems = NoItems,
            Costs = Costs,
            Weights = Weights,
            MaxWeight = MaxWeight
            ))
    return ScoreVector

def SelectPair(Scores , Noselections = 2) :
    TotalScore = np.sum(Scores**2)
    l = [i for i in range(0 , len(Scores))]
    ProbabilityVector = (Scores**2) / TotalScore
    #print(ProbabilityVector)
    Choice = np.random.choice(l , p = ProbabilityVector , size = Noselections , replace = False)
    return Choice


def CrossGenes(Individual1 , Individual2 , Crosslength , NOItems) :
    Slice = np.random.randint(0 , NOItems - Crosslength)
    Child1 = Individual1
    Child2 = Individual2
    for i in range(Slice , Slice + Crosslength) :
        temp = Child1[i]
        Child1[i] = Child2[i]
        Child2[i] = temp
    return Child1 , Child2

def GeneticCycle(Generation , NoItems , Costs , Weights , MaxWeight) :
    GenerationScore = CalculateGenerationScore(Generation , NoItems , Costs , Weights , MaxWeight)
    LuckyPair = SelectPair(GenerationScore , 3)
    Lucky1 = Generation[LuckyPair[0]]
    NewGeneration = Lucky1
    for i in range(int(np.floor((NoItems - 2) / 2))) :
        CrossPair = SelectPair(GenerationScore)
        Individual1 = Generation[CrossPair[0]]
        Individual2 = Generation[CrossPair[1]]
        Child1 , Child2 = CrossGenes(Individual1 , Individual2 , Crosslength = 5 , NOItems = NoItems)
        NewGeneration = np.vstack((NewGeneration , Child1))
        NewGeneration = np.vstack((NewGeneration , Child2))

    Lucky2 = Generation[LuckyPair[1]]
    Lucky3 = Generation[LuckyPair[2]]
    NewGeneration = np.vstack((NewGeneration , Lucky1))
    NewGeneration = np.vstack((NewGeneration , Lucky2))
    if NewGeneration.shape[0] < NoItems * NoItems :
        NewGeneration = np.vstack((NewGeneration , Lucky3))

    NewGeneration = Mutate(Generation = NewGeneration , ChromosomeLength = NoItems)

    return NewGeneration 



def GeneticEra(Initial , NOitems , CostVec , WeightVec , MaximumW , cycles = 2) :
    Generation = Initial
    GenerationScore = CalculateGenerationScore(Generation , NOitems , CostVec , WeightVec , MaximumW)
    for i in range(cycles) :
        print("\nGeneration\t: ", i + 1 )
        printGeneration(Generation = Generation , Scores = GenerationScore)
        Generation = GeneticCycle(Generation = InititalGeneration , Costs = CostVec , Weights = WeightVec , MaxWeight = MaximumW, NoItems = NOitems)
        GenerationScore = CalculateGenerationScore(Generation , NOitems , CostVec , WeightVec , MaximumW)


def Mutate(Generation, ChromosomeLength) :
    Mutations = int(ChromosomeLength / 2)
    for i in range(Mutations) :
        GeneX = random.randint(0 , ChromosomeLength - 1)
        GeneY = random.randint(0 , ChromosomeLength - 1)
        Generation[GeneX][GeneY] = abs(Generation[GeneX][GeneY] - 1)
    return Generation


def printGeneration(Generation , Scores) :
    size = Generation.shape[0]
    print("\nIndividuals\t\t\t\t\t\t\t : Scores\n")
    for i in range(size) :
        print(Generation[i] , "\t :" , Scores[i])

GeneticEra(Initial = InititalGeneration , NOitems = NumberOfItems , CostVec = CostVector , WeightVec = WeightVector , MaximumW = MaximumWeight , cycles = 15)




#        print("Selected Individuals\t: ")
#        print(Individual1)
#        print("Score\t: " , end = '')
#        print(GenerationScore[CrossPair[0]])
#        print(Individual2)
#        print("Score\t: " , end = '')
#        print(GenerationScore[CrossPair[1]])