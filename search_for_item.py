# main.py
from maps_api import stores  # Import the module that contains your functions
from trader_joes import webscrape

def main():
    # Provide the store address and search term.
    address = "1025 Spring St Nw, Atlanta, GA"
    search_term = "banana"
    
    # Call the function from the module.
    store_list = stores.get_stores_by_address(address=address)

    store_address = ""
    
    for store in store_list:
        if store["name"] == "Trader Joe's":
            store_address = store["vicinity"]
            break

    if (store_address == ""):
        print("Couldn't find any trader joes nearby.")

    else:
        webscrape.get_results(store_address, search_term)
    

if __name__ == "__main__":
    main()