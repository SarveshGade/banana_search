import Link from "next/link"
import { Banana, Search } from "lucide-react"

import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-yellow-400">
        <Link className="flex items-center justify-center" href="/">
          <Banana className="h-6 w-6 mr-2 text-yellow-900" />
          <span className="font-bold text-yellow-900">Banana Search</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="/how-it-works">
            How It Works
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-yellow-900" href="/login">
            Login
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
                  <Link href="/signup">
                    Start Searching <Search className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                <Button variant="outline" className="text-yellow-900 border-yellow-500 hover:bg-yellow-200">
                  <Link href="/how-it-works">Learn More</Link>
                </Button>
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

