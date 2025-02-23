"use client";

import React, { useState, useEffect, type ChangeEvent } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Banana, Camera, FileText, ShoppingCart, Upload } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { supabase } from "@/lib/supabaseClient";

export default function BananaSearch() {
  const [recipeInput, setRecipeInput] = useState("");
  const [recipePDF, setRecipePDF] = useState<File | null>(null);
  const [fridgeImage, setFridgeImage] = useState<File | null>(null);
  const [existingIngredients, setExistingIngredients] = useState("");
  const [recipeOutput, setRecipeOutput] = useState("");
  const [missingIngredients, setMissingIngredients] = useState<string[]>([]);
  const [address, setAddress] = useState(""); // New state for the user's address
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

  const handleRecipeInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setRecipeInput(e.target.value);
  };

  const handleRecipePDFUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setRecipePDF(e.target.files[0]);
    }
  };

  const handleFridgeImageUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFridgeImage(e.target.files[0]);
    }
  };

  const handleExistingIngredientsChange = (e: ChangeEvent<HTMLInputElement>) => {
    setExistingIngredients(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!recipeInput || !fridgeImage || !address) {
      alert("Please enter a recipe, upload a fridge image, and ensure your address is set in your profile.");
      return;
    }
    const formData = new FormData();
    formData.append("recipe", recipeInput);
    formData.append("image", fridgeImage);
    formData.append("address", address);
    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: formData,
      });
      console.log("request finished")
      if (!response.ok) {
        throw new Error("Failed to analyze image");
      }
      const data = await response.json();
      console.log("data received", data)
  
      setTimeout(() => {
        const generatedRecipe = data.recipe;
        const missing = data.missing_items;
  
        setRecipeOutput(generatedRecipe);
        setMissingIngredients(missing);
      }, 1500);
    } catch (error) {
      console.error("Error analyzing image:", error);
    }
  };
  

  const handleCreateShoppingCart = () => {
    router.push("/shop");
  };

  return (
    <div className="flex flex-col min-h-screen bg-yellow-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/dashboard">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>

      <main className="flex-grow container mx-auto px-4 py-8 flex flex-col items-center">
        {/* Banana Logo and Title */}
        <div className="flex flex-col items-center mb-8">
          <div className="relative w-32 h-16">
            <img
              src="https://static.vecteezy.com/system/resources/thumbnails/009/343/861/small/banana-is-a-yellow-fruit-free-png.png"
              alt="Banana Logo"
              className="object-contain w-full h-full"
            />
          </div>
          <h1 className="text-4xl font-bold mt-1 text-red-500">Let's Cook</h1>
        </div>

        <form onSubmit={handleSubmit} className="w-full max-w-2xl">
          <div className="bg-yellow-200 p-6 rounded-lg shadow-md space-y-4">
            <div className="flex items-center space-x-2">
              <Input
                id="recipe"
                placeholder="Enter your desired dish here... (or a pdf of your recipe!)"
                value={recipeInput}
                onChange={handleRecipeInputChange}
                className="flex-grow bg-white"
              />
              <Input
                id="recipe-pdf"
                type="file"
                accept=".pdf"
                onChange={handleRecipePDFUpload}
                className="hidden"
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => document.getElementById("recipe-pdf")?.click()}
                className="whitespace-nowrap"
              >
                <FileText className="mr-2 h-4 w-4" /> Upload PDF
              </Button>
            </div>

            <div className="flex items-center space-x-2">
              <Input
                id="existing-ingredients"
                placeholder="Upload an image of your fridge! Fill in any other ingredients too..."
                value={existingIngredients}
                onChange={handleExistingIngredientsChange}
                className="flex-grow bg-white"
              />
              <Input
                id="fridge-image"
                type="file"
                accept="image/*"
                onChange={handleFridgeImageUpload}
                className="hidden"
              />
              <Button
                type="button"
                variant="outline"
                onClick={() => document.getElementById("fridge-image")?.click()}
                className="whitespace-nowrap"
              >
                <Camera className="mr-2 h-4 w-4" /> Upload Image
              </Button>
            </div>

            {/* Display uploaded file names */}
            <div className="space-y-1">
              {recipePDF && (
                <p className="text-sm text-gray-600">Recipe PDF: {recipePDF.name}</p>
              )}
              {fridgeImage && (
                <p className="text-sm text-gray-600">Fridge Image: {fridgeImage.name}</p>
              )}
            </div>

            <Button
              type="submit"
              className="w-full bg-red-400 hover:bg-red-500 text-yellow-900 font-bold"
            >
              Analyze Recipe and Fridge
            </Button>
          </div>
        </form>

        {/* Output Bubbles */}
        {recipeOutput && (
          <div className="mt-8 w-full max-w-2xl">
            <div className="bg-green-100 p-6 rounded-lg shadow-md mb-4">
              <h2 className="text-2xl font-bold text-green-800 mb-2">Generated Recipe</h2>
              <p className="text-green-700">{recipeOutput}</p>
            </div>
            {missingIngredients.length > 0 && (
              <div className="bg-blue-100 p-6 rounded-lg shadow-md">
                <h2 className="text-2xl font-bold text-blue-800 mb-2">Missing Ingredients</h2>
                <ul className="list-disc list-inside text-blue-700">
                  {missingIngredients.map((ingredient, index) => (
                    <li key={index}>{ingredient}</li>
                  ))}
                </ul>
                <Button
                  onClick={handleCreateShoppingCart}
                  className="mt-4 bg-yellow-500 hover:bg-yellow-600 text-yellow-900"
                >
                  Create Shopping Cart
                </Button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
