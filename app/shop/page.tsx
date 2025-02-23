"use client";

import { useState } from "react";
import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ShoppingListItem } from "@/components/shopping-list-item";
import { useSearchParams } from "next/navigation";
import router from "next/router";

export default function Shop() {
  const searchParams = useSearchParams();
  // Get all query parameters named "items"
  const queryItems = searchParams.getAll("items");

  // Initialize the shopping list with the query items (each with a default quantity of 1)
  // If no query parameters exist (i.e. when linked from Dashboard), the list remains empty.
  const [items, setItems] = useState<Array<{ name: string; quantity: number }>>(
    () => {
      return queryItems.length > 0
        ? queryItems.map((item) => ({ name: item, quantity: 1 }))
        : [];
    }
  );
  const [newItem, setNewItem] = useState("");

  const addItem = () => {
    if (newItem.trim()) {
      setItems([...items, { name: newItem.trim(), quantity: 1 }]);
      setNewItem("");
    }
  };

  const removeItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const handleGenerateStorePrices = () => {
    localStorage.setItem("shoppingListItems", JSON.stringify(items));
    router.push("/store_prices");
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/dashboard">
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-yellow-900 mb-8 text-center">
          Shopping List
        </h1>
        <div className="max-w-md mx-auto">
          <div className="flex mb-4">
            <Input
              type="text"
              placeholder="Add an item"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && addItem()}
              className="flex-grow mr-2"
            />
            <Button
              onClick={addItem}
              className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600"
            >
              <Plus className="w-4 h-4" />
            </Button>
          </div>
          <ul className="space-y-2">
            {items.map((item, index) => (
              <ShoppingListItem
                key={index}
                item={item.name}
                quantity={item.quantity}
                onRemove={() => removeItem(index)}
                onUpdateQuantity={(newQuantity) => {
                  const newItems = [...items];
                  newItems[index].quantity = newQuantity;
                  setItems(newItems);
                }}
              />
            ))}
          </ul>
        </div>
      </main>
      {/* NEW: Add a footer with a "Store Prices" button at the bottom of the screen */}
      <footer className="px-4 py-4">
        <div className="container mx-auto text-center">
          <Link href="/store-prices">
            <Button className="mt-4 bg-yellow-500 hover:bg-yellow-600 text-yellow-900"
            onClick={handleGenerateStorePrices}>
              Store Prices
            </Button>
          </Link>
        </div>
      </footer>
    </div>
  );
}
