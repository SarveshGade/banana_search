import Image from "next/image"
import Link from "next/link"
import { Banana, Search, MapPin, DollarSign, ShoppingCart } from "lucide-react"

import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-yellow-50">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="#">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="#features">
            Features
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="#how-it-works">
            How It Works
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="#faq">
            FAQ
          </Link>
        </nav>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-yellow-100">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none text-yellow-900">
                  Find the Best Grocery Deals Near You
                </h1>
                <p className="mx-auto max-w-[700px] text-yellow-700 md:text-xl">
                  Banana Search helps you locate the freshest produce and best deals on all your grocery needs. Shop
                  smarter, save more!
                </p>
              </div>
              <div className="space-x-4">
                <Button className="bg-yellow-500 text-yellow-900 hover:bg-yellow-600">
                  Start Searching <Search className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" className="text-yellow-900 border-yellow-500 hover:bg-yellow-200">
                  Learn More
                </Button>
              </div>
            </div>
          </div>
        </section>
        <section id="features" className="w-full py-12 md:py-24 lg:py-32 bg-yellow-200">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-yellow-900">
              Key Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="flex flex-col items-center text-center">
                <MapPin className="h-12 w-12 mb-4 text-yellow-600" />
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Store Locator</h3>
                <p className="text-yellow-700">Find the nearest stores with the best deals based on your location.</p>
              </div>
              <div className="flex flex-col items-center text-center">
                <DollarSign className="h-12 w-12 mb-4 text-yellow-600" />
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Price Comparison</h3>
                <p className="text-yellow-700">
                  Compare prices across multiple stores to get the best deals on your groceries.
                </p>
              </div>
              <div className="flex flex-col items-center text-center">
                <ShoppingCart className="h-12 w-12 mb-4 text-yellow-600" />
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Smart Shopping Lists</h3>
                <p className="text-yellow-700">
                  Create and optimize your shopping lists for maximum savings and efficiency.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section id="how-it-works" className="w-full py-12 md:py-24 lg:py-32 bg-yellow-50">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-yellow-900">
              How It Works
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="flex flex-col items-center text-center">
                <div className="rounded-full bg-yellow-400 text-yellow-900 w-12 h-12 flex items-center justify-center mb-4 text-xl font-bold">
                  1
                </div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Enter Your Location</h3>
                <p className="text-yellow-700">Tell us where you are to find nearby grocery stores and deals.</p>
              </div>
              <div className="flex flex-col items-center text-center">
                <div className="rounded-full bg-yellow-400 text-yellow-900 w-12 h-12 flex items-center justify-center mb-4 text-xl font-bold">
                  2
                </div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Create Your Shopping List</h3>
                <p className="text-yellow-700">Add items to your list or choose from popular categories.</p>
              </div>
              <div className="flex flex-col items-center text-center">
                <div className="rounded-full bg-yellow-400 text-yellow-900 w-12 h-12 flex items-center justify-center mb-4 text-xl font-bold">
                  3
                </div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Get Optimized Results</h3>
                <p className="text-yellow-700">Receive a list of the best stores and deals for your grocery needs.</p>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 bg-yellow-100">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-yellow-900">
              What Our Users Say
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex flex-col items-center text-center p-6 bg-yellow-50 rounded-lg shadow-lg">
                <Image
                  src="/placeholder.svg?height=100&width=100"
                  width={100}
                  height={100}
                  alt="Happy user"
                  className="rounded-full mb-4"
                />
                <p className="text-yellow-700 mb-4">
                  "Banana Search has revolutionized my grocery shopping! I always find the best deals on all my favorite
                  items."
                </p>
                <p className="font-bold text-yellow-900">- Sarah M.</p>
              </div>
              <div className="flex flex-col items-center text-center p-6 bg-yellow-50 rounded-lg shadow-lg">
                <Image
                  src="/placeholder.svg?height=100&width=100"
                  width={100}
                  height={100}
                  alt="Satisfied customer"
                  className="rounded-full mb-4"
                />
                <p className="text-yellow-700 mb-4">
                  "I love how easy it is to compare prices across different stores. This app saves me time and money
                  every week!"
                </p>
                <p className="font-bold text-yellow-900">- John D.</p>
              </div>
            </div>
          </div>
        </section>
        <section id="faq" className="w-full py-12 md:py-24 lg:py-32 bg-yellow-50">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-yellow-900">
              Frequently Asked Questions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Is Banana Search free?</h3>
                <p className="text-yellow-700">
                  Yes, our basic service is completely free to use. We also offer a premium version with additional
                  features for power users.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">How accurate are the prices?</h3>
                <p className="text-yellow-700">
                  We update our prices regularly, but they may occasionally differ from in-store prices. Always check
                  the final price at checkout.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">Can I search for any grocery item?</h3>
                <p className="text-yellow-700">
                  While our name is Banana Search, we cover all grocery items, from fresh produce to pantry staples.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-yellow-900">How do I start using Banana Search?</h3>
                <p className="text-yellow-700">
                  Simply sign up for an account, enter your location, create your shopping list, and start searching for
                  the best deals. It's that easy!
                </p>
              </div>
            </div>
          </div>
        </section>
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

