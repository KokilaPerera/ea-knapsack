import knapsack, oneplusone, csv
outputfilepath = '..\\..\\..\\output\\test1.csv'

data_files = {
    'bou-s-c':'instances\\bou-s-c_01.ttp',
    'uncorr':'instances\\uncorr_01.ttp'}
alpha_params = [0.0001,0.001,0.01]
delta_params = [25,50]

def test(items, b, alpha, delta):
    i = 0
    P1 = 0
    P2 = 0
    test_loops = 30
    #print("Alpha : ",alpha, "Delta : ", delta, " Bound:", b)
    while i < test_loops:
        p1= oneplusone.run(items, b, alpha, delta, oneplusone.CHEBYSHEV)
        p2 = oneplusone.run(items, b, alpha, delta, oneplusone.CHERNOFF)
        P1 += p1
        P2 += p2
        i+=1
    P1 /= test_loops
    P2 /= test_loops
    return [round(P1,2),round(P2,2)]

def main():
    trials = []
    for file_name in data_files:
        [instance,bounds] = knapsack.load(data_files[file_name])
        print(bounds)
        for b in bounds:
            for alpha in alpha_params:
                for delta in delta_params:
                    [cheby, chern] = test(instance, b, alpha, delta)
                    trials.append([file_name,b,alpha, delta, chern,cheby])
                    print(trials[len(trials)-1])
    writeOutput(trials)

def writeOutput(trials):
    # trials are written in to the outputfilepath
    with open(outputfilepath, 'w', newline='') as outputfile:
        outputwriter = csv.writer(outputfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        outputwriter.writerow(['instance','Alpha','Delta','Chernoff','Chebyshev'])
        for trial in trials:
            outputwriter.writerow(trial)
                
    input("Press any key to exit ")

#invoke the main function
main()
