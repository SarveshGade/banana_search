const TotalPrice = ({ total }: { total: number }) => {
    return (
      <div className="mt-4 bg-red-400 p-4 rounded-lg flex justify-between text-white">
        <span>Total</span>
        <span>${total.toFixed(2)}</span>
      </div>
    );
  };
  
  export default TotalPrice;
  