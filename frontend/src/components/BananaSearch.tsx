import SearchBar from "./SearchBar";
import Cart from "./Cart";
import CartItem from "./CartItem";
import TotalPrice from "./TotalPrice";
import Toggle from "./Toggle";

const BananaSearch = () => {
  const cartItems = [
    { name: "Banana", price: 0.79, quantity: 3, total: 2.37 },
    { name: "Banana", price: 0.79, quantity: 3, total: 2.37 },
    { name: "Banana", price: 0.79, quantity: 3, total: 2.37 },
    { name: "Banana", price: 0.79, quantity: 3, total: 2.37 },
  ];

  return (
    <div className="max-w-2xl mx-auto bg-gray-100 p-4 rounded-lg">
      {/* Header */}
      <div className="flex items-center justify-center mb-6">
        <img
          src="/api/placeholder/80/40"
          alt="Banana"
          className="h-10 mr-2"
        />
        <h1 className="text-4xl font-normal">Banana Search</h1>
      </div>

      {/* Components */}
      <SearchBar />
      <Cart />

      {/* Cart Items */}
      <div className="space-y-2">
        {cartItems.map((item, index) => (
          <CartItem key={index} {...item} />
        ))}
      </div>

      {/* Total */}
      <TotalPrice total={9.48} />

      {/* Cook/Recipe Toggle */}
      <Toggle />
    </div>
  );
};

export default BananaSearch;
