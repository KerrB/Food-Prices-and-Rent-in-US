import requests
import json
import numpy

#####  #####  #####    #####  #   #  #####  #####  #####  #####  ##     #####  #####  #####  #####  #####   ###   #   #
#   #  ##  #    #        #    ##  #    #      #      #    #   #  ##       #       #   #   #    #      #    #   #  ##  #
#####  #####    #        #    # # #    #      #      #    #####  ##       #      #    #####    #      #    #   #  # # #
#   #  ##       #        #    #  ##    #      #      #    #   #  ##       #     #     #   #    #      #    #   #  #  ##
#   #  ##     #####    #####  #   #  #####    #    #####  #   #  #####  #####  #####  #   #    #    #####   ###   #   #

##Get all the names of all cities and place it into an array##
cities_url="https://www.numbeo.com/api/cities?api_key=s3lxzv9hgsytve"
cities_response = requests.get(cities_url)

cities_data = cities_response.text
cities_parsed = json.loads(cities_data)








 ####  #####  #####  #####  #####  #####  #   #   ####     ####  #####  #####  #   #    ##     #####   ###   #####
##     ##  #  ##     #   #    #      #    ##  #  #        ##       #      #     # #     ##       #    #        #  
##     #####  ####   #####    #      #    # # #  ####     ##       #      #      #      ##       #     ###     #  
##     ## #   ##     #   #    #      #    #  ##  #   #    ##       #      #      #      ##       #        #    #  
 ####  ##  #  #####  #   #    #    #####  #   #   ###      ####  #####    #      #      #####  #####   ###     #  


cities = cities_parsed["cities"]
city_list = []
country_and_city = ["city", "country"]


#TODO(Optimization): Find a way to only do the United States and not the whole world
for x in range(len(cities)):
	city_list.append({key:cities[x][key] for key in country_and_city})









#####  #####  #   #  ####   #####  #   #   ####    #####  #####  #####   ####  #####   ### 
##       #    ##  #  ##  #    #    ##  #  #        ##  #  ##  #    #    ##     ##     #    
####     #    # # #  ##  #    #    # # #  ####     #####  #####    #    ##     ####    ### 
##       #    #  ##  ##  #    #    #  ##  #   #    ##     ## #     #    ##     ##         #
##     #####  #   #  ####   #####  #   #   ###     ##     ##  #  #####   ####  #####   ### 



food_and_city = []
city_rent_prices = []



##This is to get each city and get their food prices and rent price for one bedroom inner city
for x in city_list:
	if x["country"] == "United States": 
		url = "https://www.numbeo.com/api/city_prices?api_key=s3lxzv9hgsytve&query=" + x["city"] + "," + x["country"] 
		response = requests.get(url)
			
		data = response.text
		parsed = json.loads(data)

			
		if "prices" in parsed:
			items = parsed["prices"]
			current_city = x["city"]
			attribute_subset = [ "average_price",  "item_name"]
			
					
			#this for loop checks if the item name contains rent or food prices, and make sure that it has an average price property
			for i in range(len(items)):
				if (("Restaurant" in items[i]["item_name"]) or ("Market" in items[i]["item_name"])) and ("average_price" in items[i]):
					food_prices = {key:items[i][key] for key in attribute_subset}	
					thisFoodPrice = [food_prices, current_city]
					food_and_city.append(thisFoodPrice)
				elif ("Apartment (1 bedroom) in City Centre" in items[i]["item_name"]) and ("average_price" in items[i]):
					rent_prices =  {key:items[i][key] for key in attribute_subset}
					thisRentPrice = [rent_prices, current_city]			
					city_rent_prices.append(thisRentPrice)
					
					
		
					
				



 ###    ###   ##        ####   ###   ####   #####   ####  #####  #   #
#      #   #  ##       ##     #   #  ##  #  ##     #      ##     ##  #
 ###   #   #  ##       ##     #   #  ##  #  ####   ####   ####   # # #
    #  #  ##  ##       ##     #   #  ##  #  ##     #   #  ##     #  ##
 ###    ####  #####     ####   ###   ####   #####   ###   #####  #   #



##Outputting the file into an SQL 
outF = open("Project.sql", "w")

outF.write("DROP TABLE IF EXISTS CITY;" + '\n')
outF.write("CREATE TABLE IF NOT EXISTS CITY (" + '\n')
outF.write("	CITY_NAME varchar(20)," + '\n')
outF.write("	STATE varchar(2)," + '\n')
outF.write("	PRIMARY KEY (CITY_NAME)" + '\n')
outF.write(");" + '\n')
outF.write('\n')

#for loop to generate an insert line for each city
for i in city_list:
	if i["country"] == "United States":
		outF.write("INSERT INTO CITY (CITY_NAME, STATE) VALUES(\"" + i["city"] + "\", \"" + i["city"][-2] + i["city"][-1] + "\");\n") 		
outF.write('\n')



outF.write("DROP TABLE IF EXISTS RENT;" + '\n')
outF.write("CREATE TABLE IF NOT EXISTS RENT (" + '\n')
outF.write("	CITY_NAME varchar(20)," + '\n')
outF.write("	RENT varchar(10)," + '\n')
outF.write("	PRIMARY KEY (CITY_NAME)" + '\n')
outF.write(");" + '\n')

for i in city_rent_prices:
	outF.write("INSERT INTO RENT (CITY_NAME, RENT) VALUES(\"" + i[1] + "\", \"" + str(i[0]["average_price"]) + "\");\n")

outF.write('\n')


outF.write("DROP TABLE IF EXISTS FOOD;" + '\n')
outF.write("CREATE TABLE IF NOT EXISTS FOOD (" + '\n')
outF.write("	CITY_NAME varchar(20)," + '\n')
outF.write("	APPLES varchar(20)," + '\n')
outF.write("	BANANA varchar(20)," + '\n')
outF.write("	BEEF_ROUND varchar(20)," + '\n')
outF.write("	WINE varchar(20)," + '\n')
outF.write("	CHICKEN_FILLET varchar(20)," + '\n')
outF.write("	CIGARETTES varchar(20)," + '\n')
outF.write("	DOMESTIC_BEER varchar(20)," + '\n')
outF.write("	EGGS varchar(20)," + '\n')
outF.write("	IMPORTED_BEER varchar(20)," + '\n')
outF.write("	LETTUCE varchar(20)," + '\n')
outF.write("	BREAD varchar(20)," + '\n')
outF.write("	CHEESE varchar(20)," + '\n')
outF.write("	MILK varchar(20)," + '\n')
outF.write("	ONION varchar(20)," + '\n')
outF.write("	ORANGES varchar(20)," + '\n')
outF.write("	POTATO varchar(20)," + '\n')
outF.write("	RICE varchar(20)," + '\n')
outF.write("	TOMATO varchar(20)," + '\n')
outF.write("	WATER varchar(20)," + '\n')
outF.write("	PRIMARY KEY (CITY_NAME)" + '\n')
outF.write(");" + '\n')
#TODO: Write the for loop to get all the variables
#TODO: Write a case switch function to for the item type 



outF.close()
	

