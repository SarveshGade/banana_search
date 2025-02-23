"use client"
import { X, Minus, Plus } from "lucide-react"

import { Button } from "@/components/ui/button"

interface ShoppingListItemProps {
  item: string
  quantity: number
  onRemove: () => void
  onUpdateQuantity: (newQuantity: number) => void
}

export function ShoppingListItem({ item, quantity, onRemove, onUpdateQuantity }: ShoppingListItemProps) {
  const handleQuantityChange = (newQuantity: number) => {
    if (newQuantity > 0) {
      onUpdateQuantity(newQuantity)
    }
  }

  return (
    <li className="flex items-center justify-between p-3 bg-yellow-100 rounded-lg">
      <span className="text-yellow-900 flex-grow">{item}</span>
      <div className="flex items-center">
        <Button
          onClick={() => handleQuantityChange(quantity - 1)}
          variant="ghost"
          size="sm"
          className="text-yellow-600 hover:text-yellow-900"
        >
          <Minus className="w-4 h-4" />
        </Button>
        <input
          type="number"
          value={quantity}
          onChange={(e) => {
            const newQuantity = Number.parseInt(e.target.value, 10)
            if (!isNaN(newQuantity) && newQuantity > 0) {
              onUpdateQuantity(newQuantity)
            }
          }}
          className="w-16 p-1 text-center border rounded mx-1 bg-yellow-50 text-yellow-900"
          min="1"
        />
        <Button
          onClick={() => handleQuantityChange(quantity + 1)}
          variant="ghost"
          size="sm"
          className="text-yellow-600 hover:text-yellow-900"
        >
          <Plus className="w-4 h-4" />
        </Button>
        <Button onClick={onRemove} variant="ghost" size="sm" className="text-yellow-600 hover:text-yellow-900 ml-2">
          <X className="w-4 h-4" />
        </Button>
      </div>
    </li>
  )
}

