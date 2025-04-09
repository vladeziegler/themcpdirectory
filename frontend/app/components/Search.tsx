'use client';

import React, { useState, useEffect } from 'react';
import { Search as SearchIcon, ArrowRight } from "lucide-react";
import { BentoItem, BentoGridProps, itemsSample } from "@/app/components/ui/bento-grid";
import { Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { MessageLoading } from "@/app/components/message-loading";
import Results from './Results';

interface SearchResult {
  url: string;
  description: string;
  what_can_it_do: string;
  why_is_it_useful: string;
}

interface RecentSearch {
  query: string;
  timestamp: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:5000/api';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [recentSearches, setRecentSearches] = useState<RecentSearch[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isBackendAvailable, setIsBackendAvailable] = useState(true);
  const [summary, setSummary] = useState('');

  // useEffect(() => {
  //   checkBackendHealth();
  // }, []);

  // const checkBackendHealth = async () => {
  //   try {
  //     const response = await fetch(`${API_BASE_URL}/health`);
  //     if (!response.ok) {
  //       throw new Error('Backend health check failed');
  //     }
  //     setIsBackendAvailable(true);
  //   } catch (err) {
  //     console.error('Backend health check failed:', err);
  //     setIsBackendAvailable(false);
  //   }
  // };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isBackendAvailable) {
      setError('Backend service is not available. Please try again later.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSummary('');

    try {
      const response = await fetch(`${API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          top_k: 3,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Search failed');
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error('Search error:', err);
      setError(err instanceof Error ? err.message : 'Failed to perform search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isBackendAvailable) {
    return (
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Backend Not Available</strong>
          <p className="block sm:inline"> Please make sure the backend server is running on port 5000.</p>
        </div>
      </div>
    );
  }

  // Map search results to BentoItem format
  const items: BentoItem[] = results.map((result) => ({
    title: result.url,
    description: result.what_can_it_do,
    icon: null,
    meta: result.why_is_it_useful,
    cta: "Deploy →",
  }));

  return (
    <div className="max-w-4xl mx-auto p-4">
      <form onSubmit={handleSearch} className="mb-6">
        <div className="relative max-w-2xl mx-auto">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. best servers for web search"
            className="w-full px-5 py-4 pl-12 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-red-500 text-lg"
          />
          <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <button
            type="submit"
            disabled={isLoading}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-gray-100 p-2 rounded-md hover:bg-gray-200 transition-colors"
          >
            {isLoading ? 'Searching...' : <ArrowRight className="h-5 w-5" />}
          </button>
        </div>
      </form>

      {isLoading && (
        <div className="flex justify-center my-4">
          <MessageLoading />
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative mb-4">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-4">
        <div>
          <h2 className="text-xl font-semibold mb-3">Search Results</h2>
          {results.length > 0 ? (
            <Results items={items} />
          ) : (
            <p className="text-gray-500">No results to display</p>
          )}
        </div>
        {summary && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-3">Summary</h2>
            <p className="text-gray-700">{summary}</p>
          </div>
        )}
      </div>
    </div>
  );
}

function BentoGrid({ items = itemsSample }: BentoGridProps) {
    return (
        <div className="grid grid-cols-1 gap-3 p-4 max-w-7xl mx-auto">
            {items.map((item: BentoItem, index: number) => (
                <div
                    key={index}
                    className={cn(
                        "group relative p-4 rounded-xl overflow-hidden transition-all duration-300",
                        "border border-gray-100/80 dark:border-white/10 bg-white dark:bg-black",
                        "hover:shadow-[0_2px_12px_rgba(0,0,0,0.03)] dark:hover:shadow-[0_2px_12px_rgba(255,255,255,0.03)]",
                        "hover:-translate-y-0.5 will-change-transform"
                    )}
                >
                    <div className="relative flex flex-col space-y-3">
                        <a href={item.title} className="text-lg font-medium text-blue-700 hover:underline" target="_blank" rel="noopener noreferrer">
                            {item.title}
                        </a>
                        <div className="space-y-2">
                            <h3 className="font-medium text-gray-900 dark:text-gray-100 tracking-tight text-[15px]">
                                What it does
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-300 leading-snug font-[425]">
                                {item.description}
                            </p>
                            <h3 className="font-medium text-gray-900 dark:text-gray-100 tracking-tight text-[15px]">
                                Why it's useful
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-300 leading-snug font-[425]">
                                {item.meta}
                            </p>
                        </div>
                        <span className="text-xs text-gray-500 dark:text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">
                            {item.cta || "Deploy →"}
                        </span>
                    </div>
                </div>
            ))}
        </div>
    );
} 