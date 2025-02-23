"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { Banana, Camera, ArrowRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function Cook() {
  const [step, setStep] = useState(1)
  const [fridgeImage, setFridgeImage] = useState<string | null>(null)
  const [recipe, setRecipe] = useState("")

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setFridgeImage(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleRecipeSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle recipe selection logic here
    console.log("Selected recipe:", recipe)
    setStep(3)
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/dashboard">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-yellow-900 mb-8 text-center">Let's Cook!</h1>
        {step === 1 && (
          <div className="max-w-md mx-auto text-center">
            <div className="mb-4 p-8 bg-yellow-100 rounded-lg flex flex-col items-center justify-center">
              {fridgeImage ? (
                <img
                  src={fridgeImage || "/placeholder.svg"}
                  alt="Fridge contents"
                  className="max-w-full h-auto rounded-lg"
                />
              ) : (
                <Camera className="w-24 h-24 text-yellow-600" />
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handleImageUpload}
              className="hidden"
              id="fridge-photo"
            />
            <label htmlFor="fridge-photo">
              <Button className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600 cursor-pointer">
                Take a Picture of Your Fridge
              </Button>
            </label>
            {fridgeImage && (
              <Button onClick={() => setStep(2)} className="mt-4 bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
                Next <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            )}
          </div>
        )}
        {step === 2 && (
          <div className="max-w-md mx-auto">
            <h2 className="text-2xl font-semibold text-yellow-900 mb-4">What would you like to cook?</h2>
            <form onSubmit={handleRecipeSubmit} className="space-y-4">
              <Input
                type="text"
                value={recipe}
                onChange={(e) => setRecipe(e.target.value)}
                placeholder="Enter a recipe or dish name"
                required
                className="w-full"
              />
              <Button type="submit" className="w-full bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
                Find Recipe
              </Button>
            </form>
          </div>
        )}
        {step === 3 && (
          <div className="max-w-md mx-auto">
            <h2 className="text-2xl font-semibold text-yellow-900 mb-4">Grocery List for {recipe}</h2>
            {/* This is where you'd typically fetch and display the grocery list */}
            <p className="text-yellow-700 mb-4">Here's what you need to buy for your recipe:</p>
            <ul className="list-disc list-inside text-yellow-700 mb-4">
              <li>Ingredient 1</li>
              <li>Ingredient 2</li>
              <li>Ingredient 3</li>
            </ul>
            <Button className="w-full bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
              <Link href="/shop">Go to Shopping List</Link>
            </Button>
          </div>
        )}
      </main>
    </div>
  )
}

