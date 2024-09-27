from chemcell import Chemcell

example = Chemcell("HCl", False, "/workspaces/Chemcell/Example_Data").range(0,4).tabulate()

print(example)