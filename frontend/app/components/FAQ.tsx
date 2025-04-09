import React, { useState } from 'react';
import { FAQ as FAQSection } from "@/app/components/ui/faq-section";

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <FAQSection />
  );
};

export default FAQ; 