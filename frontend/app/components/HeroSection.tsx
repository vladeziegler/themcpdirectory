import React from 'react';
import { ArrowRight } from "lucide-react";
import Search from "@/app/components/Search"
export default function HeroSection() {
  return (
    <div className="text-center py-12">
      <h1 className="text-4xl md:text-6xl font-bold mb-4">
        Find the <span className="text-red-500">MCP servers</span> for your needs
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        The largest collection of MCP servers for your AI agents
      </p>
      <Search />
      {/* <div className="relative max-w-2xl mx-auto">
        <input
          type="text"
          placeholder="e.g. best servers for web search"
          className="w-full px-5 py-4 pl-12 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-red-500 text-lg"
        />
        <button className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gray-100 p-2 rounded-md hover:bg-gray-200 transition-colors">
          <ArrowRight className="h-5 w-5" />
        </button>
      </div> */}
    </div>
  );
}