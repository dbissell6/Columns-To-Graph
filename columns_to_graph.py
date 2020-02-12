
"""
Created on Wed Feb 12 08:51:52 2020

@author: dab
"""

import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy 



def create_graph(df,co_thres,pval_thres):
    
    ##convert it to correlational matrix
    df_corr = df.corr(method='spearman')
    
    ### Convert it to a networkX graph
    Behave_Graph = nx.from_pandas_adjacency(df_corr) 
    
    
    G = Behave_Graph.copy() 
    ### Initalize a list to track which edges to remove
    remove = []

    ### calculate pval add to edge attribute
    for num in nx.edges(G):
        #pearson_coef, p_value = scipy.stats.pearsonr(df[num[0]],df[num[1]])
        spearman_coef, p_value = scipy.stats.mstats.spearmanr(df[num[0]],df[num[1]])
        G[num[0]][num[1]]['pval'] = p_value

    ### creates list to remove edges below co_thres,pval_thres in G
    for num in nx.edges(G):
        weight = G[num[0]][num[1]]['weight']
        pval = G[num[0]][num[1]]['pval']
        if weight > co_thres or weight < -co_thres and weight != 1.0 :
            pass
            if pval < pval_thres:
               pass
            else:
                remove.append((num[0],num[1]))
                
        else:
            remove.append((num[0],num[1]))
    
    ### uses list to removes edges
    for its in remove:
        t,u = its
        G.remove_edge(t,u)
        
    
    return G
    


def visual_graph(G):
    '''
    '''
    
    pos = nx.spring_layout(G, k=.50,iterations=10) 
    
    edges = G.edges()
    
    ########Use continous color from matplt

    for x,y in edges:
       if G[x][y]['weight'] > .7:
           G[x][y]['color'] = 'purple'
       
       elif G[x][y]['weight'] >= .4 and G[x][y]['weight'] <= .7 :
           G[x][y]['color'] = 'b'
           
       elif G[x][y]['weight'] > 0 and G[x][y]['weight'] <= .4 :
           G[x][y]['color'] = 'g'
       
       elif G[x][y]['weight'] < 0 and G[x][y]['weight'] > -0.4:
           G[x][y]['color'] = 'orange'
        
       elif G[x][y]['weight'] < -.4 and G[x][y]['weight'] > -.7 :
            G[x][y]['color'] = 'red'
       
       elif G[x][y]['weight'] < -.7 :
            G[x][y]['color'] = 't'

    
    colors = [G[u][v]['color'] for u,v in edges]
    weights = [(G[u][v]['weight']*10) for u,v in edges]
    
    
    plt.title('Graph of Correlations')

    nx.draw_networkx(G, pos, edges=edges, edge_color=colors, width=weights, Labels=True)
    ###Create file to export to Gephi
    #nx.write_gexf(G,"Agraph.gexf")