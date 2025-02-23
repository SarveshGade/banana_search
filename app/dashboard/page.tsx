"use client"

import { useState } from "react"
import Link from "next/link"
import { ChefHat, ShoppingCart, MapPin, Edit2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function Dashboard() {
  const [address, setAddress] = useState("123 Banana Street, Fruitville, FB 12345")
  const [isEditingAddress, setIsEditingAddress] = useState(false)
  const [newAddress, setNewAddress] = useState(address)

  const handleAddressChange = () => {
    setAddress(newAddress)
    setIsEditingAddress(false)
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/">
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-yellow-900 mb-8 text-center">Dashboard</h1>
        <div className="mb-8 p-4 bg-yellow-100 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <MapPin className="w-6 h-6 text-yellow-600 mr-2" />
              <h2 className="text-xl font-semibold text-yellow-900">Current Address</h2>
            </div>
            {!isEditingAddress && (
              <Button
                onClick={() => setIsEditingAddress(true)}
                className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600"
              >
                <Edit2 className="w-4 h-4 mr-2" /> Edit
              </Button>
            )}
          </div>
          {isEditingAddress ? (
            <div className="mt-2 flex items-center">
              <Input value={newAddress} onChange={(e) => setNewAddress(e.target.value)} className="flex-grow mr-2" />
              <Button onClick={handleAddressChange} className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
                Save
              </Button>
            </div>
          ) : (
            <p className="mt-2 text-yellow-700">{address}</p>
          )}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col items-center p-8 bg-yellow-100 rounded-lg shadow-md">
            <ChefHat className="w-16 h-16 text-yellow-600 mb-4" />
            <h2 className="text-2xl font-semibold text-yellow-900 mb-4">Cook</h2>
            <p className="text-yellow-700 text-center mb-4">
              Find recipes and meal ideas based on ingredients you have.
            </p>
            <Button className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
              <Link href="/cook">Start Cooking</Link>
            </Button>
          </div>
          <div className="flex flex-col items-center p-8 bg-yellow-100 rounded-lg shadow-md">
            <ShoppingCart className="w-16 h-16 text-yellow-600 mb-4" />
            <h2 className="text-2xl font-semibold text-yellow-900 mb-4">Shop</h2>
            <p className="text-yellow-700 text-center mb-4">Create a shopping list and find the best deals near you.</p>
            <Button className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
              <Link href="/shop">Start Shopping</Link>
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}

