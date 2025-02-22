import { ShoppingCart } from "lucide-react";

const Cart = () => {
  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center">
        <div className="relative">
          <ShoppingCart className="h-6 w-6 text-gray-700" />
          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
            6
          </span>
        </div>
        <span className="ml-4 text-xl">$13.60</span>
      </div>
      <button className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600">
        Order Now
      </button>
    </div>
  );
};

export default Cart;
