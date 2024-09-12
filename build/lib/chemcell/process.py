class Chemcellprocess:
    
    #The purpose of this? Well it is meant to get the count of headers to prepare the data to be conformed into a csv
    def Get_Logistics(React_c, Prod_c, C_P, Pc_P):
        header_c = ['Reactant_Count', 'Product_Count']
        Chemeo_Prop = C_P
        Pubchem_Prop = Pc_P
        Props = Chemeo_Prop + Pubchem_Prop
        for i in range(React_c):
            header_c.append(f"Reactant_Name_{i+1}")
            header_c.append(f"Reactant_ID_{i+1}")
            header_c += Props
        
        for i in range(Prod_c):
            header_c.append(f"Product_Name_{i+1}")
            header_c.append(f"Product_ID_{i+1}")
            header_c += Props
        
        return(header_c)