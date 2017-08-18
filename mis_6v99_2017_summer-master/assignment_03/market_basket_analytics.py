from urllib.request import urlopen
#all the products in the cataglog
prd_list = ["P01","P02","P03","P04","P05","P06","P07","P08","P09","P10"]
inputurl = "http://kevincrook.com/utd/market_basket_training.txt"
testurl = "http://kevincrook.com/utd/market_basket_test.txt"

# Calculates the frequencies of 2 item list , 3 item list and 4 item lists and returns back
# the dictionaries with key value pairs
def calculate_freq():
    freq_map_2items = {}
    freq_map_3items = {}
    freq_map_4items = {}
    prd_present = []
    data = urlopen(inputurl)
    for line in data:
        #taking the key value pairs splitting by comma
        temp = line.decode("utf-8").strip().split(',')[1:]
        # finding out all the items present in training
        [prd_present.append(x) for x in temp if x not in prd_present]
        key_search = ",".join(temp)
        # if number of items is 2, put it in 2 item list map
        if(len(temp )== 2):
            if(key_search in freq_map_2items.keys()):
                freq_map_2items[key_search] += 1
            else:
                freq_map_2items[key_search] = 1
        # if number of items is 3, put it in 3 item list map
        elif(len(temp)==3):
            if(key_search in freq_map_3items.keys()):
                freq_map_3items[key_search] += 1
            else:
                freq_map_3items[key_search] = 1
        # if number of items is 4, put it in 4 item list map
        elif(len(temp)==4):
            if(key_search in freq_map_4items.keys()):
                freq_map_4items[key_search] += 1
            else:
                freq_map_4items[key_search] = 1
    return freq_map_2items, freq_map_3items, freq_map_4items ,prd_present

# given a correct map and search key, find best item set that gives highest frequency
def search_best_comb(freq_map, search_key):
    res_key = ""
    res_value = 0
    for k , v in freq_map.items():
        set_key = set(k.split(","))
        if(search_key < set_key):
            if(res_value < v):
                res_value = v
                res_key = set_key
    return res_key, res_value

def test_scoring(freq_map_2items, freq_map_3items, freq_map_4items,prd_not_present):
    final_result_set = {}
    data = urlopen(testurl)
    for line in data:
        temp = line.decode("utf-8").strip().split(',')
        line_number = temp[0]
        keys_to_search = temp[1:]
        # removing items that are not present in training
        keys_to_search = set([x for x in keys_to_search if x not in prd_not_present])
        res_key = {}
        # if test set length is 1, then search only for 2 item set in training
        if(len(keys_to_search) ==1):
            res_key, res_val = search_best_comb(freq_map_2items, keys_to_search)
        # if test set length is 2, then search only for 3 item set in training
        elif(len(keys_to_search)==2):
            res_key, res_val = search_best_comb(freq_map_3items,keys_to_search)
        # if test set length is 3, then search only for 4 item set in training
        elif(len(keys_to_search)==3):
            res_key, res_val = search_best_comb(freq_map_4items,keys_to_search)
        # creates item for recommendation by removing test set items
        final_result_set[line_number] = ",".join([x for x in res_key if x not in keys_to_search])
    return final_result_set
#driver function
if __name__ == '__main__':
    #calls and creates the frequency maps
    freq_map_2items, freq_map_3items, freq_map_4items, prd_present = calculate_freq()
    #find items that are missing in training set
    prd_not_present = [x for x in prd_list if x not in prd_present]
    #calls function to create new recommendations and receives a map with resulting recomendations
    final_result_set = test_scoring(freq_map_2items, freq_map_3items, freq_map_4items, prd_not_present)
    #writing to file with necessary formatting
    fh = open('market_basket_recommendations.txt', 'w', encoding='utf8')
    for key in sorted(final_result_set.keys()):
        print(key + "," + final_result_set[key], file=fh)
    #closing the file
    fh.close()
