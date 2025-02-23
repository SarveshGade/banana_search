"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { Banana } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function SignUp() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [address, setAddress] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Handle sign up logic here
    console.log("Sign up with:", email, password, address)
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-md mx-auto">
          <h1 className="text-3xl font-bold text-yellow-900 mb-8 text-center">Sign Up</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-yellow-900">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="mt-1"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-yellow-900">
                Password
              </label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="mt-1"
              />
            </div>
            <div>
              <label htmlFor="address" className="block text-sm font-medium text-yellow-900">
                Address
              </label>
              <Input
                id="address"
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                required
                className="mt-1"
              />
            </div>
            <Button type="submit" className="w-full bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
              Sign Up
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-yellow-900">
            Already have an account?{" "}
            <Link href="/login" className="font-medium text-yellow-600 hover:underline">
              Log in
            </Link>
          </p>
        </div>
      </main>
    </div>
  )
}

