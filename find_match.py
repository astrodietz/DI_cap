def match(productA,max_price,include,exclude):

    #load all the important stuff
    import dill
    import pandas as pd
    import difflib
    import math as m

    #returned variables
    found=False
    return_string=""

    #load product database
    product_file='/home/astrodietz/mysite/ulta_products_CLEAN.pkd'
    data=dill.load(open(product_file, 'rb'))
    product_db = pd.DataFrame(data, columns = ['name','category','price','ingredients'])

    #formatting
    productA=productA.lower()
    product_db['name'] = [name.lower() for name in product_db['name']]
    product_list=list(product_db['name'])

    #if product not found, suggest similar product names, ask user to re-enter input
    if(productA not in product_list):

        #suggestions for similar product names
        similar=difflib.get_close_matches(productA,product_list)
        contains=[product_list[i] for i in range(0,len(product_list)) if productA in product_list[i]]

        if((len(similar)>0) or (len(contains)>0)):
            return_string+= 'product not found, did you mean:<br>'
            suggestions=list(set(similar)|set(contains))[:10] #give 10 unique suggestions
            for item in suggestions:
                return_string+=  '<br>{}'.format(item)
        else:
            return_string+=  'sorry, no matching products found'

        return_string+=  ''

    else: #get product reccomendations

        found=True
        indexA=[index for index,value in enumerate(product_list) if value==productA][0]

        #format ingredients list
        try:
            listA = product_db['ingredients'].loc[indexA].split(', ')
        except Exception:
            listA=['invalidA']

        listA=[ingr.lower() for ingr in listA]

        #print queried product info
        price=product_db['price'].loc[indexA].strip('Price')
        return_string+='your chosen product: {} ({})<br><br>'.format(productA,price)
        return_string+='ingredients:<br>'
        return_string+=", ".join(listA)
        return_string+='<br>'

        #find 3 most similar products, based on ingredients

        match_score=[0 for val in product_list] #keep track of "best" reccomendations

        for indexB, productB in enumerate(product_list):

            #format ingredients list
            try:
                listB=product_db['ingredients'].loc[indexB].split(', ')
            except:
                listB=['invalidB']

            listB=[ingr.lower() for ingr in listB]

            try:
                priceB=float(product_db['price'].loc[indexB].strip('$'))
            except Exception:
                priceB=None

            score=0

            self_check=(productA!=productB) and (productA not in productB) and (productB not in productA) #make sure productA!=productB
            prod_type=(product_db['category'].loc[indexA]==product_db['category'].loc[indexB]) #compare within same category
            optionals=(max_price is None or max_price>=priceB) and \
                      (include is None or all(elem in listB for elem in include)) and \
                      (exclude is None or len(list(set(exclude) & set(listB)))==0) #check optional params

            if(self_check and prod_type and optionals): #does product meet prerequisites?
                #ingredients at top of list should contribute more
                #use exponentially decaying weights
                weights=[m.exp(-10*float(iA)/float(len(listA))) for iA in range(0,len(listA))]
                for iA,ingrA in enumerate(listA):
                    for iB,ingrB in enumerate(listB):
                        if(ingrA==ingrB): #ingredient match!
                            #calculate weight based on list order
                            #normalize indices
                            norm_iA=float(iA)/float(len(listA))
                            norm_iB=float(iB)/float(len(listB))
                            #get (scaled) distance between ingredients
                            dist=abs(norm_iA-norm_iB) #range 0-1
                            #calculate score increase
                            score+=(1.-dist)*weights[iA]

                norm_factor=float(sum(weights))
                score=score/norm_factor
            match_score[indexB]=score

        #do matches exist?
        if(sum(match_score)>0):

            top_scores=sorted(match_score,reverse=True)[0:3]
            top_indices=[i for i,val in enumerate(match_score) if val in top_scores]

            #print top 3 matches + prices, ingredients
            return_string+='<br>top match(es):<br>'
            for index in top_indices:
                price=product_db['price'].loc[index]
                return_string+='<br>{} ({})<br>'.format(product_list[index],price)

                ingr_list = product_db['ingredients'].loc[index].split(', ')
                ingr_list=[ingr.lower() for ingr in ingr_list]

                for ingr in ingr_list: #bold shared ingredients
                    if(ingr==ingr_list[0]):
                        if(ingr in (set(listA) & set(ingr_list))):
                            return_string+=("<b>{}</b>".format(ingr))
                        else:
                            return_string+=("{}".format(ingr))
                    else:
                        if(ingr in (set(listA) & set(ingr_list))):
                            return_string+=("<b>, {}</b>".format(ingr))
                        else:
                            return_string+=(", {}".format(ingr))
                return_string+='<br>'
        else: #no matches exist
            return_string+='no matches found'

    return [found,return_string]