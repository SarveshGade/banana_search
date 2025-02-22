import { Upload } from "lucide-react";

const SearchBar = () => {
  return (
    <div className="relative mb-6">
      <input
        type="text"
        placeholder="Search Food or Upload Your Fridge..."
        className="w-full px-4 py-3 rounded-full bg-gray-300 text-gray-700 focus:outline-none"
      />
      <button className="absolute right-2 top-2 p-1 rounded-full">
        <Upload className="h-6 w-6 text-gray-600" />
      </button>
    </div>
  );
};

export default SearchBar;
