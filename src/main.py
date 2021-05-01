import knapsack, oneplusone, csv
from collections import namedtuple
from knapsack import Knapsack
from ea import CHEBYSHEV, CHERNOFF
from oneplusone import OnePlusOne
from gsemo import GSEMO

Parameter = namedtuple('Parameter',['name', "desc",'is_int','single_value','value', "min_value", "max_value"])
outputfilepath = '..\\output\\test1.csv'

data_files = {
    'bou-s-c':'instances\\bou-s-c_01.ttp',
    'uncorr':'instances\\uncorr_01.ttp'}

parameters = {"alpha" : Parameter ("alpha", "Default alpha", False, False, [0.0001,0.001,0.01], 0, 1),
              "delta" : Parameter ("delta", "Default delta", False, False, [25, 50], 0, 100),
              "test_loops" : Parameter ("test_loops", "Default no of iterations", True, True, 30, 1, 30),
              "fitness_evaluations" : Parameter ("fitness_evaluations","Default no of fitness evaluations", True, True, 100000, 1000, 100000 )}

def test(algo, alpha, delta, test_loops, fitness_evaluations, method):
    P1 = 0
    P2 = 0
   
    if(method != 2):
        i = 0
        while i < test_loops:
            i += 1
            p1= algo.run(alpha, delta, fitness_evaluations, CHEBYSHEV)
            P1 += p1
            #print("Iteration ", i, " (Chebyshev) : ", p1)
            
    if(method != 1):
        i = 0
        while i < test_loops:
            i += 1
            p2 = algo.run(alpha, delta, fitness_evaluations, CHERNOFF)
            #print("Iteration ", i, " (Chernoff): ", p2)
            P2 += p2
    P1 /= test_loops
    P2 /= test_loops
    return [round(P1,2),round(P2,2)]

def main():
    trials = []
    instances = []
    for file_name in data_files:
        print("Loading instance : ", file_name)
        option = input("\tContinue (1) or skip (2) ? ")
        if int(option) == 2:
            continue
        instances += knapsack.load(data_files[file_name], label = file_name)
    if len(instances) == 0:
        print("0 instances are loaded.")
        return

    ## show user the default parameter values, and let them override if required    
    alpha_params = param_menu(parameters["alpha"], True)
    delta_params = param_menu(parameters["delta"], True)
    test_loops = param_menu(parameters["test_loops"], True)
    fitness_evaluations = param_menu(parameters["fitness_evaluations"], True)


    method = int(input("\nSelect method(s) for probability calculations ... \nChebyshev(1) | Chernoff(2) | Both (3) : "))
    algo = int (input("\nSelect algorithm(s) ... \nOne Plus One(1) | GSEMO (2) : "))
    for instance in instances:
        for alpha in alpha_params:
            for delta in delta_params:
                if(algo == 1):
                    algo_obj = OnePlusOne(instance)
                else:
                    algo_obj = GSEMO(instance)
                [cheby, chern] = test(algo_obj, alpha, delta, test_loops, fitness_evaluations, method)
                trials.append([instance.label,instance.bound,alpha, delta, chern,cheby])
                print(trials[len(trials)-1])
    writeOutput(trials)
    input("Press enter to exit ")
    
def param_menu(param:Parameter, show_override_menu = False):
    print(param.desc, " : " , param.value)
    if (show_override_menu):
        option = input("\tUse default values (1) or override  (2) ? ")
        if int(option) == 2:
            if(param.single_value):
                print("\tEnter a value between ", param.min_value, " and ", param.max_value, " : ", end = "")
                options = int(input(""))
                if options < param.min_value or options > param.max_value:
                    print("\tInvalid input!!!\n\tContinuing with default value.")
                    return param.value
                else:
                    return options ## passed to int
            else:
                options = input("\tEnter space seperated values and press enter :  ")
                arr = options.split()
                params = []
                for opt in arr:
                    params.append(float(opt))
                return params
    return param.value
         
def writeOutput(trials):
    # trials are written in to the outputfilepath
    with open(outputfilepath, 'w', newline='') as outputfile:
        outputwriter = csv.writer(outputfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        outputwriter.writerow(['Instance','Alpha','Delta','Chernoff','Chebyshev'])
        for trial in trials:
            outputwriter.writerow(trial)

#invoke the main function
main()
