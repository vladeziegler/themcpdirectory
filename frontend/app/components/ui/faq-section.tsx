import { Check, PhoneCall } from "lucide-react";
import { Badge } from "@/app/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/app/components/ui/accordion";
import { Button } from "@/app/components/ui/button";

function FAQ() {
  const faqItems = [
    {
      question: "What is MCP (Model Context Protocol)?",
      answer: "MCP is an open-source protocol developed by Anthropic that enables AI systems like Claude to securely connect with various data sources. It provides a universal standard for AI assistants to access external data, tools, and prompts through a client-server architecture."
    },
    {
      question: "What are MCP Servers?",
      answer: "MCP Servers are systems that provide context, tools, and prompts to AI clients. They can expose data sources like files, documents, databases, and API integrations, allowing AI assistants to access real-time information in a secure way."
    },
    {
      question: "How do MCP Servers work?",
      answer: "MCP Servers work through a simple client-server architecture. They expose data and tools through a standardized protocol, maintaining secure 1:1 connections with clients inside host applications like Claude Desktop."
    },
    {
      question: "What can MCP Servers provide?",
      answer: "MCP Servers can share resources (files, docs, data), expose tools (API integrations, actions), and provide prompts (templated interactions). They control their own resources and maintain clear system boundaries for security."
    },
    {
      question: "How does Claude use MCP?",
      answer: "Claude can connect to MCP servers to access external data sources and tools, enhancing its capabilities with real-time information. Currently, this works with local MCP servers, with enterprise remote server support coming soon."
    },
    {
      question: "Are MCP Servers secure?",
      answer: "Yes, security is built into the MCP protocol. Servers control their own resources, there's no need to share API keys with LLM providers, and the system maintains clear boundaries. Each server manages its own authentication and access control."
    },
    {
      question: "What is MCP Directory?",
      answer: "MCP Directory is a community-driven platform that collects and organizes third-party MCP Servers. It serves as a central directory where users can discover, share, and learn about various MCP Servers available for AI applications."
    }
  ];

  return (
    <div className="w-full py-20 lg:py-40">
      <div className="container mx-auto">
        <div className="grid lg:grid-cols-2 gap-10">
          <div className="flex gap-10 flex-col">
            <div className="flex gap-4 flex-col">
              <div>
                <Badge variant="outline">FAQ</Badge>
              </div>
              <div className="flex gap-2 flex-col">
                <h4 className="text-3xl md:text-5xl tracking-tighter max-w-xl text-left font-regular">
                  Frequently Asked Questions
                </h4>
                <p className="text-lg max-w-xl lg:max-w-lg leading-relaxed tracking-tight text-muted-foreground text-left">
                  Here are some common questions about MCP Servers.
                </p>
              </div>
              <div className="">
                <Button className="gap-4" variant="outline">
                  Any questions? Reach out <PhoneCall className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
          <Accordion type="single" collapsible className="w-full">
            {faqItems.map((item, index) => (
              <AccordionItem key={index} value={"index-" + index}>
                <AccordionTrigger>
                  {item.question}
                </AccordionTrigger>
                <AccordionContent>
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </div>
  );
}

export { FAQ };
