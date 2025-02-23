"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ShoppingCart, Banana } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useRouter } from "next/navigation";

type Item = { name: string; quantity: number; price: number };

type GroceryStoreData = {
  address: string;
  drive_time_minutes: number;
  ingredients?: {
    [key: string]: { name: string; price?: number; retail_price?: string };
  };
};

const storesData: { [key: string]: GroceryStoreData } = {
  Kroger: {
    address: "3855 Buford Hwy NE, Atlanta",
    drive_time_minutes: 8.9,
    ingredients: {
      carrots: { name: "Carrots", price: 1.69 },
      tortilla: { name: "Guerrero® Tortillas de Harina Caseras Fajita Flour Tortillas", price: 3.29 },
      eggs: { name: "Kroger® Grade A Jumbo White Eggs", price: 5.39 },
      ham: { name: "Smithfield Anytime Favorites Diced Ham", price: 3.99 },
      cheese: { name: "Kroger® Italian Style Blend Shredded Cheese", price: 2.29 },
    },
  },
  "Trader Joe's": {
    address: "3183 Peachtree Road, Atlanta",
    drive_time_minutes: 9.2,
    ingredients: {
      carrots: { name: "CARROTS CUT & PEELED 1.5 LB", retail_price: "1.69" },
      tortilla: { name: "FLOUR TORTILLAS", retail_price: "1.99" },
      eggs: { name: "BOWL BREAKFAST CHICKEN SAUSAGE & EGG", retail_price: "4.29" },
      ham: { name: "HAMBURGER BUNS", retail_price: "2.99" },
      cheese: { name: "CREAM CHEESE BRICK", retail_price: "1.99" },
    },
  },
  Aldi: {
    address: "3963 Buford Highway, Atlanta",
    drive_time_minutes: 9.8,
    // No ingredients provided for Aldi.
  },
};

export default function StorePrices() {
  const router = useRouter();

  // State for the selected grocery store.
  const [selectedStore, setSelectedStore] = useState<string | null>(null);
  // State for the grocery list items for the selected store.
  const [storeItems, setStoreItems] = useState<Item[]>([]);
  // Optional state for manually adding an item.
  const [newItem, setNewItem] = useState("");

  // Convert storesData to an array for mapping in the left column.
  const groceryStoresArray = Object.entries(storesData).map(([storeName, data]) => ({
    name: storeName,
    address: data.address,
    drive_time_minutes: data.drive_time_minutes,
    ingredients: data.ingredients,
  }));

  // On mount, default select the first store.
  useEffect(() => {
    if (!selectedStore && groceryStoresArray.length > 0) {
      setSelectedStore(groceryStoresArray[0].name);
    }
  }, [selectedStore, groceryStoresArray]);

  // When a store is selected, update storeItems based solely on the store's ingredients.
  useEffect(() => {
    if (selectedStore && storesData[selectedStore]?.ingredients) {
      const newStoreItems: Item[] = Object.values(storesData[selectedStore].ingredients).map((ing) => ({
        name: ing.name,
        price:
          ing.price !== undefined
            ? Number(ing.price)
            : ing.retail_price
            ? Number(ing.retail_price)
            : 0,
        quantity: 1,
      }));
      setStoreItems(newStoreItems);
    } else {
      setStoreItems([]);
    }
  }, [selectedStore]);

  // Calculate total using storeItems.
  const total = storeItems.reduce((acc, item) => acc + item.price * item.quantity, 0);

  // Optionally allow manually adding a new item.
  const addItem = () => {
    if (newItem.trim()) {
      const updatedItems = [...storeItems, { name: newItem.trim(), quantity: 1, price: 0 }];
      setStoreItems(updatedItems);
      setNewItem("");
    }
  };

  const removeItem = (index: number) => {
    const updatedItems = storeItems.filter((_, i) => i !== index);
    setStoreItems(updatedItems);
  };

  return (
    <div className="flex flex-col min-h-screen bg-yellow-50">
      {/* Header */}
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/dashboard">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>

      <div className="max-w-7xl mx-auto p-4 bg-yellow-50">
        {/* Page Title */}
        <div className="flex flex-col items-center mb-8">
          <div className="relative w-64 h-32">
            <img
              src="https://static.vecteezy.com/system/resources/thumbnails/009/343/861/small/banana-is-a-yellow-fruit-free-png.png"
              alt="Banana Logo"
              className="object-contain w-full h-full"
            />
          </div>
          <h1 className="text-4xl font-bold mt-2">Banana Search</h1>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left Column: Cart and Grocery Store Selection */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center justify-between bg-yellow-200 p-4 rounded-lg">
              <div className="flex items-center gap-2">
                <ShoppingCart className="h-6 w-6" />
                <span className="text-red-500 font-bold">Cart</span>
              </div>
              <span className="text-xl text-center font-bold">Grocery Options</span>
            </div>

            {/* Grocery Stores List */}
            <div className="space-y-4 p-4 border-t border-yellow-200">
              <h3 className="text-xl font-bold text-green-800 mb-2">Grocery Stores</h3>
              <div className="grid grid-cols-1 gap-4">
                {groceryStoresArray.map((store, index) => (
                  <div
                    key={index}
                    onClick={() => setSelectedStore(store.name)}
                    className={`p-4 rounded-lg shadow cursor-pointer border ${
                      selectedStore === store.name ? "border-blue-500" : "border-transparent"
                    }`}
                  >
                    <h4 className="text-lg font-bold">{store.name}</h4>
                    <p className="text-sm text-gray-700">{store.address}</p>
                    <p className="text-sm text-gray-700">
                      Drive Time: {store.drive_time_minutes} minutes
                    </p>
                    {store.ingredients && (
                      <p className="text-sm text-gray-700">
                        Total Cost: $
                        {Object.values(store.ingredients)
                          .reduce((acc, ing) => {
                            const price = ing.price ?? (ing.retail_price ? Number(ing.retail_price) : 0);
                            return acc + price;
                          }, 0)
                          .toFixed(2)}
                      </p>
                    )}
                  </div>
                ))}
              </div>
              {selectedStore && (
                <p className="mt-2 text-sm text-blue-700">
                  Selected store: <strong>{selectedStore}</strong>
                </p>
              )}
            </div>
          </div>

          {/* Right Column: Store Items List */}
          <div className="space-y-3">
            {selectedStore ? (
              storeItems.length > 0 ? (
                storeItems.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-4 bg-yellow-200 rounded-lg"
                  >
                    <div className="flex-grow">
                      <p className="text-lg font-medium">{item.name}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <p className="text-sm text-gray-700">
                        ${(item.price ?? 0).toFixed(2)} x {item.quantity}
                      </p>
                      <Input
                        type="number"
                        value={item.quantity}
                        onChange={(e) => {
                          const newQuantity = parseInt(e.target.value) || 0;
                          const updatedItems = [...storeItems];
                          updatedItems[index].quantity = newQuantity;
                          setStoreItems(updatedItems);
                        }}
                        className="bg-yellow-100 w-16 p-1 text-sm text-center border rounded"
                      />
                      <Button
                        onClick={() => {
                          const updatedItems = storeItems.filter((_, i) => i !== index);
                          setStoreItems(updatedItems);
                        }}
                        className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 text-xs"
                      >
                        x
                      </Button>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600">No ingredients available for this store.</p>
              )
            ) : (
              <p className="text-gray-600">Please select a grocery store to view prices.</p>
            )}

            {/* Total Section */}
            {selectedStore && (
              <div className="bg-red-400 text-white p-4 rounded-lg flex justify-between">
                <span className="text-xl font-bold">Total</span>
                <span className="text-xl font-bold">${total.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
