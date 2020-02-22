import sys
from json import loads
from re import sub
import csv

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

# ItemSet
ItemSet = {}
ItemCategory = {}
Category = {}
    # Location
Location = {}
    # Country
Country = {} 
BidSet = []
ItemBid = {}
ItemSeller = {}
User = {}

def InitDicts():    
    ItemSet.setdefault('Item_ID',[])
    ItemSet.setdefault('Name',[])
    ItemSet.setdefault('Currently',[])
    ItemSet.setdefault('Buy_Price',[])
    ItemSet.setdefault('First_Bid',[])
    ItemSet.setdefault('Number_of_Bids',[])
    ItemSet.setdefault('Location_ID',[])
    ItemSet.setdefault('Started',[])
    ItemSet.setdefault('Ends',[])
    ItemSet.setdefault('Description',[])
    # Init Category
    ItemCategory.setdefault('Item_ID',[])
    ItemCategory.setdefault('Category_ID',[])
    
    # itemBid
    ItemBid.setdefault('Item_ID',[])
    ItemBid.setdefault('Bid_ID',[])
    
    # ItemSeller
    ItemSeller.setdefault('Item_ID',[])
    ItemSeller.setdefault("Seller_ID",[])
        
    
# Access the location information
def processLocation(loc):
    if "Country" in loc and loc['Country'] not in Country:
        Country[loc['Country']] = len(Country) + 1
    if loc['Location'] not in Location:
        country_id = "NULL" if "Country" not in loc else Country[loc['Country']]
        Location[loc['Location']] = (len(Location) + 1, country_id)

# Aceess the user information
def processUser(use):
    if use['UserID'] not in User:
        element = use['Rating']
        if "Location" not in use:             
            element += "|NULL"
        else:
            element += "|" + str(Location[use['Location']][0])
        User[use['UserID']] = element

# Method to check empty string
def checkEmptyStr(string):
    if string is None or len(string)==0:
        return "NULL"
    return '"'+string.replace('"', '""')+'"'


"""
When parse a jason file, iterate all items in the file and collect information
to build the data file
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']
        global Category
        global Location
        global Country
        global ItemSet
        global ItemCategory
        global BidSet
        global ItemBid
        
        for item in items:
            
            #Category
            for cat in item['Category']:
                if cat not in Category: 
                    Category[cat] = len(Category) + 1
            
            #Location&Country
            processLocation(item)
            if item['Bids']:
                for bid in item['Bids']: 
                    bidder = bid['Bid']['Bidder']
                    if 'Location' in bidder:
                        processLocation(bidder)           
            
            #UserTable
            item['Seller']['Location'] = item['Location']
            processUser(item['Seller'])
            if item['Bids']:
                for bid in item['Bids']: 
                    processUser(bid['Bid']['Bidder'])            
            
            #ItemSet
            ItemSet['Item_ID'].append(item['ItemID'])
            ItemSet['Name'].append(checkEmptyStr(item['Name']))
            ItemSet['Currently'].append(checkEmptyStr(transformDollar(item['Currently'])))
            if 'Buy_Price' in item:
                ItemSet['Buy_Price'].append(transformDollar(item['Buy_Price']))
            else:
                ItemSet['Buy_Price'].append('"0"')
            ItemSet['First_Bid'].append(transformDollar(checkEmptyStr(item['First_Bid'])))
            ItemSet['Number_of_Bids'].append(checkEmptyStr(item['Number_of_Bids']))
            ItemSet['Location_ID'].append(checkEmptyStr(str(Location[item['Location']][0])))
            ItemSet['Started'].append(checkEmptyStr(transformDttm(item['Started'])))
            ItemSet['Ends'].append(checkEmptyStr(transformDttm(item['Ends'])))
            ItemSet['Description'].append(checkEmptyStr(item['Description'])) 
            for ca in item['Category']:
                ItemCategory['Item_ID'].append(item['ItemID'])
                ItemCategory['Category_ID'].append(str(Category[ca]))              
            ItemSeller['Item_ID'].append(item['ItemID'])
            ItemSeller['Seller_ID'].append(item["Seller"]["UserID"])
            
            #BidTable
            if item['Bids']:
                for bid in item['Bids']:
                    bid_id  = str(len(BidSet) + 1)
                    element = bid['Bid']['Bidder']['UserID'] + '|'
                    element += transformDttm(bid['Bid']['Time']) + '|'
                    element += transformDollar(bid['Bid']['Amount'])
                    BidSet.append(bid_id + "|" + element + "\n")
                    ItemBid['Item_ID'].append(item['ItemID'])
                    ItemBid['Bid_ID'].append(bid_id)
            

"""
Iterate all json fils, access the command and parser them
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    InitDicts()
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)
    with open("Category.dat","w") as f:
        f.write("".join(str(id)  + "|" + item + "\n" for item, id in Category.items())) 
    
    with open("Country.dat","w") as f: 
        f.write("".join(str(id)  + "|" + country + "\n" for country, id in Country.items())) 

    with open("Location.dat","w") as f: 
        output_str = "".join(str(location_id)  + '|'  + location + '|' + str(country_id) + '\n' for location, (location_id, country_id) in Location.items())
        f.write('"' + output_str.replace('"', '""').replace('|', '"|"').replace("\n", '"\n"')[0:-1]) 
    
    with open("User.dat","w") as f: 
        f.write("".join(str(user_id)  + "|" + info + "\n" for user_id, info in User.items()))

    with open("Item.dat", "w") as o:
        for i,j,k,m,a,b,c,d,e,f in zip(*ItemSet.values()):
            o.write(i+"|"+j+"|"+k+"|"+m+"|"+a+"|"+b+"|"+c+"|"+d+"|"+e+"|"+f+"\n")

    with open("itemCategory.dat", "w") as f:
        for i,j in zip(*ItemCategory.values()):
            f.write(i+"|"+j+"\n")

    with open("ItemBid.dat", "w") as f:
        for i,j in zip(*ItemBid.values()):
            f.write(i+"|"+j+"\n")

    with open("Bid.dat","w") as f:
           f.write("".join(BidSet))
    
    with open("itemSeller.dat", "w") as f:
        for i, j in zip(*ItemSeller.values()):
            f.write(i+"|"+j+"\n")

if __name__ == '__main__':
    main(sys.argv)

