"use client";

import React, { useState, useEffect, type ChangeEvent } from "react";
import Link from "next/link";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ShoppingListItem } from "@/components/shopping-list-item";
import { useSearchParams } from "next/navigation";
import { supabase } from "@/lib/supabaseClient";
import { useRouter } from "next/navigation";
import router from "next/router";

export default function Shop() {
  const searchParams = useSearchParams();

  // Initialize the shopping list with the query items (each with a default quantity of 1)
  // If no query parameters exist (i.e. when linked from Dashboard), the list remains empty.
  const [items, setItems] = useState<Array<{ name: string; quantity: number }>>(() => {
    const storedItems = localStorage.getItem("missingIngredients");
    if (storedItems) {
      const parsed = JSON.parse(storedItems);
      // Check if the parsed data is an array of strings and map it accordingly.
      if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === "string") {
        return parsed.map((ingredient: string) => ({ name: ingredient, quantity: 1 }));
      }
      // Otherwise, assume it's already in the correct format.
      return parsed;
    }
    return [];
  });
  console.log(items);
  const [newItem, setNewItem] = useState("");
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [stores, setStores] = useState<string[]>([]);
  const [address, setAddress] = useState("");
  const router = useRouter();

  // Fetch the session on component mount and extract the address from user metadata
  useEffect(() => {
    const fetchSession = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session) {
        const userAddress = session.user.user_metadata.address;
        if (userAddress) {
          setAddress(userAddress);
        }
      }
    };
    fetchSession();
  }, []);

  const addItem = () => {
    if (newItem.trim()) {
      setItems([...items, { name: newItem.trim(), quantity: 1 }]);
      setNewItem("");
    }
  };

  const removeItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const handleGenerateStorePrices = async (e: React.FormEvent) => {
    // e.preventDefault();
    // const formData = new FormData();
    // const groceryNames = items.map(item => item.name.trim());
    
    // // Send the array directly, not as a nested JSON string
    // formData.append("ingredient_input", JSON.stringify(groceryNames));
    // formData.append("address", address);
    
    // console.log("Sending data:", {
    //     ingredients: groceryNames,
    //     address: address
    // });

    try {
    //     const response = await fetch("http://localhost:8000/groceries", {
    //         method: "POST",
    //         body: formData,
    //         headers: {
    //             'Accept': 'application/json',
    //         },
    //     });
        
    //     if (!response.ok) {
    //         const errorText = await response.text();
    //         throw new Error(`Failed to analyze groceries: ${errorText}`);
    //     }
        
    //     const data = await response.json();
    //     console.log("stores received", data);

    //     const stores = data.stores;
    //     setStores(stores);
    //     localStorage.setItem("shoppingListItems", JSON.stringify(items));
    //     localStorage.setItem("store_data", JSON.stringify(stores));  // Fixed typo in key name
        
        router.push("/storePrices");
    } catch (error) {
        console.error("Error generating output:", error);
    }
  };

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
          <Button className="mt-4 bg-yellow-500 hover:bg-yellow-600 text-yellow-900"
            onClick={handleGenerateStorePrices}>
              Store Prices
          </Button>
        </div>
      </footer>
    </div>
  );
}
