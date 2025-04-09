import type { ServerData } from "./types"

export const servers: ServerData[] = [
  // File Management
  {
    id: "dropbox-mcp",
    name: "Dropbox MCP",
    provider: "dropbox",
    description: "Access and manage your Dropbox files directly through MCP protocol",
    tags: ["storage", "files"],
    category: "file-management",
  },
  {
    id: "gdrive-mcp",
    name: "Google Drive MCP",
    provider: "google",
    description: "Connect to Google Drive for seamless file access and management",
    tags: ["storage", "google"],
    category: "file-management",
  },
  {
    id: "onedrive-mcp",
    name: "OneDrive MCP Server",
    provider: "microsoft",
    description: "Microsoft OneDrive integration for document access and collaboration",
    tags: ["storage", "microsoft"],
    category: "file-management",
  },
  {
    id: "s3-mcp",
    name: "S3 Bucket MCP",
    provider: "aws",
    description: "Connect to AWS S3 buckets for cloud storage access via MCP",
    tags: ["cloud", "aws"],
    category: "file-management",
  },

  // Web Browsing/Scraping
  {
    id: "perplexity-mcp",
    name: "Perplexity Ask MCP",
    provider: "ppl-ai",
    description:
      "A Model Context Protocol Server connector for Perplexity API, to enable web search without leaving the MCP environment",
    tags: ["search", "web"],
    category: "web-browsing",
  },
  {
    id: "tavily-mcp",
    name: "Tavily MCP Server 🚀",
    provider: "tavily-ai",
    description: "Advanced search capabilities for AI assistants via MCP protocol",
    tags: ["search", "ai"],
    category: "web-browsing",
  },
  {
    id: "browserless-mcp",
    name: "Browserless MCP",
    provider: "browserless",
    description: "Headless browser automation and web scraping through MCP",
    tags: ["browser", "automation"],
    category: "web-browsing",
  },
  {
    id: "scrapeowl-mcp",
    name: "ScrapeOwl MCP",
    provider: "scrapeowl",
    description: "Web scraping and data extraction service with MCP integration",
    tags: ["scraping", "data"],
    category: "web-browsing",
  },

  // Communication/Collaboration
  {
    id: "slack-mcp",
    name: "Slack MCP",
    provider: "slack",
    description: "Connect to Slack workspaces and channels through MCP protocol",
    tags: ["messaging", "teams"],
    category: "communication",
  },
  {
    id: "notion-mcp",
    name: "Notion MCP",
    provider: "notion",
    description: "Access and update Notion workspaces and databases via MCP",
    tags: ["notes", "collaboration"],
    category: "communication",
  },
  {
    id: "teams-mcp",
    name: "Microsoft Teams MCP",
    provider: "microsoft",
    description: "Integrate with Microsoft Teams for communication and collaboration",
    tags: ["messaging", "microsoft"],
    category: "communication",
  },
  {
    id: "discord-mcp",
    name: "Discord MCP",
    provider: "discord",
    description: "Connect to Discord servers and channels through MCP protocol",
    tags: ["messaging", "community"],
    category: "communication",
  },

  // Code and Development
  {
    id: "github-mcp",
    name: "GitHub MCP",
    provider: "github",
    description: "Access GitHub repositories, issues, and pull requests via MCP",
    tags: ["git", "code"],
    category: "development",
  },
  {
    id: "vscode-mcp",
    name: "VS Code MCP",
    provider: "microsoft",
    description: "Connect to VS Code for code editing and development workflows",
    tags: ["editor", "ide"],
    category: "development",
  },
  {
    id: "replit-mcp",
    name: "Replit MCP",
    provider: "replit",
    description: "Access Replit workspaces and collaborate on code through MCP",
    tags: ["coding", "cloud"],
    category: "development",
  },
  {
    id: "figma-mcp",
    name: "Framelink Figma MCP",
    provider: "GLips",
    description: "MCP server to provide Figma layout information to AI coding agents like Cursor",
    tags: ["design", "ui"],
    category: "development",
  },
]

export function getServersByCategory(category: string) {
  return servers.filter((server) => server.category === category)
}

export const categories = [
  {
    id: "file-management",
    title: "File Management",
    servers: getServersByCategory("file-management"),
  },
  {
    id: "web-browsing",
    title: "Web Browsing/Scraping",
    servers: getServersByCategory("web-browsing"),
  },
  {
    id: "communication",
    title: "Communication/Collaboration",
    servers: getServersByCategory("communication"),
  },
  {
    id: "development",
    title: "Code and Development",
    servers: getServersByCategory("development"),
  },
]


// import type { ServerData } from "./types"

// export const servers: ServerData[] = [
//   // File Management
//   {
//     id: "dropbox-mcp",
//     name: "Dropbox MCP",
//     provider: "dropbox",
//     description: "Access and manage your Dropbox files directly through MCP protocol",
//     tags: ["storage", "files"],
//     category: "file-management",
//   },
//   {
//     id: "gdrive-mcp",
//     name: "Google Drive MCP",
//     provider: "google",
//     description: "Connect to Google Drive for seamless file access and management",
//     tags: ["storage", "google"],
//     category: "file-management",
//   },
//   {
//     id: "onedrive-mcp",
//     name: "OneDrive MCP Server",
//     provider: "microsoft",
//     description: "Microsoft OneDrive integration for document access and collaboration",
//     tags: ["storage", "microsoft"],
//     category: "file-management",
//   },
//   {
//     id: "s3-mcp",
//     name: "S3 Bucket MCP",
//     provider: "aws",
//     description: "Connect to AWS S3 buckets for cloud storage access via MCP",
//     tags: ["cloud", "aws"],
//     category: "file-management",
//   },

//   // Web Browsing/Scraping
//   {
//     id: "perplexity-mcp",
//     name: "Perplexity Ask MCP",
//     provider: "ppl-ai",
//     description:
//       "A Model Context Protocol Server connector for Perplexity API, to enable web search without leaving the MCP environment",
//     tags: ["search", "web"],
//     category: "web-browsing",
//   },
//   {
//     id: "tavily-mcp",
//     name: "Tavily MCP Server 🚀",
//     provider: "tavily-ai",
//     description: "Advanced search capabilities for AI assistants via MCP protocol",
//     tags: ["search", "ai"],
//     category: "web-browsing",
//   },
//   {
//     id: "browserless-mcp",
//     name: "Browserless MCP",
//     provider: "browserless",
//     description: "Headless browser automation and web scraping through MCP",
//     tags: ["browser", "automation"],
//     category: "web-browsing",
//   },
//   {
//     id: "scrapeowl-mcp",
//     name: "ScrapeOwl MCP",
//     provider: "scrapeowl",
//     description: "Web scraping and data extraction service with MCP integration",
//     tags: ["scraping", "data"],
//     category: "web-browsing",
//   },

//   // Communication/Collaboration
//   {
//     id: "slack-mcp",
//     name: "Slack MCP",
//     provider: "slack",
//     description: "Connect to Slack workspaces and channels through MCP protocol",
//     tags: ["messaging", "teams"],
//     category: "communication",
//   },
//   {
//     id: "notion-mcp",
//     name: "Notion MCP",
//     provider: "notion",
//     description: "Access and update Notion workspaces and databases via MCP",
//     tags: ["notes", "collaboration"],
//     category: "communication",
//   },
//   {
//     id: "teams-mcp",
//     name: "Microsoft Teams MCP",
//     provider: "microsoft",
//     description: "Integrate with Microsoft Teams for communication and collaboration",
//     tags: ["messaging", "microsoft"],
//     category: "communication",
//   },
//   {
//     id: "discord-mcp",
//     name: "Discord MCP",
//     provider: "discord",
//     description: "Connect to Discord servers and channels through MCP protocol",
//     tags: ["messaging", "community"],
//     category: "communication",
//   },

//   // Code and Development
//   {
//     id: "github-mcp",
//     name: "GitHub MCP",
//     provider: "github",
//     description: "Access GitHub repositories, issues, and pull requests via MCP",
//     tags: ["git", "code"],
//     category: "development",
//   },
//   {
//     id: "vscode-mcp",
//     name: "VS Code MCP",
//     provider: "microsoft",
//     description: "Connect to VS Code for code editing and development workflows",
//     tags: ["editor", "ide"],
//     category: "development",
//   },
//   {
//     id: "replit-mcp",
//     name: "Replit MCP",
//     provider: "replit",
//     description: "Access Replit workspaces and collaborate on code through MCP",
//     tags: ["coding", "cloud"],
//     category: "development",
//   },
//   {
//     id: "figma-mcp",
//     name: "Framelink Figma MCP",
//     provider: "GLips",
//     description: "MCP server to provide Figma layout information to AI coding agents like Cursor",
//     tags: ["design", "ui"],
//     category: "development",
//   },
// ]

// export function getServersByCategory(category: string) {
//   return servers.filter((server) => server.category === category)
// }

// export const categories = [
//   {
//     id: "file-management",
//     title: "File Management",
//     servers: getServersByCategory("file-management"),
//   },
//   {
//     id: "web-browsing",
//     title: "Web Browsing/Scraping",
//     servers: getServersByCategory("web-browsing"),
//   },
//   {
//     id: "communication",
//     title: "Communication/Collaboration",
//     servers: getServersByCategory("communication"),
//   },
//   {
//     id: "development",
//     title: "Code and Development",
//     servers: getServersByCategory("development"),
//   },
// ]
