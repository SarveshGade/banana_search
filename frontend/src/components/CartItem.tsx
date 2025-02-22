const CartItem = ({ name, price, quantity, total }: { name: string, price: number, quantity: number, total: number }) => {
    return (
      <div className="bg-gray-300 p-3 rounded-lg flex justify-between">
        <div>
          <div>{name}</div>
          <div>{quantity}</div>
        </div>
        <div>
          <div>${price.toFixed(2)}</div>
          <div>${total.toFixed(2)}</div>
        </div>
      </div>
    );
  };
  
  export default CartItem;
  