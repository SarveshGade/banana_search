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

// Sample stores data following your format.
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
    // Assume no ingredients for Aldi or add similar structure if available.
  },
};

export default function StorePrices() {
  const router = useRouter();

  // State for the shopping list items, each with a name, quantity, and price.
  const [items, setItems] = useState<Item[]>([]);
  const [newItem, setNewItem] = useState("");

  // On mount, check if shopping list items were saved in localStorage.
  useEffect(() => {
    const storedItems = localStorage.getItem("shoppingListItems");
    if (storedItems) {
      setItems(JSON.parse(storedItems));
    }
  }, []);

  const addItem = () => {
    if (newItem.trim()) {
      // For demonstration, every new item is given a default price of $0.79.
      const defaultPrice = 0.79;
      const updatedItems = [
        ...items,
        { name: newItem.trim(), quantity: 1, price: defaultPrice },
      ];
      setItems(updatedItems);
      setNewItem("");
      localStorage.setItem("shoppingListItems", JSON.stringify(updatedItems));
    }
  };

  const removeItem = (index: number) => {
    const updatedItems = items.filter((_, i) => i !== index);
    setItems(updatedItems);
    localStorage.setItem("shoppingListItems", JSON.stringify(updatedItems));
  };

  // Calculate total as the sum of price * quantity for each item.
  const total = items.reduce(
    (acc, item) => acc + (item.price ?? 0) * item.quantity,
    0
  );

  // Convert storesData object to an array for mapping.
  const groceryStoresArray = Object.entries(storesData).map(([storeName, data]) => {
    let totalCost = 0;
    if (data.ingredients) {
      const ingredientValues = Object.values(data.ingredients);
      totalCost = ingredientValues.reduce((acc, ingredient) => {
        // Use either price or retail_price (converted to number)
        const price = ingredient.price || ingredient.retail_price;
        return acc + Number(price);
      }, 0);
    }
    return {
      name: storeName,
      address: data.address,
      drive_time_minutes: data.drive_time_minutes,
      totalCost,
    };
  });

  return (
    <div className="flex flex-col min-h-screen bg-yellow-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/dashboard">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>

      <div className="max-w-7xl mx-auto p-4 min-h-screen bg-yellow-50">
        {/* Header with Banana Logo */}
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

        {/* Main Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left Column: Cart and Grocery Stores */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center justify-between bg-yellow-200 p-4 rounded-lg">
              <div className="flex items-center gap-2">
                <ShoppingCart className="h-6 w-6" />
                <span className="text-red-500 font-bold">Cart</span>
              </div>
              <span className="text-xl text-center font-bold">
                Grocery Options
              </span>
            </div>

            {/* Grocery Stores List */}
            <div className="space-y-4 p-4 border-t border-yellow-200">
              <h3 className="text-xl font-bold text-green-800 mb-2">
                Grocery Stores
              </h3>
              {groceryStoresArray.map((store, index) => (
                <div key={index} className="p-4 bg-yellow-100 rounded-lg shadow">
                  <h4 className="text-lg font-bold">{store.name}</h4>
                  <p className="text-sm text-gray-700">{store.address}</p>
                  <p className="text-sm text-gray-700">
                    Drive Time: {store.drive_time_minutes} minutes
                  </p>
                  <p className="text-sm text-gray-700">
                    Total Grocery Cost: ${store.totalCost.toFixed(2)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: Items List */}
          <div className="space-y-3">
            {items.length > 0 ? (
              items.map((item, index) => (
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
                        const newQuantity = parseInt(e.target.value);
                        const updatedItems = [...items];
                        updatedItems[index].quantity = newQuantity;
                        setItems(updatedItems);
                        localStorage.setItem(
                          "shoppingListItems",
                          JSON.stringify(updatedItems)
                        );
                      }}
                      className="bg-yellow-100 w-16 p-1 text-sm text-center border rounded"
                    />
                    <Button
                      onClick={() => removeItem(index)}
                      className="bg-red-500 hover:bg-red-600 text-white px-2 py-1 text-xs"
                    >
                      x
                    </Button>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-600">Your shopping list is empty.</p>
            )}

            {/* Total Section */}
            <div className="bg-red-400 text-white p-4 rounded-lg flex justify-between">
              <span className="text-xl font-bold">Total</span>
              <span className="text-xl font-bold">${total.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
