"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ShoppingCart, Upload, Plus } from "lucide-react"
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ShoppingListItem } from "@/components/shopping-list-item";
import { useRouter } from "next/navigation";

export default function StorePrices() {
  const router = useRouter();

  // State for the shopping list items, each with a name and quantity.
  const [items, setItems] = useState<Array<{ name: string; quantity: number }>>([]);
  const [newItem, setNewItem] = useState("");

  // On mount, check if shopping list items were saved in localStorage.
  useEffect(() => {
    const storedItems = localStorage.getItem("shoppingListItems");
    if (storedItems) {
      setItems(JSON.parse(storedItems));
    }
  }, []);
  console.log(items)

  const addItem = () => {
    if (newItem.trim()) {
      const updatedItems = [...items, { name: newItem.trim(), quantity: 1 }];
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

  return (
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
        {/* Cart and Order Section */}
        <div className="md:col-span-2 space-y-4">
          <div className="flex items-center justify-between bg-yellow-200 p-4 rounded-lg">
            <div className="flex items-center gap-2">
              <ShoppingCart className="h-6 w-6" />
              <span className="text-red-500 font-bold">6</span>
            </div>
            <span className="text-xl font-bold">$13.60</span>
          </div>

          {/* Cook Recipe Section */}
          <div className="flex items-center gap-4 p-4 border-t border-yellow-200">
            <span className="text-red-500 text-xl font-bold">Cook</span>
            <span className="text-yellow-400 text-xl">Recipe</span>
          </div>
        </div>

        {/* Items List */}
        <div className="space-y-3">
          {[1, 2, 3, 4].map((item) => (
            <div key={item} className="bg-yellow-200 p-4 rounded-lg flex justify-between">
              <div>
                <p className="font-medium">Banana</p>
                <p className="text-yellow-600">3</p>
              </div>
              <div className="text-right">
                <p className="font-medium">$0.79</p>
                <p className="text-yellow-600">$2.37</p>
              </div>
            </div>
          ))}

          {/* Total */}
          <div className="bg-red-400 text-white p-4 rounded-lg flex justify-between">
            <span className="text-xl font-bold">Total</span>
            <span className="text-xl font-bold">$9.48</span>
          </div>
        </div>
      </div>
    </div>
  )
}