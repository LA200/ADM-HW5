
#RQ1 -----------------------------------------------------------------------------------------------------------

def big_data():
    array=[]
    listassa=[]
    file3 = open('wiki-topcats.txt','r')
    Lines = file3.readlines()
    for line in Lines:
        array=line.strip().split(' ',maxsplit=1)
        array=list(map(int,array))
        listassa.append(array)
    data=pd.DataFrame(listassa)
    data.columns=['edge_a','edge_b']
    return(data)

#RQ2 -----------------------------------------------------------------------------------------------------------

def find_pages(G,source,click):
    node_number=[]
    nome_article=[]
    for node in G.nodes():
        try:
            comparative=nx.shortest_path_length(G, source=source,target=node)
        except nx.NetworkXNoPath:
            comparative=0
        if(comparative==click):
            node_number.append(node)
            nome_article.append(labels[node])
    pages_w_clicks=pd.DataFrame([node_number,nome_article])
    pages_w_clicks=pages_w_clicks.T
    pages_w_clicks.columns=['Node_Number','Article_Name']
    return(pages_w_clicks)

#RQ3 -----------------------------------------------------------------------------------------------------------

def rq3(G, C):
    if C in cate:  # checking if C is a proper category as defined previously

        a = (category_set[category_set.Category == C].Articles).tolist()[0].split()
        for j in range(len(a)):
            a[j] = int(a[j])
        E = G.subgraph(a)  # creating the subgraph corresponding to the category C
        e = list(E.edges)
        n = list(E.nodes)

        if len(e) > 0:
            # create a dictionnary that stores for each article in C the id of the article and the incomming edges
            dic = {}
            for i in range(len(n)):
                dic[n[i]] = []
            for i in range(len(e)):
                temp = e[i][1]
                if temp in dic.keys():
                    dic[e[i][1]].append(e[i][0])
            # print(dic)

            # computation of the in-degree centrality
            maxi = 0
            article = 0
            for i in dic.keys():
                if len(dic[i]) >= maxi:
                    maxi = len(dic[i])
                    article = i

            "following part is just to make sure we are not falling in the computation of the in_degree_center of C"
            # test=nx.in_degree_centrality(H)
            # test={k: v for k, v in sorted(test.items(), key=lambda item: item[1])}
            # t=list(test.keys())[-1]
            # print(article, t)

            # counting the total number of clicks in "path" or print "Not possible" if the subgraph is not connected
            path = 0
            temp = 0
            for i in range(len(n)):
                if (n[i] in dic[article]):
                    path += nx.shortest_path_length(E, source=n[i], target=article)
                elif n[i] != article:
                    temp = 1
                    break
            if temp == 1:
                sol = 'Not possible'
            else:
                sol = str(path)
        else:
            sol = 'Not possible'
    else:
        sol = 'Not possible'

    return sol

#RQ4 -----------------------------------------------------------------------------------------------------------

def SubG(G, C):
    if C in cate:  # checking if C is a proper category as defined previously

        a = (category_set[category_set.Category == C].Articles).tolist()[0].split()
        for j in range(len(a)):
            a[j] = int(a[j])
        E = G.subgraph(a)  # creating the subgraph corresponding to the category C
    return (E)

def rq4(a,b):
    S1=SubG(G,a)
    S2=SubG(G,b)
    Sub=nx.compose(S1,S2)
    return(Sub)

def node_path_to_edges(eu):
    for j in range(0,len(eu)):
        aux=eu[j]
        aux3=[]
        for i in range(0,len(aux)-1):
            aux2=(aux[i],aux[i+1])
            aux3.append(aux2)
            eu[j]=aux3
    return(eu)

def find_same_edges(path1, path2):
    result = False
    for x in path1:
        for y in path2:
            if x == y:
                result = True
                return result
    return result

#RQ5 -----------------------------------------------------------------------------------------------------------

def nodes_from_cat(G, C):
    if C in cate:
        a=(category_set[category_set.Category==C].Articles).tolist()[0].split()
        for j in range(len(a)):
            a[j]=int(a[j])
    return(a)

def rq5(x):
    wes={}
    ref=nodes_from_cat(G,x)
    for k in categorias:
        l=[]
        aux=nodes_from_cat(G,k)
        if(aux!=ref):
            for i in ref:
                if(G.has_node(i)):
                    for j in aux:
                        if(G.has_node(j)):
                            try:
                                val=nx.shortest_path_length(G,i,j)
                                l.append(val)
                            except nx.NetworkXNoPath:
                                pass
        if(len(l)!=0):
            dist=round(sum(l)/len(l),3)
            wes[k]=dist
    dict1 = wes
    return((sorted(dict1.items(), key = lambda kv:(kv[1], kv[0]))) )

#RQ6 -----------------------------------------------------------------------------------------------------------

def df_construction(H):
    n = [i for i in (H.nodes)]
    dic_target = {}  # dic_target[Ni]= stores nodes that are pointing by Ni (Ni is the target)
    dic_source = {}  # dic_source[Ni]=stores nodes nodes that point Ni (Ni is the source)

    for i in n:
        dic_target[i] = []
        dic_source[i] = []

    for j in n:
        for i in H.edges:
            if i[0] == j:
                dic_source[j].append(i[1])
            if i[1] == j:
                dic_target[j].append(i[0])

    l = []
    for i in n:
        l.append([i, dic_target[i], dic_source[i], ])

    df = pd.DataFrame(l, columns=['n_article', 'incoming', 'outgoing'])
    df['PRt0'] = 1.0 / len(
        n)  # construct a dataframe to be able to work properly - initial values of PageRank are the same for every nodes
    df['PRt1'] = 0
    return df


def PRt1_Ni(H, df, Ni, damping_factor):
    n = [i for i in (H.nodes)]
    cst = damping_factor / (len(n))

    inc = df[df.n_article == Ni]['incoming'].tolist()[0]  # look for incoming nodes of the node Ni

    if len(inc) >= 1:  # check if there is no incoming links - if it is true, the value of PR is constant
        dic = {}
        for i in range(len(inc)):
            dic[inc[i]] = len(df[df.n_article == inc[i]]['outgoing'].tolist()[
                                  0])  # stores for each incomming links the nb of outcomming
        sol = 0
        for i in range(len(inc)):
            sol += (df[df.n_article == inc[i]]['PRt0'].values) / (
            dic[inc[i]])  # compute the sum of PRi(t-1)/nb_outgoing(PRi) for i in incoming links
        df.at[df[df.n_article == Ni].index, 'PRt1'] = cst + (1 - damping_factor) * sol[
            0]  # Compute final value of PR(t)

    else:
        df.at[df[df.n_article == Ni].index, 'PRt1'] = cst
    return df

def PR(H,iteration,damping_factor):
    df=df_construction(H)
    n=[i for i in (H.nodes)]
    for j in range(iteration): # The number of iterations for the PR algorithm
        for i in n:
            df=PRt1_Ni(H,df,i,damping_factor)
        df['PRt0']=df['PRt1'] # update current value of PR
        df['PRt1']=0
    df.sort_values('PRt0') # sort page by their PR score
    l=np.arange(1,len(n)+1)
    df['PageRank']=l
    return df #return a sorted df w.r.t PagrRank score
