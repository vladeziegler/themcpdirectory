import React from 'react';
import { Link, Info, Star } from 'lucide-react';
import { BentoItem } from '@/app/components/ui/bento-grid';

interface ResultsProps {
  items: BentoItem[];
}

const Results: React.FC<ResultsProps> = ({ items }) => {
  return (
    <div className="grid grid-cols-1 gap-6">
      {items.map((item, index) => (
        <div key={index} className="p-4 border rounded-lg shadow-sm text-left bg-gray-100">
          <a href={item.title} className="flex items-center text-blue-700 hover:underline mb-2">
            <Link className="w-4 h-4 mr-2" />
            {item.title}
          </a>
          <div className="flex items-start mb-2">
            <Info className="w-4 h-4 mr-2 text-gray-700" />
            <div>
              <h3 className="font-medium text-gray-900">What it does</h3>
              <p className="text-sm text-gray-700">{item.description}</p>
            </div>
          </div>
          <div className="flex items-start">
            <Star className="w-4 h-4 mr-2 text-yellow-600" />
            <div>
              <h3 className="font-medium text-gray-900">Why it's useful</h3>
              <p className="text-sm text-gray-700">{item.meta}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Results; 