import Link from "next/link"
import { Banana, MapPin, ShoppingCart, DollarSign } from "lucide-react"

export default function HowItWorks() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="/login">
            Login
          </Link>
        </nav>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-yellow-900 mb-8 text-center">How It Works</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="flex flex-col items-center text-center">
            <MapPin className="h-12 w-12 mb-4 text-yellow-600" />
            <h2 className="text-xl font-bold mb-2 text-yellow-900">1. Enter Your Location</h2>
            <p className="text-yellow-700">Tell us where you are to find nearby grocery stores and deals.</p>
          </div>
          <div className="flex flex-col items-center text-center">
            <ShoppingCart className="h-12 w-12 mb-4 text-yellow-600" />
            <h2 className="text-xl font-bold mb-2 text-yellow-900">2. Create Your Shopping List</h2>
            <p className="text-yellow-700">Add items to your list or choose from popular categories.</p>
          </div>
          <div className="flex flex-col items-center text-center">
            <DollarSign className="h-12 w-12 mb-4 text-yellow-600" />
            <h2 className="text-xl font-bold mb-2 text-yellow-900">3. Get Optimized Results</h2>
            <p className="text-yellow-700">Receive a list of the best stores and deals for your grocery needs.</p>
          </div>
        </div>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-yellow-400">
        <p className="text-xs text-yellow-900">© 2024 Banana Search. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4 text-yellow-900" href="#">
            Terms of Service
          </Link>
          <Link className="text-xs hover:underline underline-offset-4 text-yellow-900" href="#">
            Privacy
          </Link>
        </nav>
      </footer>
    </div>
  )
}

